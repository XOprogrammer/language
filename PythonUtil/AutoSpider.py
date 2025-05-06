from urllib.request import *
from urllib.parse import *
from time import sleep
from os import path, mkdir, system
from shutil import rmtree

try:
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import JavascriptException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.common.exceptions import NoSuchDriverException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
except ModuleNotFoundError:
    print(f'\033[31m未知模块[Error]：selenium\033[0m')

__version__ = '2.0.2'
__author__ = 'yzmd <a2541507030@163.com>'

__all__ = ['ReptileUtil', 'SeleniumTest', 'version']

try:
    from bs4 import *
except Exception:
    system("chcp 65001")
    system("python.exe -m pip install --upgrade pip")
    system("pip uninstall bs4")
    system("pip install bs4")

# 版本号
def version() -> str:
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
    print(f'\033[34m{prompt}\nFilesUtil: v{__version__}\033[0m')
    return __version__

class ReptileUtil:
    def get_header(self):
        """获取当前请求头字典"""
        if self.__head == {}:
            self.__head = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
            }
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
        if not path.exists(dir_path):
            mkdir(dir_path)
        else:
            rmtree(dir_path)
            mkdir(dir_path)

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

    def get(self, url: str, headers: dict = None):
        """
        GET请求获取网页源码
        :param url: 请求URL
        :param headers: 请求头字典
        :return: 网页源码(bytes)
        """
        if headers is None:
            headers = self.get_header()
        req = Request(
            url=url,
            headers=headers
        )
        return urlopen(req).read()

    def post(self, url: str, data: dict, headers: dict = None):
        """
        POST请求获取网页源码
        :param url: 请求URL
        :param headers: 请求头字典
        :param data: POST数据字典
        :return: 网页源码字符串
        """
        if headers is None:
            headers = self.get_header()
        req = Request(
            method="POST",
            url=url,
            headers=headers,
            data=bytes(urlencode(data), encoding="utf-8")
        )
        return urlopen(req).read().decode('utf-8')

    def r_get(self, url: str, headers: dict = None):
        """
        GET请求并用BeautifulSoup解析
        :param url: 请求URL
        :param headers: 请求头字典
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(self.get(url=url, headers=headers).decode("utf-8"), "html.parser")

    def r_post(self, url: str, data: dict, headers: dict = None):
        """
        POST请求并用BeautifulSoup解析
        :param url: 请求URL
        :param headers: 请求头字典
        :param data: POST数据字典
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(self.post(url=url, headers=headers, data=data).decode("utf-8"), "html.parser")

    @staticmethod
    def download(load_path: str, save_path: str, delayed: int = 0):
        """
        下载文件(使用urlretrieve)
        :param load_path: 文件下载URL
        :param save_path: 本地保存路径
        :param delayed: 延时秒数
        """
        urlretrieve(load_path, save_path)
        sleep(delayed)

    def download_req(self, load_path: str, save_path: str, delayed: int = 0):
        """
        下载文件(使用Request)
        :param load_path: 文件下载URL
        :param save_path: 本地保存路径
        :param delayed: 延时秒数
        """
        req = Request(
            url=load_path,
            headers=self.get_header()
        )
        with urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())
        sleep(delayed)

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

