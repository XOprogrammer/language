from pymysql import Connection


def MySQL(
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
