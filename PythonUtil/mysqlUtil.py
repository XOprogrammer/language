from pymysql import Connection

__all__ = ['MysqlUtil', 'version']

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

class MysqlUtil:
    @staticmethod
    def mysql(
            host: str,
            database: str,
            port: int,
            user: str,
            password: str,
            sql: str
    ):
        try:
            conn = Connection(
                host=host,
                port=port,
                user=user,
                password=password,
                autocommit=True
            )
            conn.select_db(database)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.close()
            return cursor.fetchall()
        except Exception as e:
            err: str = str(e)[1:5]
            err_str = str(e)[6:-1]
            if err == "1049":
                return f"未知数据库:{err_str}"
            elif err == "2003":
                return f"IP或端口错误:{err_str}"
            elif err == "1045":
                return f"用户名或密码错误:{err_str}"
            elif err == "1064":
                return f"MySQL语法错误:{err_str}"

    @staticmethod
    def help_mysql():
        return {
            "language": "SQL语法提示",
            "查询": "select * from 表名 where 1;",
            "插入": "insert into (列名, 列名, ...) values(值, 值, ...);",
            "修改": "update 表名 set 列名=值 where 列名=要修改的值;",
            "删除": "delete from 表名 where 列名=要删除的数据;",
            "创建表": "create table 表名 (列名 数据类型, ...)",
            "删除表": "drop table 表名;",
            "创建数据库": "create database if not exists 数据库名;",
            "删除数据库": "drop database if exists 数据库名;"
        }
