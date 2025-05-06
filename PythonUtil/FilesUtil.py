from os import system, remove, path, makedirs, walk, removedirs, rename
from shutil import move, rmtree
from pathlib import Path
from re import *

__version__ = '1.0.0'
__author__ = 'yzmd <a2541507030@163.com>'
__all__ = ['FilesUtil', 'version']

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

class FilesUtil:
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

    @staticmethod
    def __create_arr_item(pd_item: list, create_item: list) -> list:
        if len(pd_item) > len(create_item):
            for i in range(len(create_item), len(pd_item)):
                create_item.append(create_item[-1])
        return [create_item[-1] if item == '' else item for item in create_item]


    # 帮助文档
    def help(self, get_text:str = None) -> dict:
        __merge_files = ('files_list(list): 文件路径\n\t\t'
                         'files_encode(str): 文件编解码\n\t\t'
                         'save_file(str): 文件保存路径(默认：当前执行路径/merge_files.文件后缀)\n\t\t'
                         'del_source_file(bool): 是否删除源文件(默认否)')
        __merge_files_b = ('files_list(list): 文件路径\n\t\t'
                         'save_file(str): 文件保存路径(默认：当前执行路径/merge_files.文件后缀)\n\t\t'
                         'del_source_file(bool): 是否删除源文件(默认否)')
        __split_file = ('files_list(list|str): 文件路径\n\t\t'
                        'segmentation(list|str): 分割标志\n\t\t'
                        'files_encode(list|str): 编解码\n\t\t'
                        'save_file_list(list|str): 保存路径\n\t\t'
                        'del_source_file(bool): 是否删除源文件(默认否)')
        __migration_files = ('files_path(list|str): 文件路径\n\t\t'
                             'directory_path(list|str): 目录路径')
        __copy_files = ('files_path(list|str): 文件路径\n\t\t'
                        'files_encode(list|str): 编解码\n\t\t'
                        'rename(list|str): 重命名复制文件')
        __create_dir = 'dir_name(list|str): 目录名'
        __rename_files = ('old_files_list(list|str): 旧文件名（可带地址）\n\t\t'
                          'new_files_list(list|str): 新文件名\n\t\t'
                          'name_lr(list|str): 文件名前后缀')
        __del_files_dir = ('f_d_path(list|str): 文件(或目录)路径\n\t\t'
                           'force_del_dir(bool): 是否强制删除目录(默认否)')
        __content_view = ("files_path(list|str): 文件路径"
                          "file_encode(list|str): 读解码")
        __usort = ("arr(list): 需要排序的数组\n\t\t"
                   "idx(list): 排序数组时的参考数组\n\t\t"
                   "lr(bool): 升降序（默认：降序False）")
        __open_files_dirs = 'files_path(list|str): 文件(或目录)路径'
        __query_files = ('files_path(list|str): 文件(或目录)路径\n\t\t'
                         'all_files(bool): 是否查询包括子目录内的所有文件(默认否)\n\t\t'
                         'lr(bool): 正反排序(默认正序：false)')
        __query_files_p = 'directory(str): 目录路径'

        def h_prompt(string):
            return f'\033[34m{string}\033[0m'
        help_text = {
            'version': {
                'title': 'version',
                'message': h_prompt('查看 FilesUtil 版本号'),
                'must': False
            },
            'merge_files': {
                'title': 'merge_files',
                'message': h_prompt('合并文件'),
                'join': __merge_files,
                'must': False
            },
            'merge_files_b': {
                'title': 'merge_files_b',
                'message': h_prompt('合并文件(二进制版)'),
                'join': __merge_files_b,
                'must': False
            },
            'split_file': {
                'title': 'split_file',
                'message': h_prompt('拆分文件'),
                'join': __split_file,
                'must': False
            },
            'migration_files': {
                'title': 'migration_files',
                'message': h_prompt('迁移文件'),
                'join': __migration_files,
                'must': False
            },
            'copy_files': {
                'title': 'copy_files',
                'message': h_prompt('复制文件'),
                'join': __copy_files,
                'must': False
            },
            'create_dir': {
                'title': 'create_dir',
                'message': h_prompt('创建目录'),
                'join': __create_dir,
                'must': False
            },
            'rename_files': {
                'title': 'rename_files',
                'message': h_prompt('文件重命名'),
                'join': __rename_files,
                'must': False
            },
            'del_files_dir': {
                'title': 'del_files_dir',
                'message': h_prompt('删除文件或目录'),
                'join': __del_files_dir,
                'must': False
            },
            'content_view': {
                'title': 'content_view',
                'message': h_prompt('文件内容预览'),
                'join': __content_view,
                'must': False
            },
            'usort': {
                'title': 'usort',
                'message': h_prompt('数组排序'),
                'join': __usort,
                'must': False
            },
            'open_files_dirs': {
                'title': 'open_files_dirs',
                'message': h_prompt('打开文件或目录'),
                'join': __open_files_dirs,
                'must': False
            },
            'query_files': {
                'title': 'query_files',
                'message': h_prompt('查询指定目录下的所有文件'),
                'join': __query_files,
                'must': False
            },
            'query_files_p': {
                'title': 'query_files_p',
                'message': h_prompt('查询指定目录下的所有文件'),
                'join': __query_files_p,
                'must': False
            }
        }
        if get_text is not None:
            return help_text[get_text]
        for ht in help_text:
            self.__success(ht, '', end='\t\t\n')
            for ht2 in help_text[ht]:
                if ht2 != 'title':
                    print(f'\t\t{help_text[ht][ht2]}')
            if ht != 'save_write_all':
                print('\n')
        return help_text

    # 文件合并(一维合并未进阶二维合并)
    def merge_files(self, files_list: list = None, files_encode: str = 'utf-8', save_file: str = 'merge_files', del_source_file: bool = False):
        __files_list_type = type(files_list)
        if __files_list_type == list and files_list is not None and len(files_list) >= 2:
            
            readlines = ''
            if search(self.__files_path_re, save_file) is None:
                save_file += f"{search(self.__files_path_re, files_list[-1]).group(3)}"
            for i in files_list:
                try:
                    with open(i, 'r', encoding=files_encode) as r_merge:
                        readlines += f'{r_merge.read()}\n'
                    if del_source_file:
                        remove(i)
                except UnicodeDecodeError:
                    self.__err(f'“{files_encode}”编解码器解码失败！请检查文件编码和所有文件编码是否一致！', 'merge_files[Error]: ')
                    return
                except FileNotFoundError:
                    self.__err(f'文件“{i}”不存在！', 'merge_files[Error]: ')
                    return

            with open(save_file, 'w', encoding=files_encode) as w_merge:
                w_merge.write(readlines)
                self.__success(f'文件合并成功！（共合并 {len(files_list)} 个文件）', 'merge_files[success]: ')
        else:
            self.__err(f'请以列表类型传入文件路径至少两个及以上！', 'merge_files[success]: ')

    # 文件合并：二进制版(一维合并未进阶二维合并)
    def merge_files_b(self, files_list: list = None, save_file: str = 'merge_files',del_source_file: bool = False):
        __files_list_type = type(files_list)
        if __files_list_type == list and files_list is not None and len(files_list) >= 2:
            if search(self.__files_path_re, save_file) is None:
                save_file += f"{search(self.__files_path_re, files_list[-1]).group(3)}"
            for i in files_list:
                try:
                    with open(i, 'rb') as r_merge:
                        readall = r_merge.read()
                        with open(save_file, 'ab') as w_merge:
                            w_merge.write(readall)
                    if del_source_file:
                        remove(i)
                except FileNotFoundError:
                    self.__err(f'文件“{i}”不存在！', 'merge_files[Error]: ')
                    return
            self.__success(f'文件合并成功！（共合并 {len(files_list)} 个文件）', 'merge_files[success]: ')
        else:
            self.__err(f'请以列表类型传入文件路径至少两个及以上！', 'merge_files[success]: ')

    # 文件拆分
    def split_files(self, files_list: list|str = None, segmentation: list|str = '', files_encode: list|str = 'utf-8', save_file_list: list|str = 'split', del_source_file: bool = False):
        def str_rep_t(string):
            return (string.replace('\\', '\\\\')
                    .replace('\n', '\\n')
                    .replace('+', '\\+')
                    .replace('.', '\\.'))
        def str_rep_f(string):
            return (string.replace('\\\\', '\\')
                    .replace('\\n', '\n')
                    .replace('\\+', '+')
                    .replace('\\.', '.'))
        def legitimate_name_pd(string) -> bool:
            pd1 = search(r'^[a-zA-Z]:.*', string)
            pd2 = search(r'[:*?"<>|]', string)
            if pd1 and string.count(':') >= 2:
                self.__err(f'文件(或目录)名不合法！(来自文件“{string}”)', 'split_file[Error]: ')
                return False
            elif pd1 is None and pd2 is not None:
                self.__err(f'文件(或目录)名不合法！(来自文件“{string}”)', 'split_file[Error]: ')
                return False
            return True

        __files_list_type = type(files_list)
        __segmentation_type = type(segmentation)
        __files_encode_type = type(files_encode)
        __save_file_list_type = type(save_file_list)

        def single_split_file(file_path, file_encode, split_this, save_file_path) -> bool:
            
            if search(r'\..*$', save_file_path) is None:
                save_file_path += '.txt'
            elif search(r'\.$', save_file_path) is not None:
                save_file_path += 'txt'
            try:
                with open(file_path, 'r', encoding=file_encode) as r_split:
                    try:
                        readlines = r_split.readlines()
                    except UnicodeDecodeError:
                        self.__err(f'“{files_encode}”编解码器无法解码！', 'split_file[Error]: ')
                        return False
                    text_list = findall(rf'(.*?)({split_this}\\n)', str_rep_t(sub(r'[\n\r]+$', '', ''.join(readlines))),
                                        S)
                    file_last = search(rf'{split_this}\\n(.*?)({split_this}$)',
                                       str_rep_t(sub(r'[\n\r]+$', '', ''.join(readlines))), S)
                    text_list.append((file_last.group(1), file_last.group(2)))
                    if len(text_list) > 1:
                        savefile = search(self.__files_path_re, save_file_path)
                        if savefile is not None:
                            if not legitimate_name_pd(savefile.group(1)):
                                return False
                            save_file_path = sub(rf'{savefile.group(3)}$', '', save_file_path)
                            if not legitimate_name_pd(save_file_path):
                                return False
                        else:
                            self.__err(f'文件(或目录)名不合法！(来自文件“{save_file_path}”)', 'split_file[Error]: ')
                            return False
                        for cf in text_list:
                            with open(
                                    f'{save_file_path}_{text_list.index(cf) + 1}{search(self.__files_path_re, file_path).group(3)}',
                                    'w', encoding=file_encode) as w_split:
                                w_split.write(str_rep_f(f'{cf[0].lstrip('\\n')}{cf[1].rstrip('\\n')}'))
                        return True
                    elif len(text_list) == 1:
                        self.__err(f'文件“{file_path}”拆分后仍是本文件！(自动取消拆分)', 'split_file[Error]: ')
                        return False
                    else:
                        self.__err(f'文件“{file_path}”拆分失败！', 'split_file[Error]: ')
                        return False
            except FileNotFoundError as e:
                fd = search('directory: \'(.*?)\'', str(e))
                self.__err(fd.group(1), 'split_file[没有这样的文件或目录]: ')
                return False

        if files_list:
            if __files_list_type == str:
                self.__prompt('当前为单文件拆分...', 'split_file[Prompt]: ')
                if __segmentation_type != str or __files_encode_type != str or __save_file_list_type != str:
                    self.__err('所有参数应统一使用字符串类型传递方式！(除了 del_source_file 使用布尔类型)', 'split_file[Error]: ')
                else:
                    if single_split_file(files_list, files_encode, segmentation, save_file_list):
                        self.__success(f'文件“{files_list}”拆分成功！', 'split_file[success]: ')
                    if del_source_file:
                        remove(files_list)
            elif __files_list_type == list:
                self.__prompt('当前为多文件拆分...', 'split_file[Prompt]: ')
                if __segmentation_type != list or __files_encode_type != list or __save_file_list_type != list:
                    self.__err('所有参数应统一使用列表类型传递方式！(除了 del_source_file 使用布尔类型)', 'split_file[Error]: ')
                else:
                    segmentation = self.__create_arr_item(files_list, segmentation)
                    files_encode = self.__create_arr_item(files_list, files_encode)
                    save_file_list = self.__create_arr_item(files_list, save_file_list)
                    if len(files_list) == len(segmentation) == len(files_encode) == len(save_file_list):
                        for i in files_list:
                            index = files_list.index(i)
                            single_split_file(i, files_encode[index], segmentation[index], save_file_list[index])
                            if del_source_file:
                                remove(i)
                        self.__success(f'文件拆分成功！（共拆分 {len(files_list)} 个文件）', 'split_file[success]: ')
                    else:
                        self.__err(f'传入参数不足，拆分失败！（自动退出拆分）', 'split_file[Error]: ')
                        return
            else:
                self.__err('文件路径填入类型错误！应为字符串类型或列表类型', 'split_file[Error]: ')
        else:
            self.__err('未指定文件路径！', 'split_file[Error]: ')

    # 文件迁移
    def migration_files(self, files_path: list|str, directory_path: list|str):
        def migration(dir, file):
            if path.isabs(dir) and path.isabs(file):
                try:
                    self.__call_create_dir = False
                    self.create_dir(dir)
                    f_nt = search(self.__files_path_re, file)
                    move(file, f'{dir}/{f_nt.group(2)}{f_nt.group(3)}')
                    self.__success(f'成功将文件“{file}”迁移到目录“{dir}”')
                except OSError:
                    self.__err(f'文件(或目录)“{file}”不存在！', 'copy_file[Error]: ')
            else:
                self.__err('请使用绝对路径！', 'migration_file[Error]: ')
                # print(path.dirname(__file__).replace('\\', '/'))

        __files_path_type = type(files_path)
        __directory_path_type = type(directory_path)

        if __files_path_type == str and __directory_path_type == str:
            migration(directory_path, files_path)
            self.__call_create_dir = True
        elif __files_path_type == list and __directory_path_type == list:
            for i in files_path:
                migration(directory_path[files_path.index(i)], i)
            self.__call_create_dir = True
        else:
            self.__err('请统一使用列表类型或字符串类型填入参数', 'migration_file[Error]: ')

    # 文件复制
    def copy_files(self, files_path: list|str, files_encode: list|str = 'utf-8', rename: list|str = ''):
        def copy(f_path, f_encode, f_ren = '', f_id = 1):
            
            f_ntp = search(self.__files_path_re, f_path)
            f_re_ntp = search(self.__files_path_re, f_ren)
            try:
                with open(f_path, 'r', encoding=f_encode) as cpr:
                    copy_read = cpr.read()
                    if f_ren == '':
                        copy_path = f'{f_ntp.group(2)}_copy'
                    else:
                        copy_path = f'{f_re_ntp.group(2)}'
            except FileNotFoundError:
                self.__err(f'文件(或目录)“{f_path}”不存在！', 'copy_file[Error]: ')
                return
            except AttributeError:
                copy_path = f_ren
                f_re_ntp = f_ntp
            except UnicodeDecodeError:
                if __files_encode_type == str:
                    self.__err(f'“{f_encode}”编解码器无法解码！',  'copy_file[Error]: ')
                else:
                    self.__err(f'“{f_encode}”编解码器无法解码！(在“files_encode”列表的第 {f_id} 个元素)',
                               'copy_file[Error]: ')
                return
            except OSError:
                self.__err(f'文件(或目录)“{f_path}”不存在！', 'copy_file[Error]: ')
                return

            if f_re_ntp is None:
                f_re_ntp = f_ntp
            new_path = f'{f_re_ntp.group(1)}{copy_path}{f_ntp.group(3)}'
            if str(f_ntp.group()) == new_path:
                copy_path = f'{f_ntp.group(2)}_copy'
            with open(f'{f_re_ntp.group(1)}{copy_path}{f_ntp.group(3)}', 'w', encoding=f_encode) as cpw:
                cpw.write(copy_read)
            self.__success(f'成功复制文件“{f_path}”到“{sub(r'/$', '', f_re_ntp.group(1))}”！(文件名为: {copy_path}{f_re_ntp.group(3)})')
        __files_path_type = type(files_path)
        __files_encode_type = type(files_encode)
        __rename_type = type(rename)
        if __files_path_type == str and __files_encode_type == str and __rename_type == str:
            copy(files_path, files_encode, rename)
        elif __files_path_type == list and __files_encode_type == list and __rename_type == list:
            files_encode = self.__create_arr_item(files_path, files_encode)
            for i in files_path:
                index = files_path.index(i)
                files_encode_n = None
                try:
                    files_encode_n = files_encode[index]
                    rename_n = rename[index]
                except IndexError:
                    if len(files_path) != len(files_encode):
                        self.__err(f'各列表元素数量必须相同，除了最后一个列表！(文件“{i}”复制失败)', 'copy_file[Error]: ')
                        return
                    else:
                        rename_n = ''
                copy(i, files_encode_n, rename_n, index + 1)
        else:
            self.__err('参数填入类型应统一为列表类型或字符串类型！', 'copy_file[Error]: ')

    # 创建目录
    def create_dir(self, dir_name: list|str = ''):
        __dir_name_type = type(dir_name)
        def create_dir_pd(d_name):
            ff_string = '\\ / : * ? " < > |'
            d_name = d_name.strip()
            if d_name != '' and not path.exists(d_name):
                try:
                    makedirs(d_name)
                    self.__success(f'目录“{sub(r'([/\\])$', '', d_name)}”创建成功！')
                except OSError:
                    self.__err(f'目录名不合法(【非法字符如→】“{ff_string}”)！“{d_name}”创建失败')
            elif self.__call_create_dir:
                self.__err(f'目录名不能为空！', 'create_dir[Error]: ')
        if __dir_name_type == str:
            create_dir_pd(dir_name)
        elif __dir_name_type == list:
            for i in dir_name:
                create_dir_pd(i)
        else:
            self.__err(f'目录名填入应为列表类型或字符串类型，而非“{search(r'^<class \'(.*?)\'>$', str(__dir_name_type)).group(1)}”类型！')

    # 文件重命名
    def rename_files(self, old_files_list: list|str = '', new_files_list: list|str = '', name_lr: list|str = ''):
        __old_files_list_type = type(old_files_list)
        if __old_files_list_type == list and new_files_list == '':
            new_files_list = list()
            for i in old_files_list:
                new_files_list.append('')
        __new_files_list_type = type(new_files_list)
        __name_lr_type = type(name_lr)

        def f_rename(old_name, new_name):
            def lr_pd(old, news, pd1, pd2):
                if news == '':
                    rename(old, pd1)
                else:
                    rename(old, pd2)
            f_ntp = search(self.__files_path_re, old_name)
            if path.exists(old_name):
                if name_lr != '':
                    if __name_lr_type == str:
                        lr_pd(old_name, new_name, f"{f_ntp.group(1)}/{name_lr}{f_ntp.group(2)}{name_lr}{f_ntp[3]}",
                              f"{f_ntp.group(1)}/{name_lr}{new_name}{name_lr}{f_ntp[3]}")
                    elif __name_lr_type == list:
                        if len(name_lr) >= 2:
                            lr_pd(old_name, new_name, f"{f_ntp.group(1)}/{name_lr[0]}{f_ntp.group(2)}{name_lr[1]}{f_ntp[3]}",
                                  f"{f_ntp.group(1)}/{name_lr[0]}{new_name}{name_lr[1]}{f_ntp[3]}")
                        else:
                            lr_pd(old_name, new_name, f"{f_ntp.group(1)}/{f_ntp.group(2)}{f_ntp[3]}",
                                  f"{f_ntp.group(1)}/{new_name}{f_ntp[3]}")
                    else:
                        self.__err('文件名两边填入应为字符串或列表类型！', 'rename_files[Error]: ')
                else:
                    rename(old_name, f"{f_ntp.group(1)}/{new_name}{f_ntp[3]}")
                return f"{f_ntp.group(1)}/{new_name}{f_ntp[3]}"
            else:
                self.__err(f'文件“{old_name}”不存在！', 'rename_files[Error]: ')
                return False

        if __old_files_list_type == str and __new_files_list_type == str:
            if f_rename(old_files_list, new_files_list):
                file_type = search(self.__files_path_re, old_files_list).group(3)
                new_f_name = ''
                if __name_lr_type == str:
                    new_f_name = f'{name_lr}{new_files_list}{name_lr}'
                elif __name_lr_type == list:
                    new_f_name = f'{name_lr[0]}{new_files_list}{name_lr[1]}'
                self.__success(f'文件重命名完成！({old_files_list} to {new_f_name}{file_type})', 'rename_files[Success]: ')
            else:
                self.__err(f'文件重命名失败！(at {old_files_list})', 'rename_files[Error]: ')
        elif __old_files_list_type == list and __new_files_list_type == list:
            count = 0
            try:
                for i in old_files_list:
                    if i is not None:
                        f_rename(i, new_files_list[count])
                        count += 1
                    else:
                        continue
            except IndexError:
                pass
            except FileExistsError:
                pass
            if count != 0:
                self.__success(f'文件重命名完成！（共重命名 {count} 个文件）')
            else:
                self.__err(f'新文件名中重复旧文件名过多！重命名失败！')
        else:
            self.__err(f'新/旧 文件名填入类型应为列表类型或字符串类型！', 'rename_files[Error]: ')

    # 删除 文件|目录
    def del_files_dir(self, f_d_path: list|str, force_del_dir: bool = False):
        if type(force_del_dir) != bool:
            force_del_dir = False
        def check_path(f_or_d):
            try:
                if path.isdir(f_or_d):
                    removedirs(f_or_d)
                elif path.isfile(f_or_d):
                    remove(f_or_d)
                else:
                    self.__err(f'文件(或目录)“{f_or_d}”不存在！', 'del_files_dir[Error]: ')
                    return
                self.__success(f'已删除文件(或目录)“{f_or_d}”！')
                return
            except PermissionError:
                self.__err(f'访问“{f_or_d}”时被拒绝！', 'del_files_dir[Error]: ')
                return
            except OSError:
                if force_del_dir:
                    rmtree(f_or_d)
                    return
                self.__err(f'目录“{f_or_d}”不是空的，不能删除！', 'del_files_dir[Error]: ')
        __f_d_path_type = type(f_d_path)
        if __f_d_path_type == str:
            check_path(f_d_path)
        elif __f_d_path_type == list:
            for i in f_d_path:
                check_path(i)
        else:
            self.__err(f'文件(或目录)名填入类型应为列表类型或字符串类型！', 'del_files_dir[Error]: ')

    # 内容预览
    def content_view(self, files_path: list|str, file_encode: list|str = 'utf-8'):
        __files_path_type = type(files_path)
        __file_encode_type = type(file_encode)
        def c_view(file, encode):
            try:
                with open(file, 'r', encoding=encode) as f_view:
                    self.__prompt(f'\n-------------------- {file} --------------------\n', '')
                    print(f_view.read())
            except PermissionError:
                self.__warn(f'读取“{file}”文件时发现 用户权限不足！！！(如果是“../”或“./”，请尝试将其更改为真实目录名再重试)', 'content_view[发生意外]: ')
            except FileNotFoundError:
                self.__err(f'文件“{file}”不存在！', 'content_view[Error]: ')
            except OSError:
                self.__err(f'文件“{file}”不存在！', 'content_view[Error]: ')
            except UnicodeDecodeError:
                self.__err(f'“{encode}”编解码器无法解码！', 'content_view[Error]: ')
        if __files_path_type == str and __file_encode_type == str:
            c_view(files_path, file_encode)
        elif __files_path_type == list and __file_encode_type == list:
            file_encode = self.__create_arr_item(files_path, file_encode)
            for i in files_path:
                c_view(i, file_encode[files_path.index(i)])
        else:
            self.__err('请统一使用列表类型或字符串类型填入参数', 'content_view[Error]: ')

    # 打开文件|目录
    def open_files_dirs(self, files_path: list|str):
        def open_tf(f_path):
            f_path = f_path.replace('/', '\\')
            if system(f'if exist "{f_path}" ( start {f_path} ) else ( false ) 2>NUL'):
                self.__err(f'Windows 找不到文件(或目录)“{f_path}”。请确定文件(或目录)名是否正确后，再试一次。', 'System[Error]: ')
        if files_path:
            __files_path_type = type(files_path)
            if __files_path_type == str:
                open_tf(files_path)
            elif __files_path_type == list:
                for i in files_path:
                    open_tf(i)
            else:
                self.__err(f'文件路径填入类型应为列表类型或字符串类型，而非“{search(r'^<class \'(.*?)\'>$', str(__files_path_type)).group(1)}”类型！', 'open_files[Error]: ')
        else:
            self.__err(f'文件路径不能为空！', 'open_files[Error]: ')

    # 数组排序
    def usort(self, arr: list, idx: list = None, lr: bool = False):
        news_arr2 = []
        try:
            if idx is None:
                idx = arr
            news_arr = [0] * (len(arr) + 10)

            num = -1
            for arrI in idx:
                query = findall(r'\d+', arrI)
                news_arr[int(query[num]) - 1] = arr[idx.index(arrI)]

            for arrI in news_arr:
                if arrI != 0:
                    news_arr2.append(arrI)
            if lr is True:
                news_arr2.reverse()
            return news_arr2
        except IndexError:
            self.__warn("列表索引超出范围！排序失败", "query_files[Warning]: ")
            return False

    # 查找指定目录下的所有文件
    def query_files(self, files_path: list | str, all_files: bool = False, lr: bool = False) -> dict:
        new_arr = list()

        def create_file_arr(f_path):
            dir_file_arr = dict()
            path_all_arr = list()
            file_all_arr = list()
            file_path_all_arr = list()
            if all_files:
                for file_path, nan_arr, files_arr in walk(f_path):
                    path_arr = list()
                    file_arr = list()
                    file_path_arr = list()
                    for file_o in files_arr:
                        path_arr.append(file_path)
                        file_arr.append(file_o)
                        file_path_arr.append(f'{file_path}/{file_o}')
                    if path_arr and self.usort(file_arr, lr=lr):
                        path_all_arr.append(path_arr)
                        file_all_arr.append(self.usort(file_arr, lr=lr))
                        file_path_all_arr.append(self.usort(file_path_arr, lr=lr))
                    else:
                        file_all_arr.append(file_arr)
                        file_path_all_arr.append(file_path_arr)
            else:
                path_all_arr = next(walk(f_path))[0]
                file_all_arr = next(walk(f_path))[2]
                for file_name in next(walk(f_path))[2]:
                    file_path_all_arr.append(f'{next(walk(f_path))[0]}/{file_name}')
                if self.usort(file_all_arr, lr=lr):
                    file_path_all_arr = self.usort(file_path_all_arr, file_all_arr, lr)
                    file_all_arr = self.usort(file_all_arr, lr=lr)
            dir_file_arr['path'] = path_all_arr
            dir_file_arr['file'] = file_all_arr
            dir_file_arr['file_path'] = file_path_all_arr
            return dir_file_arr
        __files_path_type = type(files_path)
        if __files_path_type == str:
            new_arr = create_file_arr(files_path)
        elif __files_path_type == list:
            for i in files_path:
                new_arr.append(create_file_arr(i))
        else:
            self.__err('路径填入类型应为列表类型或字符串类型，且需是绝对路径！', 'dir_files_all[Error]: ')
        return new_arr

    @staticmethod
    def query_files_p(directory: str):
        arr = []
        dir_path = Path(directory)
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                arr.append(str(file_path))
        return arr

    def __init__(self):
        self.__call_create_dir = True
        self.__files_path_re = r'(.*?)([^/|^\\]+)(\.[^/|^\\]+$)'
