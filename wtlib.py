import win32console
import win32file
import win32con
import os, sys, pprint


ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040

KEYPRESS = 1
MOUSEMOTION = 2
MOUSEBUTTONDOWN = 3
LEFT = 4
RIGHT = 5
DOUBLE = 6


class Event:
    def __init__(self, **k):
        self.__dict__.update(k)
    
    def __str__(self):
        dct = {**self.__dict__}
        for i in dct:
            if i.startswith("__"):
                dct.remove(i)
        return "Event " + pprint.pformat(dct, 4, 128)
    
    def __repr__(self):
        return self.__str__()


class Frame:
    def __init__(self, wt, name, pos, size):
        self.wt = wt
        self.name, self.pos, self.size = name, Event(x=pos[0], y=pos[1]), Event(x=size[0], y=size[1])
    
    def render(self):
        self.wt.set_at("┌", self.pos.x, self.pos.y)
        self.wt.set_at("┐", self.pos.x + self.size.x, self.pos.y) 
        self.wt.set_at("└", self.pos.x, self.pos.y + self.size.y)
        self.wt.set_at("┘", self.pos.x + self.size.x, self.pos.y + self.size.y)
        
        for x in range(self.size.x - 1):
            self.wt.set_at("─", self.pos.x + 1 + x, self.pos.y)
            self.wt.set_at("─", self.pos.x + 1 + x, self.pos.y + self.size.y)
        
        for y in range(self.size.y - 1):
            self.wt.set_at("│", self.pos.x, self.pos.y + 1 + y)
            self.wt.set_at("│", self.pos.x + self.size.x, self.pos.y + 1 + y)
        
        for x, c in enumerate(self.name):
            self.wt.set_at(c, self.pos.x + x + 1, self.pos.y + 1)


class WT:
    def __init__(self, title: str = "ViLauncher") -> None:
        self.title = title
        os.system("echo -ne \"\\e]0;"+self.title+"\\a\"")
        self.win_in = win32console.PyConsoleScreenBufferType(
            win32file.CreateFile("CONIN$",
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                win32file.FILE_SHARE_READ,
                None,
                win32file.OPEN_ALWAYS,
                0,
                None
            )
        )

        self.win_in.SetStdHandle(win32console.STD_INPUT_HANDLE)

        self.in_mode = self.win_in.GetConsoleMode()
        self.new_mode = (self.in_mode | win32console.ENABLE_MOUSE_INPUT | ENABLE_EXTENDED_FLAGS)
        self.new_mode &= ~ENABLE_QUICK_EDIT_MODE
        self.win_in.SetConsoleMode(self.new_mode)

        os.system("mode 192,72")

        self.clear()
    
    def flip(self):
        sys.stdout.write("".join(tuple(self.buffer)))
        sys.stdout.flush()
    
    def clear(self):
        self.buffer = [" ",] * 192 * 72
    
    def set_at(self, s, x, y):
        self.buffer[x + y * 192] = s
    
    def pool(self):
        if len(self.win_in.PeekConsoleInput(1)) <= 0:
            return ()
        
        events = []

        for e in self.win_in.ReadConsoleInput(1):
            if e.EventType == win32console.KEY_EVENT:
                key = e.Char
                code = ord(key)
                events.append(Event(type=KEYPRESS, unicode=key, key=code))
            elif e.EventType == win32console.MOUSE_EVENT:
                pos = (e.MousePosition.X, e.MousePosition.Y)
                button = 0

                if e.EventFlags == 0:
                    if e.ButtonState & win32con.FROM_LEFT_1ST_BUTTON_PRESSED != 0:
                        button = LEFT
                    if e.ButtonState & win32con.RIGHTMOST_BUTTON_PRESSED != 0:
                        button = RIGHT
                elif e.EventFlags & win32con.DOUBLE_CLICK != 0:
                    button = DOUBLE
                
                if button:
                    events.append(Event(type=MOUSEBUTTONDOWN, pos=pos, button=button))
                else:
                    events.append(Event(type=MOUSEMOTION, pos=pos))
        
        return tuple(events)
    
    def __del__(self):
        self.quit()
    
    def quit(self):
        self.win_in.SetConsoleMode(self.in_mode)


wt = WT()

frame = Frame(wt, "Test Frame", (9, 4), (50, 10))

frame.render()
wt.flip()

while 1:
    for e in wt.pool():
        if e.type == MOUSEBUTTONDOWN:
            print(e)
