from urllib.request import *
from urllib.parse import *
from requests import get
from bs4 import *
from re import *


def imgDownLoad(lists: list = None):
    if lists is not None:
        return lists
    else:
        return []


def imgPath(filePath: str = ""):
    return filePath


def urlCode(String: str):
    return quote(String)


def Get(**kwargs):
    req = Request(
        url=kwargs["url"],
        headers=kwargs["headers"]
    )
    return urlopen(req).read()


def rGet(**kwargs):
    return BeautifulSoup(Get(**kwargs).decode("utf-8"), "html.parser")


def Download(**kwargs):
    with open(kwargs["path"], "wb") as download:
        download.write(get(kwargs["file"]).content)


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/119.0.0.0"
                  "Safari/537.36",
    "Cookie": "PHPSESSID=opiodjl1kfite6ok7950kn8u54; Hm_lvt_fe338b12aba190ae800147b6d1d0d309=1700177214; "
              "Hm_lpvt_fe338b12aba190ae800147b6d1d0d309=1700177993"
}

catStep = 0
for k in imgDownLoad():
    for page in range(1, 1000):
        bs = rGet(
            url=f"https://www.toopic.cn/index.php/index_index_soso?kw={urlCode(k)}&page={page}",
            headers=head
        )
        if len(bs.find_all("img")) <= 1:
            break
        for i in bs.find_all("img"):
            if search(r"(jpg)|(png)", i.attrs["src"]):
                catStep += 1
                print(f"开始下载第{catStep}个")
                Download(
                    path=f"{imgPath().replace(r'/$', '')}/{catStep}.png",
                    file=f"https://www.toopic.cn{i.attrs['src']}"
                )
