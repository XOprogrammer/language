from re import search as _src, sub as _sub
from os import path as _path, system as _sys
from importlib.util import find_spec

from tomlkit import (
    document as _document,
    table as _table,
    array as _array,
    dumps as _dumps,
    parse as _parse
)

import tomlkit
from cryptography.fernet import Fernet as _fernet
from PyInstaller.__main__ import run

__version__ = '1.0.0'
__author__ = 'yzmd <a2541507030@163.com>'

__all__ = ['PyBuildUtil', 'version']

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

class PyBuildUtil:
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

    def init_config(self, project_name: str, version_: str = '1.0.0', description: str = '暂无描述...',
                    is_production: bool = False, debug_mode: bool = False):
        """
        基础配置
        :param project_name: 项目名称
        :param version_: 项目版本号（默认1.0.0）
        :param description: 描述文段（默认暂无）
        :param is_production: 是否为生产环境配置（默认否）
        :param debug_mode: 是否弃用调试模式（默认否）
        :return:
        """
        self.__project_name = project_name
        self.__doc.add('project_name', project_name)
        self.__doc.add('version', version_)
        self.__doc.add('description', description)
        self.__doc.add('is_production', is_production)
        self.__doc.add('debug_mode', debug_mode)

    def authors_config(self, author: str, email: str, organization: str = '暂无...', *args):
        """
        作者&维护者信息
        :param author: 作者姓名
        :param email: 电子邮箱
        :param organization: 所属组织
        :param args: 贡献者（格式：{'name': '贡献者名', 'role': '职能'}, {...}, ...）
        """

        authors = _table()

        authors.add('maintainer', {
            'name': author,
            'email': email,
            'organization': organization
        })

        contributors = _array()
        for i in args:
            if len(i) == 2 and 'name' in i and 'role' in i:
                contributors.append(i)
        authors.add('contributors', contributors)

        self.__doc.add('authors', authors)

    def deps_config(self, required: list, optional: dict = None, development: list = None):
        """
        依赖配置
        :param required: 必需依赖
        :param optional: 可选依赖
        :param development: 开发依赖
        """
        dependencies = _table()
        dependencies.add('required', required)
        if optional is not None: dependencies.add('optional', optional)
        if development is not None: dependencies.add('development', development)
        self.__doc.add('dependencies', dependencies)


    def database_config(self, host: str, port: int, database_name: str, username: str,
                        password: str, pool_size: int = 10, timeout: float | int = 30,
                        slave_enabled: bool = False, slave_host: str = None, slave_port: int = None):
        """
        数据库配置
        :param host: 数据库 域名/IP
        :param port: 数据库端口
        :param database_name: 数据库名称
        :param username: 数据库用户名
        :param password: 数据库密码
        :param pool_size: 连接池大小（默认：10）
        :param timeout: 连接超时时间（单位：秒，默认：30）
        :param slave_enabled: 是否启用从库（默认否）
        :param slave_host: 从库 域名/IP
        :param slave_port: 从库端口
        """
        database = _table()

        database.add('primary', {
            'host': host,
            'port': port,
            'name': database_name,
            'credentials': {
                'username': username,
                'password': password
            },
            'pool_size': pool_size,
            'timeout': timeout
        })

        if slave_enabled:
            if slave_host is not None and type(slave_host) == str:
                if slave_port is not None and type(slave_port) == int:
                    database.add('replica', {
                        'host': slave_host,
                        'port': slave_port,
                        'enabled': True
                    })
                else:
                    self.__err(f'从库 端口 配置错误！')
            else:
                self.__err(f'从库 域名/IP 配置错误！', 'database_config[Error]: ')

        self.__doc.add('database', database)

    def services_config(self, host: str, port: int, ssl_enabled: bool, cert_file: str = None,
                        key_file: str = None, allowed_origins: list = None, allowed_methods: list = None,
                        allowed_headers: list = None, exposed_headers: list = None, allow_credentials: bool = False,
                        max_age: int = 10, temp_type: str = None, temp_host: str = None, temp_port: int = None,
                        temp_ttl: int = 3600):
        """
        服务配置
        :param host: 域名/IP
        :param port: 端口
        :param ssl_enabled: 是否启用 SSL
        :param cert_file: 证书文件路径
        :param key_file: 私钥文件路径
        :param allowed_origins: 允许的跨域来源
        :param allowed_methods: 允许的HTTP方法（默认：常见REST方法）
        :param allowed_headers: 允许的请求头（默认：基础请求头）
        :param exposed_headers: 暴露的响应头
        :param allow_credentials: 是否允许凭据（默认否）
        :param max_age: 预检请求缓存时间（秒）
        :param temp_type: 缓存类型
        :param temp_host: 缓存 域名/IP
        :param temp_port: 缓存端口
        :param temp_ttl: 缓存时间（单位：秒，默认：3600）
        """

        services = _table()
        web_service = {
            'host': host,
            'port': port,
            'cors': {
                'allowed_origins': allowed_origins or [],
                'allowed_methods': allowed_methods or ['POST', 'GET', 'PUT', 'DELETE'],
                'allowed_headers': allowed_headers or ["Content-Type", "Authorization"],
                'exposed_headers': exposed_headers or ["X-API-Version"],
                'allow_credentials': allow_credentials,
                'max_age': max_age
            }
        }

        if ssl_enabled:
            if cert_file is not None:
                if key_file is not None:
                    web_service['ssl'] = {
                        'enabled': True,
                        'cert_file': cert_file,
                        'key_file': key_file
                    }
                else:
                    self.__err('密匙文件路径（key_file）错误！', 'services_config[Error]: ')
            else:
                self.__err('证书文件路径（cert_file参数）错误！', 'services_config[Error]: ')

        services.add('web', web_service)

        if temp_type is not None:
            services.add('cache', {
                'type': temp_type,
                'host': temp_host,
                'port': temp_port,
                'ttl': temp_ttl
            })

        self.__doc.add('services', services)

    def set_interval_config(self, *args):
        """
        定时任务配置
        :param args: 任务配置元组（如：{'name': '任务名', 'schedule': 'cron表达式', 'command': '执行的命令'}, {...}, ...）
        标准格式为：{
            'name': '任务名',(必填)
            'description': '任务描述',
            'schedule': 'cron表达式',(必填)
            'command': '执行的命令'(必填)
        }
        """
        scheduled_tasks = _array()
        for i in args:
            if 4 >= len(i) >= 3:
                if 'name' in i and 'command' in i and 'schedule' in i:
                    task = dict()
                    task.update(i)
                    scheduled_tasks.append(task)
        self.__doc.add('scheduled_tasks', scheduled_tasks)

    def advanced_config(self, max_threads: int, cache_size: str, zip_enabled: bool = False,
                        zip_level: int = 6, default_lang: str = 'zh-CN', supported_lang: list = None,
                        fallback_lang: str = 'en-US', new_parser: bool = False, beta_features: list = None):
        """
        高级特性配置
        :param max_threads:最大线程数
        :param cache_size: 缓存大小（如：1GB）
        :param zip_enabled: 是否压缩（默认否）
        :param zip_level: 压缩级别（范围：1~9，默认：6）
        :param default_lang: 默认语言（默认：zh-CN）
        :param supported_lang: 支持的语言（默认：[]）
        :param fallback_lang: 回退语言（默认：en-US）
        :param new_parser: 是否启用新解释器（默认否）
        :param beta_features: 启用的beta功能列表（默认：[]）
        """
        advanced = _table()
        if zip_enabled:
            if zip_level > 9:
                zip_level = 9
            elif zip_level < 1:
                zip_level = 1
        advanced.add('performance', {
            'max_threads': max_threads,
            'cache_size': cache_size,
            'compression': {
                'enabled': zip_enabled,
                'level': zip_level
            }
        })

        if supported_lang is None: supported_lang = list()
        advanced.add('i18n', {
            'default_lang': default_lang,
            'supported_lang': supported_lang,
            'fallback': fallback_lang
        })

        if beta_features is None: beta_features = list()
        advanced.add('experimental', {
            'new_parser': new_parser,
            'beta_features': beta_features
        })

        self.__doc.add('advanced', advanced)

    def add_customize_config(self, table_name: str = None, **kwargs):
        """
        动态生成自定义配置
        :param table_name: 是否以表格生成配置（不设置表名则为否）
        :param kwargs: 配置键值对（如：a='b'）
        """
        tn = None
        if table_name is not None:
            tn = _table()
        for i in kwargs:
            if table_name is not None:
                tn.add(str(i), kwargs[i])
            else:
                self.__doc.add(str(i), kwargs[i])
        if table_name is not None:
            self.__doc.add(table_name, tn)

    def create_config_file(self, save_path: str = './', encryption: bool = False):
        """
        生成TOML配置文件（自动使用项目名称命名）
        :param save_path: 保存路径（默认：./）
        :param encryption: 是否加密（默认否）
        """
        toml_content = _dumps(self.__doc)
        if _src(r'/$|\\$', save_path) is None:
            save_path += '/'
        else:
            save_path = _sub(r'/*\\*', '', save_path) + '/'

        __pn = ''
        if self.__project_name != '':
            __pn = f'{self.__project_name}_'
        else:
            self.__warn('未配置“init_config”（基础配置）', '未知项目[Warning]: ')
        try:
            with open(f'{save_path}{__pn}config.toml', 'w', encoding='UTF-8') as toml:
                toml.write(toml_content)
            self.__success(f'“{self.__project_name}”配置文件生成成功：{save_path}{__pn}config.toml')
            self.__toml_file = f'{save_path}{__pn}config.toml'
        except Exception:
            self.__warn(f'项目名称“{self.__project_name}”非法，已改用原始名称“config”！',
                        'create_config_file[Warning]: ')
            with open(f'{save_path}config.toml', 'w', encoding='UTF-8') as toml:
                toml.write(toml_content)
            self.__success(f'“{self.__project_name}”配置文件生成成功：{save_path}config.toml')
            self.__toml_file = f'{save_path}config.toml'

        if encryption:
            # self.__encryption(self.__toml_file, )
            key = _fernet.generate_key()
            cipher_suite = _fernet(key)

            enc_path = _path.splitext(self.__toml_file)[0] + '.enc'
            key_path = _path.splitext(self.__toml_file)[0] + '.key'

            with open(self.__toml_file, 'rb') as f:
                encrypted = cipher_suite.encrypt(f.read())
            with open(enc_path, 'wb') as f:
                f.write(encrypted)
            self.__success(f'“{self.__project_name}”加密配置文件生成成功：{enc_path}')
            with open(key_path, 'wb') as f:
                f.write(key)
            self.__success(f'“{self.__project_name}”密匙文件生成成功：{key_path}')

    def builder(self, py_file: str, add_file: str = None, name: str = None,
                icon: str = None, dir_or_file: bool = True, force_contain_tomlkit: bool = False,
                add_module_src_paths: str = None, temp_file_path: str = None, clear_temp: bool = True,
                upx_path: str = None, save_path: str = './'):
        """
        打包 python 程序
        :param py_file: py文件
        :param add_file: 添加其他文件（如：'a.txt;b.png;c.pdf'）
        :param name: 程序名称（默认空）
        :param icon: 程序图标（默认空）
        :param dir_or_file: 打包为单文件或文件夹（默认：打包为文件夹，值：True）
        :param force_contain_tomlkit: 强制包含 TOML 解析库（默认：否）
        :param add_module_src_paths: 添加模块搜索路径（默认空）
        :param temp_file_path: 临时文件目录（默认空）
        :param clear_temp: 清理缓存后打包（默认是）
        :param upx_path: 使用 UPX 压缩（默认空）
        :param save_path: 打包文件保存路径
        """
        if _src(r'/$|\\$', save_path) is None:
            save_path += '/'
        else:
            save_path = _sub(r'/*\\*', '', save_path) + '/'
        build_join = [py_file]

        if name is not None: build_join.append(f'--name={name}')
        if icon is not None: build_join.append(f'--icon={icon}')
        if save_path is not None: build_join.append(f'--distpath={save_path}')
        if dir_or_file: build_join.append('--onefile')
        else: build_join.append('--onedir')
        if force_contain_tomlkit: build_join.append('--hidden-import=tomlkit')
        if add_module_src_paths is not None: build_join.append(f'--paths={add_module_src_paths}')
        if temp_file_path is not None: build_join.append(f'--runtime-tmpdir={temp_file_path}')
        if clear_temp: build_join.append('--clean')
        if upx_path is not None: build_join.append(f'--upx-dir={upx_path}')
        if add_file is not None or self.__toml_file != '':
            if add_file is None: build_join.append(f'--add-data={self.__toml_file};.')
            else: build_join.append(f'--add-data={add_file};.')

        run(build_join)

    def help(self, get_re: bool = False):
        """
        显示帮助信息
        :param get_re: 是否获取返回值（默认否）
        """
        __help = "\t\t:param get_re: 是否获取返回值（默认否）"
        __init_config = ("\t\t:param project_name: 项目名称（必填）"
                         "\n\t\t:param version_: 项目版本号（默认'1.0.0'）"
                         "\n\t\t:param description: 项目描述（默认'暂无描述...'）"
                         "\n\t\t:param is_production: 是否为生产环境（默认False）"
                         "\n\t\t:param debug_mode: 是否启用调试模式（默认False）")
        __authors_config = ("\t\t:param author: 主维护者姓名（必填）"
                            "\n\t\t:param email: 主维护者邮箱（必填）"
                            "\n\t\t:param organization: 所属组织（默认'暂无...'）"
                            "\n\t\t:param args: 贡献者信息（格式：{'name':'姓名','role':'角色'}, ...）")
        __deps_config = ("\t\t:param required: 必需依赖列表（如['flask>=2.0']）"
                         "\n\t\t:param optional: 可选依赖字典（如{'redis':'缓存支持'}）"
                         "\n\t\t:param development: 开发依赖列表（如['pytest']）")
        __database_config = ("\t\t:param host: 主库域名/IP（必填）"
                             "\n\t\t:param port: 主库端口（必填）"
                             "\n\t\t:param database_name: 数据库名（必填）"
                             "\n\t\t:param username: 用户名（必填）"
                             "\n\t\t:param password: 密码（必填）"
                             "\n\t\t:param pool_size: 连接池大小（默认10）"
                             "\n\t\t:param timeout: 连接超时秒数（默认30）"
                             "\n\t\t:param slave_enabled: 是否启用从库（默认False）"
                             "\n\t\t:param slave_host: 从库域名/IP"
                             "\n\t\t:param slave_port: 从库端口")
        __services_config = ("\t\t:param host: 服务域名/IP（必填）"
                             "\n\t\t:param port: 服务端口（必填）"
                             "\n\t\t:param ssl_enabled: 是否启用SSL（必填）"
                             "\n\t\t:param cert_file: SSL证书路径（必填）"
                             "\n\t\t:param key_file: SSL私钥路径（必填）"
                             "\n\t\t:param allowed_origins: 允许的跨域来源列表"
                             "\n\t\t:param max_age: 预检请求缓存秒数"
                             "\n\t\t:param temp_type: 缓存类型（如'redis'）"
                             "\n\t\t:param temp_host: 缓存服务域名/IP"
                             "\n\t\t:param temp_port: 缓存服务端口"
                             "\n\t\t:param temp_ttl: 缓存时间秒数（默认3600）")
        __set_interval_config = ("\t\t:param args: 任务配置元组（如：{'name': '任务名', 'schedule': 'cron表达式', 'command': '执行的命令'}, {...}, ...）"
                                 "\n\t\t标准格式为：{"
                                 "\n\t\t\t'name': '任务名',(必填)"
                                 "\n\t\t\t'description': '任务描述',"
                                 "\n\t\t\t'schedule': 'cron表达式',(必填)"
                                 "\n\t\t\t'command': '执行的命令'(必填)"
                                 "\n\t\t}")
        __advanced_config = ("\t\t:param max_threads: 最大线程数"
                             "\n\t\t:param cache_size: 缓存大小（如'512MB'）"
                             "\n\t\t:param zip_enabled: 是否启用压缩（默认False）"
                             "\n\t\t:param zip_level: 压缩级别1-9（默认6）"
                             "\n\t\t:param default_lang: 默认语言（默认'zh-CN'）"
                             "\n\t\t:param supported_lang: 支持语言列表"
                             "\n\t\t:param fallback_lang: 回退语言（默认'en-US'）"
                             "\n\t\t:param new_parser: 是否启用新解析器（默认False）"
                             "\n\t\t:param beta_features: Beta功能列表")
        __add_customize_config = ("\t\t:param table_name: 是否以表格生成配置（不设置表名则为否）"
                                  "\n\t\t:param kwargs: 配置键值对（如：a='b'）")
        __create_config_file = ("\t\t:param save_path: 保存路径（默认：./）"
                                "\n\t\t:param encryption: 是否加密（默认否）")
        __builder = ("\t\t:param py_file: py文件（必填）"
                     "\n\t\t:param toml_file: 添加其他文件（如：'a.txt;b.png;c.pdf'）"
                     "\n\t\t:param name: 程序名称（默认空）"
                     "\n\t\t:param icon: 程序图标（默认空）"
                     "\n\t\t:param dir_or_file: 打包为单文件或文件夹（默认：打包为文件夹，值：True）"
                     "\n\t\t:param force_contain_tomlkit: 强制包含 TOML 解析库（默认：否）"
                     "\n\t\t:param add_module_src_paths: 添加模块搜索路径（默认空）"
                     "\n\t\t:param temp_file_path: 临时文件目录（默认空）"
                     "\n\t\t:param clear_temp: 清理缓存后打包（默认是）"
                     "\n\t\t:param upx_path: 使用 UPX 压缩（默认空）"
                     "\n\t\t:param save_path: 打包文件保存路径")

        func_list = [
            ['help', '显示帮助信息', __help],
            ['init_config', '基础配置', __init_config],
            ['authors_config', '作者配置', __authors_config],
            ['deps_config', '依赖配置', __deps_config],
            ['database_config', '数据库配置', __database_config],
            ['services_config', '服务配置', __services_config],
            ['set_interval_config', '定时任务', __set_interval_config],
            ['advanced_config', '高级配置', __advanced_config],
            ['add_customize_config', '动态生成自定义配置', __add_customize_config],
            ['create_config_file', '生成TOML配置文件（自动使用项目名称命名）', __create_config_file],
            ['builder', '打包 python 程序', __builder]
        ]

        if get_re:
            return func_list

        for func in func_list:
            self.__prompt(func[0], '')
            self.__success(func[1], '\t')
            print(func[2], end='\n\n')

    def __init__(self):
        self.__doc = _document()
        self.__project_name = ''
        self.__toml_file = ''
        self.__services = None
