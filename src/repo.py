import os


if os.name == "nt":
    from repo_win import *
elif os.name == "vi":
    from repo_vios import *
else:
    from repo_posix import *
