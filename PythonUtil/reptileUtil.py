from urllib.request import *
from urllib.parse import *
import os
import shutil

try:
    from bs4 import *
except Exception:
    os.system("chcp 65001")
    os.system("python.exe -m pip install --upgrade pip")
    os.system("pip uninstall bs4")
    os.system("pip install bs4")

__head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

def get_header():
    return __head

def set_header(key: str, value):
    __head[key] = value

def createDir(dirPath: str):
    """
    如果文件夹不存在就创建，如果文件存在就清空！
    :param dirPath: 文件夹名
    :return:
    """
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    else:
        shutil.rmtree(dirPath)
        os.mkdir(dirPath)


def urlCode(String: str):
    """
    将字符串转为url编码
    :param String: 字符串
    :return:
    """
    return quote(String)


def rUrlCode(String: str):
    """
    将url编码解析为字符串
    :param String: url字段
    :return:
    """
    return unquote(String)


def Get(url: str, headers: dict):
    """
    get请求获取网页源码
    :param url: 网址
    :param headers: 请求头
    :return:
    """
    req = Request(
        url=url,
        headers=headers
    )
    return urlopen(req).read()


def Post(url: str, headers: dict, data: dict):
    """
    post请求获取网页源码
    :param url: 网址
    :param headers: 请求头
    :param data: 请求参数
    :return:
    """
    req = Request(
        method="POST",
        url=url,
        headers=headers,
        data=bytes(urlencode(data), encoding="utf-8")
    )
    return urlopen(req).read().decode('utf-8')


def rGet(url: str, headers: dict):
    """
    将get请求回来的数据用bs4解析
    :param url: 网址
    :param headers: 请求头
    :return:
    """
    return BeautifulSoup(Get(url=url, headers=headers).decode("utf-8"), "html.parser")


def rPost(url: str, headers: dict, data: dict):
    """
    将post请求回来的数据用bs4解析
    :param url: 网址
    :param headers: 请求头
    :param data: 请求参数
    :return:
    """
    return BeautifulSoup(Post(url=url, headers=headers, data=data).decode("utf-8"), "html.parser")


def htmlSave(path: str, html: str):
    """
    保存html文件
    :param path: 另存为地址
    :param html: html内容
    :return:
    """
    with open(path, "w", encoding="utf-8") as h5:
        h5.write(str(html))


def Download(loadPath: str, savePath: str):
    """
    下载文件
    :param loadPath: 文件的下载地址
    :param savePath: 文件的保存路径 + 文件名.后缀名
    :return:
    """
    return urlretrieve(loadPath, savePath)
