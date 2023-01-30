from pathlib import Path
from os.path import join
from requests import get
from bs4 import BeautifulSoup
giturl = "https://github.com"


def git_content(user, repo, *pages, ext=None):
    content = []
    page_url = join(giturl, user, repo)
    if pages:
        page_url += join("/tree/main", *pages)
    page_data = get(page_url).text
    links = BeautifulSoup(page_data, "html.parser").find("body").findAll("a")
    for link in links:
        href = link.get("href")
        if ext:
            if href.endswith(f".{ext}"):
                content.append(dict(
                    filename=link.get("title"),
                    url=f"{giturl}{href}?raw=true"
                ))
        else:
            content.append(dict(
                filename=link.get("title"),
                url=f"{giturl}{href}?raw=true"
            ))
    return content


def get_files(path):
    path = Path(str(path))
    content = []
    files = [i for i in path.iterdir() if i.is_file()]
    for file in files:
        content.append(dict(
            filename=file.name,
            size=file.stat().st_size * 1.0e-6,
            path=str(file)
        ))
    return content