class SeleniumTest:
    # 报错信息输出
    @staticmethod
    def __err(string: str = '', start_text: str = 'Error: ', end: str = '\n'):
        """打印红色错误信息"""
        print(f'\033[31m{start_text}{string}\033[0m', end=end)

    # 警告信息输出
    @staticmethod
    def __warn(string: str = '', start_text: str = 'Warning: ', end: str = '\n'):
        """打印黄色警告信息"""
        print(f'\033[33m{start_text}{string}\033[0m', end=end)

    # 提示信息输出
    @staticmethod
    def __prompt(string: str = '', start_text: str = 'Prompt: ', end: str = '\n'):
        """打印蓝色提示信息"""
        print(f'\033[34m{start_text}{string}\033[0m', end=end)

    # 成功信息输出
    @staticmethod
    def __success(string: str = '', start_text: str = 'Success: ', end: str = '\n'):
        """打印绿色成功信息"""
        print(f'\033[32m{start_text}{string}\033[0m', end=end)

    # 模式字符串转换
    @staticmethod
    def __this_mode(mode):
        """
        将模式字符串转换为Selenium的By常量
        :param mode: 模式字符串(css/class_/id/xpath/ele/link/p_link)
        :return: 对应的By常量
        """
        mode = mode.lower()
        if mode == 'class':
            return 'CLASS_NAME'
        elif mode == 'id':
            return 'ID'
        elif mode == 'xpath':
            return 'XPATH'
        elif mode == 'name':
            return 'NAME'
        elif mode == 'ele':
            return 'TAG_NAME'
        elif mode == 'link':
            return 'LINK_TEXT'
        elif mode == 'p_link':
            return 'PARTIAL_LINK_TEXT'
        else:
            return 'CSS_SELECTOR'

    def get_page(self, url: str):
        """
        打开指定网页
        :param url: 要打开的网页URL
        """
        self.driver.get(url)
        self.get_wait_ele(self.driver, 30, 'ele', 'body', err_msg='主元素加载失败！')

    def js_get_page(self, url: str, page_num: int = -1):
        """
        使用JavaScript在新标签页中打开网页
        :param url: 要打开的URL
        :param page_num: 要切换到的页面索引(默认-1表示最后一个标签页)
        """
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.position_page(page_num)

    def get_ele(self, parent_ele: WebElement, mode: str = 'css', mode_ele: str = None, single_duo: bool = False):
        """
        在父元素内查找元素
        :param parent_ele: 要查找的父元素
        :param mode: 查找模式(css/class_/id/xpath/ele/link/p_link)
        :param mode_ele: 元素标识符(选择器/类名/ID等)
        :param single_duo: 是否查找多个元素(False表示查找单个元素)
        :return: 找到的WebElement(或多个元素列表)
        """
        mode = self.__this_mode(mode)
        if single_duo:
            return parent_ele.find_elements(eval(f'By.{mode}'), mode_ele)
        else:
            return parent_ele.find_element(eval(f'By.{mode}'), mode_ele)

    @staticmethod
    def get_attr(ele: WebElement, ele_type: str):
        """
        获取元素属性值
        :param ele: 要获取属性的WebElement
        :param ele_type: 要获取的属性名
        :return: 属性值
        """
        return ele.get_attribute(ele_type)

    def js_click(self, ele_btn: WebElement):
        """
        使用JavaScript点击元素(适用于元素被遮挡时)
        :param ele_btn: 要点击的元素
        """
        self.driver.execute_script('arguments[0].click()', ele_btn)

    def get_wait_ele(self, parent_ele: WebElement, timeout: int = 0, mode: str = 'css', mode_ele: str = None, single_duo: bool = False, err_msg: str = '元素寻找超时！'):
        """
        等待元素出现
        :param parent_ele: 要查找的父元素
        :param timeout: 最大等待时间(秒)
        :param mode: 查找模式(css/class_/id/xpath/ele/link/p_link)
        :param mode_ele: 元素标识符(选择器/类名/ID等)
        :param single_duo: 是否查找多个元素(False表示查找单个元素)
        :param err_msg: 超时错误信息
        :return: 找到的WebElement(或多个元素列表)
        """
        mode = self.__this_mode(mode)
        ds_str = 'presence_of_element_located'
        if single_duo:
            ds_str = 'presence_of_all_elements_located'
        return WebDriverWait(parent_ele, timeout).until(
            eval(f'EC.{ds_str}')((eval(f'By.{mode}'), mode_ele)),
            message=err_msg)

    @staticmethod
    def download(load_path: str, save_path: str):
        """
        下载文件(使用urlretrieve)
        :param load_path: 文件下载URL
        :param save_path: 本地保存路径
        :return: (filename, headers)元组
        """
        return urlretrieve(load_path, save_path)

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
    def create_dir(dir_path: str):
        """
        创建或清空目录
        :param dir_path: 目录路径
        """
        if not path.exists(dir_path):
            mkdir(dir_path)
        else:
            rmtree(dir_path)
            mkdir(dir_path)

    def set_win_size(self, width: int | float = 800, height: int | float = 500):
        """
        设置浏览器窗口大小
        :param width: 窗口宽度
        :param height: 窗口高度
        """
        self.driver.set_window_size(width, height)

    def close(self, page_num: int = -1):
        """
        关闭当前标签页并切换到指定标签页
        :param page_num: 要切换到的标签页索引(默认-1表示最后一个标签页)
        """
        self.driver.close()
        self.position_page(page_num)

    def quit(self, one_key: bool = True):
        """
        退出浏览器
        :param one_key: 是否立即退出(True)或等待用户回车后退出(False)
        """
        if one_key:
            self.driver.quit()
        else:
            input('\033[34m在此回车退出！\033[0m')
            self.driver.quit()

    def reload(self, toggle_f5: bool = False):
        """
        刷新页面
        :param toggle_f5: 是否使用F5键刷新(False使用refresh方法)
        """
        if toggle_f5:
            self.get_wait_ele(self.driver, 30, 'ele', 'body').send_keys(Keys.F5)
        else:
            self.driver.refresh()

    def move_ele(self, parent_ele: WebElement, timeout: int = 0, mode: str = 'css', mode_ele: str = None, ranges: int = False, ele_a: WebElement = None,ele_b: WebElement = None, err_msg: str = ''):
        """
        移动元素(滑块验证或拖放)
        :param parent_ele: 父元素
        :param timeout: 等待超时时间
        :param mode: 查找模式
        :param mode_ele: 元素标识符
        :param ranges: 移动距离(像素)
        :param ele_a: 要拖动的元素
        :param ele_b: 目标元素
        :param err_msg: 错误信息
        """
        actions = ActionChains(parent_ele)
        if ele_a is None and ele_b is None:
            slider = self.get_wait_ele(parent_ele, timeout, mode, mode_ele, False, err_msg)
            actions.click_and_hold(slider).move_by_offset(ranges, 0).release().perform()
        else:
            actions.drag_and_drop(ele_a, ele_b).perform()

    def js_scroll_page(self, parent_ele: WebElement, mode: str = 'px', ranges: int = 0, scroll_num: int = 1):
        """
        滚动页面
        :param parent_ele: 父元素或滚动参照元素
        :param mode: 滚动模式(px/ele/p_ele)
        :param ranges: 滚动距离(像素)或元素位置
        :param scroll_num: 滚动次数
        """
        actions = ActionChains(self.driver)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState === 'complete'")
        )
        for _ in range(scroll_num):
            if mode == 'ele':
                actions.scroll_to_element(parent_ele).perform()
            elif mode == 'p_ele':
                actions.scroll_to_element(parent_ele).perform()
                actions.scroll_by_amount(0, ranges).perform()
            else:
                actions.scroll_by_amount(0, ranges).perform()

    def position_page(self, page_num: int = 0):
        """
        切换到指定标签页
        :param page_num: 标签页索引
        """
        self.driver.switch_to.window(self.driver.window_handles[page_num])

    def js_get_text(self, ele: WebElement, get_text: bool = False):
        """
        获取指定元素（单层）或元素内（包含子元素）所有文本内容
        :param ele: 指定元素
        :param get_text: 是否获取所有文本（默认否）
        :return: 文本内容
        """
        if get_text:
            return ele.text
        return self.driver.execute_script('return arguments[0].childNodes[0].textContent.trim();', ele)

    def help(self, get_re: bool = False):
        """
        显示帮助信息
        :param get_re: 是否获取返回值（默认否）
        """
        __help = "\t\t:param get_re: 是否获取返回值（默认否）"
        __get_page = "\t\t:param url: 网址"
        __get_ele = ('\t\t:param parent_ele: 在此元素范围内查询\n\t\t'
                     ':param mode: 查询模式，模式如下\n\t\t\t\t'
                     '① css（默认）：使用css选择器查询\n\t\t\t\t'
                     '② class_：使用类名选择器查询\n\t\t\t\t'
                     '③ id：使用id选择器查询\n\t\t\t\t'
                     '④ xpath：使用xpath路径查询\n\t\t\t\t'
                     '⑤ ele：使用html标签名查询\n\t\t\t\t'
                     '⑥ link：使用完整超链接文本查询（此文本指：<a href="#">这里的文本</a>）\n\t\t\t\t'
                     '⑦ p_link: 使用部分超链接文本查询（此文本指：在link文本的基础上自定义截取的部分文本）\n\t\t'
                     ':param mode_ele: 查询此元素\n\t\t'
                     ':param single_duo: 是否启用多元素查询（默认：否）\n:return: 查询结果')
        __get_attr = ('\t\t:param ele: 指定元素\n\t\t'
                      ':param ele_type: 指定属性\n\t\t'
                      ':return: 属性值')
        __js_click = '\t\t:param ele_btn: 被点击的元素'
        __get_wait_ele = ('\t\t:param parent_ele: 指定元素范围\n\t\t'
                          ':param timeout: 超时时间\n\t\t'
                          ':param mode: 查询模式，模式如下\n\t\t\t\t'
                          '① css（默认）：使用css选择器查询\n\t\t\t\t'
                          '② class_：使用类名选择器查询\n\t\t\t\t'
                          '③ id：使用id选择器查询\n\t\t\t\t'
                          '④ xpath：使用xpath路径查询\n\t\t\t\t'
                          '⑤ ele：使用html标签名查询\n\t\t\t\t'
                          '⑥ link：使用完整超链接文本查询（此文本指：<a href="#">这里的文本</a>）\n\t\t\t\t'
                          '⑦ p_link: 使用部分超链接文本查询（此文本指：在link文本的基础上自定义截取的部分文本）\n\t\t'
                          ':param mode_ele: 查询元素\n\t\t'
                          ':param single_duo: 是否启用多元素查询（默认：否）\n\t\t'
                          ':param err_msg: 超时信息\n\t\t'
                          ':return: 查询结果')
        __Download = ('\t\t:param loadPath: 文件的下载地址\n\t\t'
                      ':param savePath: 文件的保存路径 + 文件名.后缀名')
        __urlCode = '\t\t:param String: 字符串'
        __rUrlCode = '\t\t:param String: url字段'
        __createDir = '\t\t:param dirPath: 文件夹名'
        __set_win_size = '\t\t:param width: 宽度\n\t\t:param height: 高度'
        __close = '\t\t:param page_num: 页面序号'
        __quit = '\t\t:param Onekey: 是否一键退出（默认：是）'
        __reload = '\t\t:param toggle_f5: 是否使用F5键刷新（默认：否）'
        __move_ele = ('\t\t:param parent_ele: 父元素\n\t\t'
                      ':param timeout: 超时时间\n\t\t'
                      ':param mode: 查询模式\n\t\t'
                      ':param mode_ele: 查询元素\n\t\t'
                      ':param ranges: 移动距离\n\t\t'
                      ':param ele_a: 要拖动的元素\n\t\t'
                      ':param ele_b: 目标元素\n\t\t'
                      ':param err_msg: 错误信息')
        __js_scroll_page = ('\t\t:param parent_ele: 父元素\n\t\t'
                            ':param mode: 滚动模式(px/ele/p_ele)\n\t\t'
                            ':param ranges: 滚动距离\n\t\t'
                            ':param scroll_num: 滚动次数')
        __position_page = '\t\t:param page_num: 页面序号'
        __js_get_page = '\t\t:param url: 网址\n\t\t:param page_num: 页面序号'
        __driver = 'selenium中的driver（此为变量而非方法）'
        __js_get_text = ('\t\t:param ele: 指定元素\n\t\t'
                         ':param get_text: 是否获取所有文本（默认否）\n\t\t'
                         ':return: 文本内容')

        __init = ("\t\t:param driver_path: chromedriver.exe的路径\n\t\t"
                  ":param headless_tf: 是否启用无头？（默认：否）")

        # 按照您要求的顺序排列，__init__在最后
        func_list = [
            ['help', '帮助', __help],
            ['get_page', '获取网页', __get_page],
            ['js_get_page', 'JS方式获取网页', __js_get_page],
            ['get_ele', '查询指定元素范围内的指定元素', __get_ele],
            ['get_attr', '查询指定元素的指定属性', __get_attr],
            ['js_click', '使用js点击元素（可用于元素被遮挡时）', __js_click],
            ['get_wait_ele', '等待查询元素', __get_wait_ele],
            ['Download', '下载文件', __Download],
            ['urlCode', '将字符串转为url编码', __urlCode],
            ['rUrlCode', '将url编码解析为字符串', __rUrlCode],
            ['createDir', '创建或清空目录', __createDir],
            ['set_win_size', '设置窗口大小', __set_win_size],
            ['close', '关闭当前标签页', __close],
            ['quit', '退出浏览器', __quit],
            ['reload', '刷新页面', __reload],
            ['move_ele', '移动元素(滑块/拖放)', __move_ele],
            ['js_scroll_page', '滚动页面', __js_scroll_page],
            ['position_page', '切换到指定标签页', __position_page],
            ['js_get_text', '获取指定元素（单层）或元素内（包含子元素）所有文本内容', __js_get_text],
            ['driver', '浏览器驱动对象', __driver],
            ['__init__', '初始化浏览器', __init]
        ]

        if get_re:
            return func_list

        for func in func_list:
            self.__prompt(func[0], '')
            self.__success(func[1], '\t')
            print(func[2], end='\n\n')

    def __init__(self, driver_path: str = None, headless_tf: bool = False):
        """
        初始化浏览器驱动
        :param driver_path: chromedriver路径
        :param headless_tf: 是否启用无头模式
        """
        try:
            if driver_path:
                self.__service = Service(executable_path=driver_path)
            if headless_tf:
                self.__chrome_options = Options()
                self.__chrome_options.add_argument("--headless")
            if driver_path and headless_tf:
                self.driver = Chrome(service=self.__service, options=self.__chrome_options)
            elif driver_path and headless_tf is False:
                self.driver = Chrome(service=self.__service)
            elif driver_path is None and headless_tf:
                self.driver = Chrome(options=self.__chrome_options)
            else:
                self.driver = Chrome()
        except NoSuchDriverException:
            self.__err('未找到chromedriver.exe！（可能未下载或未设置为环境变量）', '初始化错误[Error]: ')
            self.__prompt(self.help(True)[-1][0], '', '\n\t')
            self.__success(self.help(True)[-1][1], '')
            print(self.help(True)[-1][2])