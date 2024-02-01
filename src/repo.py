import requests as req
import json


class Repo:
    def get_list() -> list[str]:
        return json.loads(req.get("https://raw.githubusercontent.com/vivavy/vilauncher/main/index.json").text)["list"]
    
    def get_info(proj: str) -> dict:
        return json.loads(req.get(f"https://raw.githubusercontent.com/vivavy/{proj}/main/meta_inf.json").text)


if __name__ == '__main__':
    while 1:
        lst = Repo.get_list()
        for n, i in enumerate(lst):
            print(str(n + 1) + ")", lst[n])
        index = int(input("select project> ")) - 1
        print(Repo.get_info(lst[n]))
