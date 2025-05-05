from os import remove, path
from re import search
from utils.SeleniumTest import *
from time import sleep
from urllib.parse import quote

module = []

# 版本号
def version() -> str:
    vs = 'v1.0.4'
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

def ku_gou_download(music_list: list = None, file_path: str = None):
    """
    下载酷狗音乐
    :param music_list: 歌曲列表
    :param file_path: 另存为地址
    :return:
    """
    if type(music_list) == list and type(file_path) == str and path.isdir(file_path) is True:
        if music_list is not None and file_path is not None:
            if len(music_list) >= 1:
                if music_list[0] != "":
                    # 填充
                    print("\033[33m温馨提示[Prompt]: 您的歌曲位中的类型\033[31m必须\033["
                          "33m是字符串类型且不能为空，请勿出现除字符串类型以外的类型或空字符串类型！否则将不会下载该歌曲位中的歌曲！")
                    new_list = []
                    for i in music_list:
                        if str(i).strip() != "" and type(i) == str:
                            new_list.append(i)
                        else:
                            print("\033[33m警告[Warning]: 检测到为空的字符串(或不为字符串类型的歌曲)！将为您清除违规歌曲, 但不会影响其他歌曲的下载")
                            break
                    file_path = file_path.replace("\\", "/").replace("//", "/")
                    if search(r"/$", file_path) is not None:
                        file_path = file_path[0:-1]
                    fail_list = []
                    st = SeleniumTest()
                    st.get_page("https://www.kugou.com/?islogout")
                    st.get_wait_ele(st.driver, 30, 'xpath', '/html/body/div[1]/div[1]/div/div[2]/div[2]/div[1]')
                    print("\033[33m请在10s内登录!\033[33m")
                    count = 11
                    for j in range(1, 11):
                        count -= 1
                        print(f"剩余登录时间: {count}s")
                        sleep(1)

                    for i in new_list:
                        i = str(i)
                        st.get_page(f"https://www.kugou.com/yy/html/search.html#searchType=song&searchKeyWord={quote(i)}")
                        st.get_wait_ele(st.driver, 30, 'xpath', '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]', err_msg="查找“第一首歌曲”超时")
                        st.js_click(st.get_ele(st.driver, 'xpath', '/html/body/div[4]/div[1]/div[2]/ul[2]/li[1]'))
                        st.position_page(-1)
                        st.get_wait_ele(st.driver, 30, 'id', 'myAudio', err_msg='查找“audio”超时')
                        st.get_wait_ele(st.driver, 30, 'class', 'audio_name', err_msg="查找“歌曲名”超时")
                        sleep(3)
                        audio_name = st.js_get_text(st.get_ele('class', 'audioName'), True)

                        print(f"\033[35m正在下载[Download]: {audio_name} ...")
                        try:
                            st.download(st.get_attr(st.get_ele(st.driver, 'id', 'myAudio'), 'src'), f"{file_path}/{audio_name}.mp3")
                            print(f"\033[32m{audio_name}（下载成功）\n")
                        except Exception:
                            print(f"\033[31m{audio_name}（下载失败）\n")
                            fail_list.append(audio_name)
                            remove(f"{file_path}/{audio_name}.mp3")
                        sleep(3)
                        st.close()
                        st.position_page(-1)
                    if len(fail_list) != 0:
                        print("\033[33m本次下载失败名单:")
                        for i in fail_list:
                            print(f"\t\033[34m{i}")
                    else:
                        print("\033[32m本次无下载失败的歌曲")
                    st.quit()
                else:
                    print("\033[33m警告[Warning]: 您的第一歌曲位不能为空任何歌曲（list['this is not None', 'xxx', ...]）")
            else:
                print("\033[31m错误[Error]: 您的歌曲列表为空")
        elif music_list is None:
            print("\033[31m错误[Error]: 您未添加歌曲列表(musicList)")
        elif file_path is None:
            print("\033[31m错误[Error]: 您未添加歌曲存储目录(filePath)")
    elif type(music_list) != list:
        print(
            "\033[31m错误[Error]: 您指定的歌曲列表不是数组(列表)类型! 歌曲列表必须为数组(列表)类型! ( type(musicList) != list )")
    elif type(file_path) != str:
        print(
            "\033[31m错误[Error]: 您指定的歌曲存储目录不是字符串类型! 歌曲存储目录必须为字符串类型! ( type(filePath) != str )")
    elif path.isdir(file_path) is False:
        print("\033[31m错误[Error]: 您指定的歌曲存储目录不存在!")
    print("\033[30m")
