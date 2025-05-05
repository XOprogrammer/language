from urllib.request import *
from urllib.parse import *
import os
import shutil

__all__ = ['ReptileUtil']

try:
    from bs4 import *
except Exception:
    os.system("chcp 65001")
    os.system("python.exe -m pip install --upgrade pip")
    os.system("pip uninstall bs4")
    os.system("pip install bs4")

__all__ = ['ReptileUtil', 'version']

# 版本号
def version() -> str:
    vs = 'v1.0.0'
    prompt = '''
主版本号（x）：
    • 主版本号用于表示产品的主要版本或重大更新。
    • 当主版本号增加时，通常意味着产品发生了重大变化或引入了不兼容的更新。
    • 例如，从1.0.0到2.0.0的升级可能表示产品经历了重大重构或引入了全新的功能集。
次版本号（y）：
    • 次版本号用于表示产品的次要更新或功能增强。
    • 当次版本号增加时，通常意味着产品在保持向后兼容性的同时，增加了新的功能或改进了现有功能。
    • 例如，从1.1.0到1.2.0的升级可能表示产品增加了新的功能或优化了用户体验。
修订号（z）：
    • 修订号用于表示产品的修复或微调。
    • 当修订号增加时，通常意味着产品修复了已知的bug、改进了性能或进行了其他微小的调整。
    • 例如，从1.1.1到1.1.2的升级可能表示产品修复了一个或多个影响用户体验的bug。
'''
    print(f'\033[34m{prompt}\nFilesUtil: {vs}\033[0m')
    return vs

class ReptileUtil:
    def get_header(self):
        """获取当前请求头字典"""
        return self.__head

    def set_header(self, **kwargs: str|int|list|set|dict|tuple|float):
        """
        设置请求头键值对
        :param kwargs: 键值对
        """
        __this_header = kwargs
        try:
            __this_header["user_agent"] = kwargs["user_agent"]
        except KeyError:
            __this_header["user-agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                                       "/132.0.0.0 Safari/537.36")
        __this_header = {k.replace("_", "-"): v for k, v in __this_header.items()}
        self.__head = __this_header
        return self

    @staticmethod
    def create_dir(dir_path: str):
        """
        创建或清空目录
        :param dir_path: 目录路径
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        else:
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)

    @staticmethod
    def url_code(string: str):
        """
        将字符串转为URL编码
        :param string: 要编码的字符串
        :return: URL编码后的字符串
        """
        return quote(string)

    @staticmethod
    def r_url_code(string: str):
        """
        将URL编码解析为字符串
        :param string: URL编码字符串
        :return: 解码后的字符串
        """
        return unquote(string)

    @staticmethod
    def get(url: str, headers: dict):
        """
        GET请求获取网页源码
        :param url: 请求URL
        :param headers: 请求头字典
        :return: 网页源码(bytes)
        """
        req = Request(
            url=url,
            headers=headers
        )
        return urlopen(req).read()

    @staticmethod
    def post(url: str, headers: dict, data: dict):
        """
        POST请求获取网页源码
        :param url: 请求URL
        :param headers: 请求头字典
        :param data: POST数据字典
        :return: 网页源码字符串
        """
        req = Request(
            method="POST",
            url=url,
            headers=headers,
            data=bytes(urlencode(data), encoding="utf-8")
        )
        return urlopen(req).read().decode('utf-8')

    def r_get(self, url: str, headers: dict):
        """
        GET请求并用BeautifulSoup解析
        :param url: 请求URL
        :param headers: 请求头字典
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(self.get(url=url, headers=headers).decode("utf-8"), "html.parser")

    def r_post(self, url: str, headers: dict, data: dict):
        """
        POST请求并用BeautifulSoup解析
        :param url: 请求URL
        :param headers: 请求头字典
        :param data: POST数据字典
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(self.post(url=url, headers=headers, data=data).decode("utf-8"), "html.parser")

    @staticmethod
    def download(load_path: str, save_path: str):
        """
        下载文件(使用urlretrieve)
        :param load_path: 文件下载URL
        :param save_path: 本地保存路径
        :return: (filename, headers)元组
        """
        return urlretrieve(load_path, save_path)

    def download_req(self, load_path: str, save_path: str):
        """
        下载文件(使用Request)
        :param load_path: 文件下载URL
        :param save_path: 本地保存路径
        """
        req = Request(
            url=load_path,
            headers=self.get_header()
        )
        with urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())

    @staticmethod
    def re_help(get_re: bool = False):
        """
        显示帮助信息
        :param get_re: 是否获取返回值（默认否）
        """
        __re_help = "\t\t:param get_re: 是否获取返回值（默认否）"
        __get_header = "\t\t:return: 当前请求头字典"
        __set_header = "\t\t:param key: 请求头键名\n\t\t:param value: 请求头值"
        __createDir = "\t\t:param dirPath: 文件夹路径"
        __urlCode = "\t\t:param String: 要编码的字符串\n\t\t:return: URL编码后的字符串"
        __rUrlCode = "\t\t:param String: URL编码字符串\n\t\t:return: 解码后的字符串"
        __Get = "\t\t:param url: 请求URL\n\t\t:param headers: 请求头字典\n\t\t:return: 网页源码(bytes)"
        __Post = "\t\t:param url: 请求URL\n\t\t:param headers: 请求头字典\n\t\t:param data: POST数据字典\n\t\t:return: 网页源码字符串"
        __rGet = "\t\t:param url: 请求URL\n\t\t:param headers: 请求头字典\n\t\t:return: BeautifulSoup对象"
        __rPost = "\t\t:param url: 请求URL\n\t\t:param headers: 请求头字典\n\t\t:param data: POST数据字典\n\t\t:return: BeautifulSoup对象"
        __htmlSave = "\t\t:param path: 文件保存路径\n\t\t:param html: HTML内容"
        __Download = "\t\t:param loadPath: 文件下载URL\n\t\t:param savePath: 本地保存路径\n\t\t:return: (filename, headers)元组"
        __Download_req = "\t\t:param loadPath: 文件下载URL\n\t\t:param savePath: 本地保存路径"

        # 按照您要求的顺序排列
        func_list = [
            ['re_help', '显示帮助信息', __re_help],
            ['get_header', '获取当前请求头', __get_header],
            ['set_header', '设置请求头键值对', __set_header],
            ['createDir', '创建或清空目录', __createDir],
            ['urlCode', 'URL编码字符串', __urlCode],
            ['rUrlCode', 'URL解码字符串', __rUrlCode],
            ['Get', 'GET请求获取网页源码', __Get],
            ['Post', 'POST请求获取网页源码', __Post],
            ['rGet', 'GET请求并用BeautifulSoup解析', __rGet],
            ['rPost', 'POST请求并用BeautifulSoup解析', __rPost],
            ['htmlSave', '保存HTML到文件', __htmlSave],
            ['Download', '下载文件(urlretrieve)', __Download],
            ['Download_req', '下载文件(Request)', __Download_req]
        ]

        if get_re:
            return func_list

        for func in func_list:
            print(f"\033[34m{func[0]}\033[0m", end='')  # 蓝色方法名
            print(f"\033[32m\t{func[1]}\033[0m")  # 绿色功能描述
            print(func[2], end='\n\n')  # 参数说明

    def __init__(self):
        self.__head = {}
