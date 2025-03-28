from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from os import path, mkdir
from shutil import rmtree
from urllib.parse import unquote, quote
from urllib.request import urlretrieve

class selenium_test:
    # 报错
    @staticmethod
    def __err(string: str = '', start_text: str = 'Error: ', end: str = '\n'):
        print(f'\033[31m{start_text}{string}\033[0m', end=end)

    # 警告
    @staticmethod
    def __warn(string: str = '', start_text: str = 'Warning: ', end: str = '\n'):
        print(f'\033[33m{start_text}{string}\033[0m', end=end)

    # 提示
    @staticmethod
    def __prompt(string: str = '', start_text: str = 'Prompt: ', end: str = '\n'):
        print(f'\033[34m{start_text}{string}\033[0m', end=end)

    # 完成
    @staticmethod
    def __success(string: str = '', start_text: str = 'Success: ', end: str = '\n'):
        print(f'\033[32m{start_text}{string}\033[0m', end=end)

    # 模板字符串
    @staticmethod
    def __this_mode(mode):
        mode = mode.lower()
        if mode == 'class_':
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

    def help(self):
        __get_page = "\t\t:param url: 网址"
        __get_ele = ('\t\t:param parent_ele: 在此元素范围内查询\n\t\t'
                     ':param mode_ele: 查询此元素\n\t\t'
                     ':param mode: 查询模式，模式如下\n\t\t\t\t'
                     '① css（默认）：使用css选择器查询\n\t\t\t\t'
                     '② class_：使用类名选择器查询\n\t\t\t\t'
                     '③ id：使用id选择器查询\n\t\t\t\t'
                     '④ xpath：使用xpath路径查询\n\t\t\t\t'
                     '⑤ ele：使用html标签名查询\n\t\t\t\t'
                     '⑥ link：使用完整超链接文本查询（此文本指：<a href="#">这里的文本</a>）\n\t\t\t\t'
                     '⑦ p_link: 使用部分超链接文本查询（此文本指：在link文本的基础上自定义截取的部分文本）\n\t\t'
                     ':param single_duo: 是否启用单元素查询（默认：否）\n:return: 查询结果')
        __get_attr = ('\t\t:param ele: 指定元素\n\t\t'
                      ':param ele_type: 指定属性\n\t\t'
                      ':return: 属性值')
        __driver_quit = '\t\t:param exit_tf: 是否直接退出（默认：是）'
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
        ':param err_msg: 超时信息\n\t\t'
        ':param single_duo: 是否启用多元素查询（默认：否）\n\t\t'
        ':return: 查询结果')
        __Download = ('\t\t:param loadPath: 文件的下载地址\n\t\t'
                      ':param savePath: 文件的保存路径 + 文件名.后缀名')
        __urlCode = '\t\t:param String: 字符串'
        __rUrlCode = '\t\t:param String: url字段'
        __createDir = '\t\t:param dirPath: 文件夹名'
        __js_scroll_page = ('\t\t:param scroll_top_tf: 是否一键滚动到底部（默认：是）\n\t\t'
                            ':param speed: 速度\n\t\t'
                            ':param distance: 距离')
        __position_page = '\t\t:param page_num: 页面序号'
        __driver = 'selenium中的driver（此为变量而非方法）'
        func_list = [['get_page', '获取网页', __get_page], ['get_ele', '查询指定元素范围内的指定元素', __get_ele],
                ['get_attr', '查询指定元素的指定属性', __get_attr], ['driver_quit', '退出操作', __driver_quit], ['js_click','使用js点击元素（可用于元素被遮挡时）', __js_click],
                ['get_wait_ele', '等待查询，等待查询到指定元素后再执行下一步，否则直接退出程序', __get_wait_ele], ['Download', '下载文件', __Download], ['urlCode', '将字符串转为url编码', __urlCode],
                ['rUrlCode', '将url编码解析为字符串', __rUrlCode], ['createDir', '如果文件夹不存在就创建，如果文件存在就清空！' , __createDir], ['js_scroll_page','使用js滚动到指定位置', __js_scroll_page],
                ['position_page', '定位到指定页面', __position_page], ['driver', __driver, '']]
        for func in func_list:
            self.__prompt(func[0], '')
            self.__success(func[1], '\t')
            print(func[2], end='\n\n\n')

    def get_page(self, url: str):
        """
        获取网页
        :param url: 网址
        """
        self.driver.get(url)

    def get_ele(self,parent_ele: WebElement, mode_ele: str, mode: str = 'css', single_duo: bool = False):
        """
        查询指定元素范围内的指定元素
        :param parent_ele: 在此元素范围内查询
        :param mode_ele: 查询此元素
        :param mode: 查询模式，模式如下
                    ① css（默认）：使用css选择器查询
                    ② class_：使用类名选择器查询
                    ③ id：使用id选择器查询
                    ④ xpath：使用xpath路径查询
                    ⑤ ele：使用html标签名查询
                    ⑥ link：使用完整超链接文本查询（此文本指：<a href="#">这里的文本</a>）
                    ⑦ p_link: 使用部分超链接文本查询（此文本指：在link文本的基础上自定义截取的部分文本）
        :param single_duo: 是否启用单元素查询（默认：否）
        :return: 查询结果
        """
        mode = self.__this_mode(mode)
        if single_duo:
            return parent_ele.find_element(eval(f'By.{mode}'), mode_ele)
        else:
            return parent_ele.find_elements(eval(f'By.{mode}'), mode_ele)

    @staticmethod
    def get_attr(ele: WebElement, ele_type: str):
        """
        查询指定元素的指定属性
        :param ele: 指定元素
        :param ele_type: 指定属性
        :return: 属性值
        """
        return ele.get_attribute(ele_type)

    def driver_quit(self, exit_tf: bool = True):
        """
        退出操作
        :param exit_tf: 是否直接退出（默认：是）
        """
        if exit_tf is False:
            input('在此回车退出！')
        self.driver.quit()

    def js_click(self, ele_btn: WebElement):
        """
        使用js点击元素（可用于元素被遮挡时）
        :param ele_btn: 被点击的元素
        """
        self.driver.execute_script('arguments[0].click()', ele_btn)

    def get_wait_ele(self,parent_ele: WebElement, timeout: int = 0, mode: str = 'css', mode_ele: str = None, single_duo: bool = False, err_msg: str = '元素寻找超时！'):
        """
        等待查询，等待查询到指定元素后再执行下一步，否则直接退出程序
        :param parent_ele: 指定元素范围
        :param timeout: 超时时间
        :param mode: 查询模式，模式如下
                    ① css（默认）：使用css选择器查询
                    ② class_：使用类名选择器查询
                    ③ id：使用id选择器查询
                    ④ xpath：使用xpath路径查询
                    ⑤ ele：使用html标签名查询
                    ⑥ link：使用完整超链接文本查询（此文本指：<a href="#">这里的文本</a>）
                    ⑦ p_link: 使用部分超链接文本查询（此文本指：在link文本的基础上自定义截取的部分文本）
        :param mode_ele: 查询元素
        :param err_msg: 超时信息
        :param single_duo: 是否启用多元素查询（默认：否）
        :return: 查询结果
        """
        mode = self.__this_mode(mode)

        ds_str = 'presence_of_element_located'
        if single_duo:
            ds_str = 'presence_of_all_elements_located'
        return WebDriverWait(parent_ele, timeout).until(eval(f'EC.{ds_str}')((eval(f'By.{mode}'), mode_ele)), message=err_msg)

    @staticmethod
    def Download(loadPath: str, savePath: str):
        """
        下载文件
        :param loadPath: 文件的下载地址
        :param savePath: 文件的保存路径 + 文件名.后缀名
        """
        return urlretrieve(loadPath, savePath)

    @staticmethod
    def urlCode(String: str):
        """
        将字符串转为url编码
        :param String: 字符串
        """
        return quote(String)

    @staticmethod
    def rUrlCode(String: str):
        """
        将url编码解析为字符串
        :param String: url字段
        """
        return unquote(String)

    @staticmethod
    def createDir(dirPath: str):
        """
        如果文件夹不存在就创建，如果文件存在就清空！
        :param dirPath: 文件夹名
        """
        if not path.exists(dirPath):
            mkdir(dirPath)
        else:
            rmtree(dirPath)
            mkdir(dirPath)

    def js_scroll_page(self, scroll_top_tf: bool = True, speed: int = 0, distance: int = 0):
        """
        使用js滚动到指定位置
        :param scroll_top_tf: 是否一键滚动到底部（默认：是）
        :param speed: 速度
        :param distance: 距离
        """
        if scroll_top_tf:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        else:
            for i in range(speed):
                self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * distance}')

    def position_page(self, page_num: int = 0):
        """
        定位到指定页面
        :param page_num: 页面序号
        """
        self.driver.switch_to.window(self.driver.window_handles[page_num])

    def __init__(self, driver_path: str = None, headless_tf: bool = False):
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
