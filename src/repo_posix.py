import requests as req
import json
import os
import zipfile
import sys
import shutil


class Repo:
    def get_list() -> list[str]:
        return json.loads(req.get("https://raw.githubusercontent.com/vivavy/vilauncher/main/index.json").text)["list"]
    
    def get_installed() -> list[str]:
        with open(Repo.get_src_path("launcher") + "/installed.json", "rt") as f:
            return json.load(f)["list"]
    
    def run_project(proj: str) -> None:
        info = Repo.get_info(proj)

        command = sys.executable + " " + Repo.get_src_path(proj) + "/main.py"
        
        os.system("clear")
        os.system(command)
    
    def purge(proj: str) -> None:
        shutil.rmtree(Repo.get_proj_path(proj))

        lst = Repo.get_installed()
        lst.remove(proj)
        
        with open(Repo.get_src_path("launcher") + "/installed.json", "wt") as f:
            json.dump({"list": lst}, f)
    
    def get_info(proj: str) -> dict:
        return json.loads(req.get(f"https://raw.githubusercontent.com/vivavy/{proj}/main/meta_inf.json").text)
    
    def print_info(proj: str):
        info = Repo.get_info(proj)
        print()
        print("Название:", info["name"])
        print("Описание:", info["desc"])
        print("Приоритет:", info["priority"])
        print("Статус:", info["status"])
        print("Зависимости:")
        
        for d in info["depencies"]:
            print("\t•", d)
    
    def get_zip(proj: str) -> os.PathLike:
        with open(proj + ".zip", "wb") as f:
            f.write(req.get(f"https://github.com/vivavy/{proj}/archive/refs/heads/main.zip").content)

        return proj + ".zip"
    
    def get_src_path(proj: str) -> os.PathLike:
        return Repo.get_proj_path(proj) + "/src"
    
    def get_proj_path(proj: str) -> os.PathLike:
        return Repo.get_viis_path() + "/" + proj
    
    def install(proj: str) -> None:
        Repo.get_zip(proj)

        with zipfile.ZipFile(proj + ".zip", 'r') as zip_ref:
            zip_ref.extractall(Repo.get_viis_path())
        
        os.remove(proj + ".zip")

        os.rename(Repo.get_viis_path() + "/" + proj + "-main", Repo.get_viis_path() + "/" + proj)
        proj_path = Repo.get_viis_path() + "/" + proj
        os.system(sys.executable + " " + proj_path + "/install.py \"" + proj_path + "\"")

        lst = Repo.get_installed()
        lst.append(proj)

        with open(Repo.get_src_path("launcher") + "/installed.json", "wt") as f:
            f.write(json.dumps({"list": lst}))

    def get_viis_path() -> os.PathLike:
        return "/home/" + os.getlogin() + "/viis"
    
    def set_info(info: dict) -> None:
        with open(Repo.get_src_path("launcher"), "wt") as f:
            json.dump(info, f)
