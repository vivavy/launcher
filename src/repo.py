import requests as req
import json
import os
import zipfile
import sys


class Repo:
    def get_list() -> list[str]:
        return json.loads(req.get("https://raw.githubusercontent.com/vivavy/vilauncher/main/index.json").text)["list"]
    
    def get_installed() -> None:
        with open(Repo.get_src_path("launcher"), "rt") as f:
            return json.load(f)["list"]
    
    def run_project(proj: str) -> None:
        info = Repo.get_info(proj)

        command = Repo.get_src_path(proj) + "/main.py"
        
        os.system("cls")
        os.system(command)
    
    def get_info(proj: str) -> dict:
        return json.loads(req.get(f"https://raw.githubusercontent.com/vivavy/{proj}/main/meta_inf.json").text)
    
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

        os.rename(Repo.get_viis_path() + "\\" + proj + "-main", Repo.get_viis_path() + "\\" + proj)
        proj_path = Repo.get_viis_path() + "\\" + proj
        os.system(proj_path + "\\install.py \"" + proj_path + "\"")

    def get_viis_path() -> os.PathLike:
        if os.name == 'nt':
            return "C:\\Users\\" + os.getlogin() + "\\viis"
        
        elif os.name == 'vi':
            return "app://ru.vivisoft.viis"
        
        else:
            return "/home/" + os.getlogin() + "/viis"
