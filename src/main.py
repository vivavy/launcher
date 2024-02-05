import sys, repo


BULLET = "•"

help_0 = """
Введи "list" чтобы получить список проектов
Введи "install [package]" чтобы установить проект
Введи "upgrade [package]" чтобы обновить проект
Введи "remove [package]" чтобы удалить проект
Введи "run package" чтобы запустить проект
Введи "info package" чтобы узнать информацию о проекте
Введи "exit" чтобы выйти
Нажми CTRL+C чтобы выйти
"""

repo = repo.Repo

while True:
    try:
        cmd = list(input(help_0).split())

        if cmd[0] == "list":
            lst = repo.get_list()
            ins = repo.get_installed()
            print("\nУстановленные:")

            for p in ins:
                print(BULLET, p)

            print("\nДоступные для установки:")

            for p in lst:
                if p not in ins:
                    print(BULLET, p)

        if cmd[0] == "install":
            if len(cmd) < 2:
                cmd.append("Название проекта> ")

            for proj in cmd[1:]:
                if proj not in repo.get_list() or proj in repo.get_installed():
                    print(f"Проект \"{proj}\" недоступен для установки. Либо его не существует, либо он уже установлен.")
                    print(f"Введи \"list\" и перепроверь.")

                else:
                    repo.install(proj)

        if cmd[0] == "upgrade":
            if len(cmd) < 2:
                cmd.append("Название проекта> ")

            for proj in cmd[1:]:
                if proj == "launcher":
                    info = repo.get_info()
                    repo.purge(proj)
                    repo.install(proj)
                    repo.set_info(info)
                if proj not in repo.get_installed():
                    print(f"Проект \"{proj}\" недоступен для установки. Либо его не существует, либо он уже установлен.")
                    print(f"Введи \"list\" и перепроверь.")

                else:
                    repo.purge(proj)
                    repo.install(proj)

        if cmd[0] == "remove":
            if len(cmd) < 2:
                cmd.append("Название проекта> ")

            for proj in cmd[1:]:
                if proj not in repo.get_installed():
                    print(f"Проект \"{proj}\" не установлен")

                else:
                    repo.purge(proj)

        if cmd[0] == "run":
            if len(cmd) < 2:
                cmd.append("Название проекта> ")

            for proj in cmd[1:]:
                if proj not in repo.get_installed():
                    print(f"Проект \"{proj}\" не установлен")

                else:
                    repo.run_project(proj)
        if cmd[0] == "info":
            if len(cmd) < 2:
                cmd.append("Название проекта> ")

            if cmd[1] not in repo.get_installed():
                print("Этот проект не установлен")

            else:
                repo.print_info(proj)
        
        if cmd[0] == "exit":
            sys.exit()

    except KeyboardInterrupt:
        break
