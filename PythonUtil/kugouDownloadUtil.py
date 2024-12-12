from os import remove, system, path
from re import search, I
from time import sleep
from urllib.parse import quote

module = []
try:
    from requests import get
except ModuleNotFoundError as e:
    request = search(r"requests", str(e), I).group()
    if request == "requests":
        module.append(request)
try:
    from selenium.webdriver import Chrome
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.expected_conditions import presence_of_element_located as poel
except ModuleNotFoundError as e:
    Selenium = search(r"selenium", str(e), I).group()
    if Selenium == "selenium":
        module.append(Selenium)
if len(module) >= 1:
    for i in module:
        system(f"pip install {i}")
    print("\033[32m成功下载缺失的模块: ", end="")
    for k in module:
        if k == "selenium" and len(module) > 1:
            print("\033[32m, ", end="")
        print(f"\033[32m{k}", end="")
    print("\n")


def version():
    return "v1.0.3"


def kDownload(musicList: list = None, filePath: str = None):
    """
    下载酷狗音乐
    :param musicList: 歌曲列表
    :param filePath: 另存为地址
    :return:
    """
    if type(musicList) == list and type(filePath) == str and path.isdir(filePath) is True:
        if musicList is not None and filePath is not None:
            if len(musicList) >= 1:
                if musicList[0] != "":
                    # 填充
                    print("\033[33m温馨提示[Prompt]: 您的歌曲位中的类型\033[31m必须\033["
                          "33m是字符串类型且不能为空，请勿出现除字符串类型以外的类型或空字符串类型！否则将不会下载该歌曲位中的歌曲！")
                    newList = []
                    for i in musicList:
                        if str(i).strip() != "" and type(i) == str:
                            newList.append(i)
                        else:
                            print("\033[33m警告[Warning]: 检测到为空的字符串(或不为字符串类型的歌曲)！将为您清除违规歌曲, 但不会影响其他歌曲的下载")
                            break
                    filePath = filePath.replace("\\", "/").replace("//", "/")
                    if search(r"/$", filePath) is not None:
                        filePath = filePath[0:-1]
                    failList = []
                    driver = Chrome()
                    driver.get("https://www.kugou.com/?islogout")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]').click()
                    print("\033[33m请在10s内登录!\033[33m")
                    count = 11
                    for j in range(1, 11):
                        count -= 1
                        print(f"剩余登录时间: {count}s")
                        sleep(1)

                    for i in newList:
                        i = str(i)
                        driver.get(
                            f"https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord={quote(i)}")
                        WebDriverWait(driver, 30).until(poel((By.XPATH, '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]')),
                                                        "查找“第一首歌曲”超时")
                        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]').click()
                        driver.switch_to.window(driver.window_handles[-1])
                        WebDriverWait(driver, 30).until(poel((By.ID, 'myAudio')), "查找“audio”超时")
                        WebDriverWait(driver, 30).until(poel((By.CLASS_NAME, 'audioName')),
                                                        "查找“歌曲名”超时")
                        sleep(3)
                        audioName = driver.find_element(By.CLASS_NAME, 'audioName').text
                        print(f"\033[35m正在下载[Download]: {audioName} ...")
                        try:
                            with open(f"{filePath}/{audioName}.mp3", "wb") as music:
                                music.write(get(driver.find_element(By.ID, 'myAudio').get_dom_attribute("src")).content)
                            print(f"\033[32m{audioName}（下载成功）\n")
                        except Exception:
                            print(f"\033[31m{audioName}（下载失败）\n")
                            failList.append(audioName)
                            remove(f"{filePath}/{audioName}.mp3")
                        sleep(3)
                        driver.close()
                        driver.switch_to.window(driver.window_handles[-1])
                    if len(failList) != 0:
                        print("\033[33m本次下载失败名单:")
                        for i in failList:
                            print(f"\t\033[34m{i}")
                    else:
                        print("\033[32m本次无下载失败的歌曲")
                    driver.quit()
                else:
                    print("\033[33m警告[Warning]: 您的第一歌曲位不能为空任何歌曲（list['this is not None', 'xxx', ...]）")
            else:
                print("\033[31m错误[Error]: 您的歌曲列表为空")
        elif musicList is None:
            print("\033[31m错误[Error]: 您未添加歌曲列表(musicList)")
        elif filePath is None:
            print("\033[31m错误[Error]: 您未添加歌曲存储目录(filePath)")
    elif type(musicList) != list:
        print(
            "\033[31m错误[Error]: 您指定的歌曲列表不是数组(列表)类型! 歌曲列表必须为数组(列表)类型! ( type(musicList) != list )")
    elif type(filePath) != str:
        print(
            "\033[31m错误[Error]: 您指定的歌曲存储目录不是字符串类型! 歌曲存储目录必须为字符串类型! ( type(filePath) != str )")
    elif path.isdir(filePath) is False:
        print("\033[31m错误[Error]: 您指定的歌曲存储目录不存在!")
    print("\033[30m")
