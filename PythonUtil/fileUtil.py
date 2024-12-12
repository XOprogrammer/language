def readFile(address: str, encoding: str):
    """
    读取文件数据
    :param address: 文件地址
    :param encoding: 文件编码格式
    :return: 文件内容
    """
    with open(address, "r", encoding=encoding) as file:
        read = file.read()
        return read


def writeFile(address: str, encoding: str, fileString: str):
    """
    写入并覆盖文件
    :param address: 文件地址（没有则新建）
    :param encoding: 文件编码格式
    :param fileString: 文件内容
    :return: 写入提示
    """
    with open(address, "w", encoding=encoding) as file:
        file.write(fileString)
        return "写入内容成功!"


def appends(address: str, encoding: str, fileString: str):
    """
    追加文件内容
    :param address: 文件地址（没有则新建）
    :param encoding: 文件编码格式
    :param fileString: 文件内容
    :return: 写入提示
    """
    with open(address, "a", encoding=encoding) as file:
        file.write(fileString)
        return "追加内容成功!"
