try:
    from pymysql import Connection as _Connection
except ModuleNotFoundError:
    print(f'\033[31m未知模块[Error]：pymysql\033[0m')


__version__ = '1.0.0'
__author__ = 'yzmd <a2541507030@163.com>'

__all__ = ['MysqlUtil', 'version']

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

class MysqlUtil:
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

    def connect(self, host: str, database_name: str, port: int, user: str, password: str):
        """
        连接数据库
        :param host: 数据库域名或IP
        :param database_name: 数据库名
        :param port: 端口
        :param user: 用户名
        :param password: 用户密码
        """
        self.__connect = _Connection(
            host=host,
            port=port,
            user=user,
            password=password,
            autocommit=True
        )
        self.__connect.select_db(database_name)
        self.__cursor = self.__connect.cursor()

    def cursor_brush(self, sql_text: str | list):
        """
        执行 SQL 语句
        :param sql_text: sql语句
        """
        def brush(st: str):
            try:
                self.__cursor.execute(st)
                self.__results = self.__cursor.fetchall()
            except Exception as e:
                err: str = str(e)[1:5]
                err_str = str(e)[6:-1]
                if err == "1049":
                    self.__results = f"未知数据库:{err_str}"
                elif err == "2003":
                    self.__results = f"IP或端口错误:{err_str}"
                elif err == "1045":
                    self.__results = f"用户名或密码错误:{err_str}"
                elif err == "1064":
                    self.__results = f"MySQL语法错误:{err_str}"
        if type(sql_text) == str:
            brush(sql_text)
        elif type(sql_text) == list:
            for cb in sql_text:
                brush(cb)
        else:
            self.__err('传递的参数必须为字符串类型（或字典类型）', 'cursor_brush[Error]: ')
        self.__cursor.close()

    def get_results(self):
        """
        获取 sql 语句执行结果
        :return: 执行结果
        """
        return self.__results

    def quit(self):
        """
        关闭数据库连接
        """
        self.__connect.close()

    def insert(self,table_name: str, keys: tuple = None, values: tuple = None, database_name: str = None, other_data: str = None, create: bool = False):
        """
        新增数据
        :param table_name: 表名
        :param keys: 列
        :param values: 值
        :param database_name: 数据库名
        :param other_data: 其他语句
        :param create: 是否开启创建模式
        """
        if other_data is not None: other_data = ' ' + other_data
        if create:
            if database_name is not None:
                self.cursor_brush('create database if not exists %s%s;' % (database_name, other_data))
            else:
                self.cursor_brush('create table %s %s%s;' % (table_name, keys, other_data))
        else:
            self.cursor_brush(f'insert into {table_name} {keys} values %s%s;' % (values, other_data))

    def delete(self, table_name: str, data: str = None, database_name: str = None, other_data: str = None):
        """
        删除数据
        :param table_name: 表名
        :param data: 键值对（如：列名=`值`）
        :param database_name: 数据库名
        :param other_data: 其他语句
        """
        if other_data is not None: other_data = ' ' + other_data
        if database_name is not None: self.cursor_brush('drop database if exists %s%s;' % (database_name, other_data))
        elif data is None: self.cursor_brush('drop table %s%s;' % (table_name, other_data))
        elif data is not None:self.cursor_brush(f'delete from {table_name} where %s%s;' % (data, other_data))

    def update(self, table_name: str, new_data: str = None, old_data: str = None, new_table_name: str = None, other_data: str = None):
        """
        更新数据
        :param table_name: 表名
        :param new_data: 新键值对（如：列名=`值`）
        :param old_data: 修改范围键值对（如：列名>值）
        :param new_table_name: 新表名
        :param other_data: 其他语句
        """
        if other_data is not None: other_data = ' ' + other_data
        if new_table_name is not None:
            self.cursor_brush(f'rename table %s to %s%s;' % (table_name, new_table_name, other_data))
        else:
            self.cursor_brush(f'update {table_name} set %s where %s%s;' % (new_data, old_data, other_data))

    def select(self, table_name: str, query_data: str, from_data: str, other_data: str = None):
        """
        查询数据
        :param table_name: 表名
        :param query_data: 查询键值对（如：列名或count(列名)等）
        :param from_data: 条件键值对（如：列名=`值`）
        :param other_data: 其他语句
        """
        if other_data is not None: other_data = ' ' + other_data
        self.cursor_brush(f'select %s from {table_name} where %s%s;' % (query_data, from_data, other_data))

    @staticmethod
    def grammar_prompt(re_flag: bool = False):
        """
        SQL 语句基础语法提示
        :param re_flag: 是否开启返回值模式
        :return: 语法提示字典集
        """
        grammar = {
            "查询": "select * from 表名 where 1;",
            "插入": "insert into (列名, 列名, ...) values(值, 值, ...);",
            "修改": "update 表名 set 列名=值 where 列名=要修改的值;",
            "删除": "delete from 表名 where 列名=要删除的数据;",
            "创建表": "create table 表名 (列名 数据类型, ...)",
            "删除表": "drop table 表名;",
            "创建数据库": "create database if not exists 数据库名;",
            "删除数据库": "drop database if exists 数据库名;"
        }
        if re_flag:
            return grammar
        for i in grammar:
            print(f'{i}: {grammar[i]}')

    def help(self, get_re: bool = False):
        """
        显示帮助信息
        :param get_re: 是否获取返回值（默认否）
        """
        __help = "\t\t:param get_re: 是否开启返回值模式（默认否）"
        __connect = ("\t\t:param host: 数据库域名或IP"
                     "\n\t\t:param database_name: 数据库名"
                     "\n\t\t:param port: 端口"
                     "\n\t\t:param user: 用户名"
                     "\n\t\t:param password: 用户密码")
        __cursor_brush = "\t\t:param sql_text: sql语句"
        __get_results = '\t\t:return: 执行结果'
        __insert = ("\t\t:param table_name: 表名"
                    "\n\t\t:param keys: 列"
                    "\n\t\t:param values: 值"
                    "\n\t\t:param database_name: 数据库名"
                    "\n\t\t:param other_data: 其他语句"
                    "\n\t\t:param create: 是否开启创建模式")
        __delete = ("\t\t:param table_name: 表名"
                    "\n\t\t:param data: 键值对（如：列名=`值`）"
                    "\n\t\t:param database_name: 数据库名"
                    "\n\t\t:param other_data: 其他语句")
        __update = ("\t\t:param table_name: 表名"
                    "\n\t\t:param new_data: 新键值对（如：列名=`值`）"
                    "\n\t\t:param old_data: 修改范围键值对（如：列名>值）"
                    "\n\t\t:param new_table_name: 新表名"
                    "\n\t\t:param other_data: 其他语句")
        __select = ("\t\t:param table_name: 表名"
                    "\n\t\t:param query_data: 查询键值对（如：列名或count(列名)等）"
                    "\n\t\t:param from_data: 条件键值对（如：列名=`值`）"
                    "\n\t\t:param other_data: 其他语句")
        __grammar_prompt = ("\t\t:param re_flag: 是否开启返回值模式（默认否）"
                            "\n\t\t:return: 语法提示字典集")
        func_list = [
            ['help', '帮助', __help],
            ['connect', '连接数据库', __connect],
            ['cursor_brush', '执行 SQL 语句', __cursor_brush],
            ['get_results', '获取 sql 语句执行结果', __get_results],
            ['quit', '关闭数据库连接', '\t\t无参数'],
            ['insert', '新增数据', __insert],
            ['delete', '删除数据', __delete],
            ['update', '更新数据', __update],
            ['select', '查询数据', __select],
            ['grammar_prompt', 'SQL 语句基础语法提示', __grammar_prompt]
        ]

        if get_re:
            return func_list

        for func in func_list:
            self.__prompt(func[0], '')
            self.__success(func[1], '\t')
            print(func[2], end='\n\n')

    def __init__(self):
        self.__connect = None
        self.__cursor = None
        self.__results = None
