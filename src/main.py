import repo


repo = repo.Repo

lst = repo.get_list()

print(lst)

proj = lst[0]

# repo.install(proj)

repo.run_project(proj)
