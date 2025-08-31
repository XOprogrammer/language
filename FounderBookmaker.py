from re import (search as _src, findall as _findall,
                S as _S, DOTALL as _DOTALL, sub as _sub,
                match as _match)
from os import system as _system

__all__ = ['FounderBookmaker', 'version']

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

class FounderBookmaker:
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

    # 帮助文档
    def help(self) -> dict:
        title_lr = ('rep(str): 判断依据\n\t\t'
                    'top1(str): 一级标题设置\n\t\t'
                    'top2(str): 二级标题设置\n\t\t'
                    'top3(str): 三级标题设置\n\t\t'
                    'top4(str): 四级标题设置\n\t\t'
                    'pattern(str): 正则匹配(默认匹配阿拉伯数字)')
        chart_lr = ('start(str): 图、表名称前\n\t\tend(str): 图、表名称后\n\t\tstart_t(str): 表名称前\n\t\tend_t(str): 表名称后\n\t\t'
                    'start_i(str): 图名称前,\n\t\tend_i(str): 图名称后,\n\t\taccord(bool): 是否开启图、表同步(默认是)')
        part_tb = ('start(str): 段前\n\t\t'
                   'end(str): 段后')
        image_content = ('path(list|str): 图片地址的数组\n\t\t'
                         'img_type(str): 图片属性\n\t\t'
                         'write_file_encode(str): 写编码\n\t\t'
                         'write_image_bool(bool): 写入图模式选择(默认统一写入)')
        table_revise = ('write_file_list(list|str): 文件地址\n\t\t'
                        'write_file_encode(str): 写编码\n\t\t'
                        'top(str): 表格开标签属性\n\t\t'
                        'bottom(str): 表格闭标签属性\n\t\t'
                        'bh_type(list|str): 表行属性\n\t\t'
                        'write_table_bool(bool): 写入表模式选择(默认统一写入)')
        references_lr = ('start(str): 前添加\n\t\t'
                         'center(str): 在开头[数字]后添加\n\t\t'
                         'end(str): 后添加')
        open_copy_file = ('app_path(str): 指定应用打开文件(非必要)\n\t\t'
                          'open_file_path(bool): 在资源管理器中找到文件(非必要，默认False -> 不使用此功能)')
        save_write_all = ('filepath(list|str): 文件地址\n\t\t'
                          'rencode(str): 读解码\n\t\t'
                          'wencode(str): 写编码\n\t\t'
                          'save_path(str): 保存路径(非必要)')
        def h_prompt(string):
            return f'\033[34m{string}\033[0m'
        help_text = {
            'version': {
                'title': 'version',
                'message': h_prompt('查看 FounderBookmaker 版本号'),
                'must': False
            },
            'title_lr': {
                'title': 'title_lr',
                'message': h_prompt('给标题两边添加内容，默认为空'),
                'join': title_lr,
                'must': False
            },
            'chart_lr': {
                'title': 'chart_lr',
                'message': h_prompt('给图、表名称两边添加内容，默认为空'),
                'join': chart_lr,
                'must': False
            },
            'part_tb': {
                'title': 'part_tb',
                'message': h_prompt('统一给段落前后添加内容，默认为空'),
                'join': part_tb,
                'must': False
            },
            'image_content': {
                'title': 'image_content',
                'message': h_prompt('修改插入图片的内容，默认为空（内部清空）'),
                'join': image_content,
                'must': False
            },
            'table_revise': {
                'title': 'table_revise',
                'message': h_prompt('修改表信息，默认为空'),
                'join': table_revise,
                'must': False
            },
            'references_lr': {
                'title': 'references_lr',
                'message': h_prompt('给参考文献添加内容，默认为空'),
                'join': references_lr,
                'must': False
            },
            'content_preview': {
                'title': 'content_preview',
                'message': h_prompt('预览文件内容, 使用时必须在写入文件后'),
                'must': False
            },
            'open_copy_file': {
                'title': 'open_copy_file',
                'message': h_prompt('打开写入后的文件, 使用时必须在写入文件后(默认)'),
                'join': open_copy_file,
                'must': False
            },
            'save_write_all': {
                'title': 'save_write_all',
                'message': h_prompt('执行主函数(写入函数)'),
                'join': save_write_all,
                'must': True
            }
        }
        for ht in help_text:
            self.__success(ht, '', end='\t\t\n')
            for ht2 in help_text[ht]:
                if ht2 != 'title':
                    print(f'\t\t{help_text[ht][ht2]}')
            if ht != 'save_write_all':
                print('\n')
        return help_text

    # 内容预览
    def content_preview(self):
        self.__prompt('已开启内容预览！', '\ncontent_preview[prompt]: ')
        for wfile_path in self.wfile_list:
            if wfile_path is not None and self.__read_encode is not None:
                with open(wfile_path, 'r', encoding=self.__read_encode) as preview:
                    content = preview.read()
                    self.__prompt(f'\n-------------------- {wfile_path} --------------------\n', '')
                    print(content)
            else:
                self.__err('content_preview 引用错误！应该在 write_all 之后引用（此项不影响写入)')
                return

    # 打开文件
    def open_copy(self, app_path: str = '', open_file_path: bool = False):
        if open_file_path:
            self.__prompt('已启动自动打开文件路径...', '\nopen_copy[prompt]: ')
        else:
            self.__prompt('已启动自动打开文件...', '\nopen_copy[prompt]: ')
        for wfile_path in self.wfile_list:
            if wfile_path is not None:
                if not open_file_path:
                    if app_path != '':
                        app_path = f'"" "{app_path}" '
                    try:
                        _system(f'start {app_path}{wfile_path}')
                    except Exception as e:
                        self.__err(f'{e}(不影响写入)', '发生意外错误[Error]: ')
                else:
                    try:
                        _system(f'start {_src(r'(.*?)([^/\\]+)\.([a-zA-Z0-9]+)$', wfile_path).group(1)}')
                    except Exception as e:
                        self.__err(f'{e}(不影响写入)', '发生意外错误[Error]: ')
            else:
                self.__err('open_copy_file 引用错误！应该在 write_all 之后引用（此项不影响写入)')

    # 标题两边
    def __title_lr(self, line, founder_bookmaker_cursor) -> bool:
        dian_len = len(_findall(self.__title_lr_rep, line))
        if _src(self.__title_lr_pattern, line) is not None and _src(r'[\u4e00-\u9fff]', line) is not None and len(
                line) <= 25:
            if dian_len == 0:
                founder_bookmaker_cursor.write(f'{self.__title_lr_top1}{line}\n')
                return True
            elif dian_len == 1:
                founder_bookmaker_cursor.write(f'{self.__title_lr_top2}{line}\n')
                return True
            elif dian_len == 2:
                founder_bookmaker_cursor.write(f'{self.__title_lr_top3}{line}\n')
                return True
            elif dian_len == 3:
                founder_bookmaker_cursor.write(f'{self.__title_lr_top4}{line}\n')
                return True
            else:
                return False

    def title_lr(self, rep: str = '', top1: str = '', top2: str = '', top3: str = '', top4: str = '', pattern: str = r'^(\d+(\.\d+)*)\s*(?=.*[^\d\s.])(.+)'):
        self.__title_lr_Bool = True
        self.__title_lr_rep = rep
        self.__title_lr_top1 = top1
        self.__title_lr_top2 = top2
        self.__title_lr_top3 = top3
        self.__title_lr_top4 = top4
        self.__title_lr_pattern = pattern
        self.__prompt('默认只能修改带有中文字符的匹配项\n', '\ntitle_lr[prompt]: ')

    # 图、表两边
    def __chart_lr(self, line, founder_bookmaker_cursor) -> bool:
        if self.__chart_lr_accord:
            pattern = r'^(表|图)\s*([一二三四五六七八九十百千万亿零]+|[0-9]+|(?:I|V|X|L|C|D|M)(?:I|V|X|L|C|D|M)*)(.+)$'
            if _src(pattern, line) is not None:
                founder_bookmaker_cursor.write(f'{self.__chart_lr_start}{line}{self.__chart_lr_end}\n')
                return True
            else:
                return False
        else:
            Table = r'^表\s*([一二三四五六七八九十百千万亿零]+|[0-9]+|(?:I|V|X|L|C|D|M)(?:I|V|X|L|C|D|M)*)(.+)$'
            Image = r'^图\s*([一二三四五六七八九十百千万亿零]+|[0-9]+|(?:I|V|X|L|C|D|M)(?:I|V|X|L|C|D|M)*)(.+)$'
            if _src(Table, line) is not None:
                founder_bookmaker_cursor.write(f'{self.__chart_lr_table_start}{line}{self.__chart_lr_table_end}\n')
                return True
            elif _src(Image, line) is not None:
                founder_bookmaker_cursor.write(f'{self.__chart_lr_image_start}{line}{self.__chart_lr_image_end}\n')
                return True
            else:
                return False

    def chart_lr(self, start: str = '', end: str = '', start_t: str = '', end_t: str = '', start_i: str = '',
                 end_i: str = '', accord: bool = True):
        self.__chart_lr_Bool = True
        self.__chart_lr_start = start
        self.__chart_lr_end = end
        self.__chart_lr_table_start = start_t
        self.__chart_lr_table_end = end_t
        self.__chart_lr_image_start = start_i
        self.__chart_lr_image_end = end_i
        self.__chart_lr_accord = accord
        if accord and (
                self.__chart_lr_table_start != '' or self.__chart_lr_table_end != '' or self.__chart_lr_image_start != '' or self.__chart_lr_image_end != ''):
            self.__warn('单独设置图、表名称无效，已开启统一设置模式！（此设置无任何作用，且不影响写入)')
        elif not accord and (self.__chart_lr_start != '' or self.__chart_lr_end != ''):
            self.__warn('统一设置图、表名称无效，已开启单独设置模式！（此设置无任何作用，且不影响写入)')

    # 段落前后
    def __part_tb(self, line, founder_bookmaker_cursor) -> bool:
        if line.strip() != '' and _src(r'^', line) is None and _match(r'^［\d+］', line) is None:
            founder_bookmaker_cursor.write(f'{self.__part_tb_start}{line}{self.__part_tb_end}\n')
            return True
        else:
            return False

    def part_tb(self, start: str = '', end: str = ''):
        self.__part_tb_Bool = True
        self.__part_tb_start = start
        self.__part_tb_end = end

    # 图片内容
    def __image_content(self, line, founder_bookmaker_cursor) -> bool:
        __image_path_type = type(self.__image_path)
        if __image_path_type == str:
            if _src(r'(〖XC)(.*?)(〗)', line) is not None:
                image_xc = _src(r'(.*?)(〖XC).*?〗(.*)', line)
                founder_bookmaker_cursor.write(
                    f'{image_xc.group(1)}{image_xc.group(2)}<{self.__image_path}>;{self.__image_type}〗{image_xc.group(3)}\n')
                self.__image_count += 1
                return True
            else:
                return False
        elif __image_path_type == list:
            for wfile_path in self.wfile_list:
                with open(wfile_path, 'r', encoding=self.__image_write_file_encode) as imgr:
                    __img_read = imgr.read()
                    with open(wfile_path, 'w', encoding=self.__image_write_file_encode) as imgw:
                        img_string = ''
                        try:
                            __img_file_path_list = self.__image_path.pop(0)
                            __img_file_path_list_type = type(__img_file_path_list)
                            __img_xc_list = _findall(r'(.*?)(〖XC)(.*?)〗(.*?)(?=〖XC|)', __img_read, _DOTALL)
                            __img_count = 0
                            for k in __img_xc_list:
                                if __img_file_path_list_type == list:
                                    try:
                                        img_string += f'{k[0]}{k[1]}<{__img_file_path_list[__img_xc_list.index(k)]}>;{self.__image_type}〗{k[3]}'
                                        __img_count += 1
                                    except IndexError:
                                        img_string += f'{k[0]}{k[1]}{k[2]}〗{k[3]}'
                                        self.__warn('数据不足，将默认不修改此图片', 'image_content[prompt]: ')
                                else:
                                    self.__err(
                                        f'应该传入二维数组，这里却是一维数组！图片单独写入失败！(在 image_content 第1个参数)',
                                        'image_content[prompt]: ')
                                    return False
                        except IndexError:
                            if self.__image_msg_err:
                                self.__err('数据严重不足，将退出修改图片信息！', 'image_content[Error]: ')
                                self.__image_msg_err = False

                            return False
                        imgw.write(f'{img_string}')
                self.__success(f'成功修改“{wfile_path}”中的图片信息！(共修改 {__img_count} 个图)')
            return True
        else:
            self.__err('图片地址填入类型错误！应为列表类型或字符串类型(仅影响图片写入)')
            return False

    def image_content(self, img_path: list | str = None, img_type: str = '', write_file_encode: str = 'utf-8',
                      write_image_bool: bool = True):
        self.__image_content_Bool = write_image_bool
        self.__image_path = img_path
        self.__image_type = img_type
        self.__image_write_file_encode = write_file_encode
        if not write_image_bool and not self.__image_flag:
            self.__err(
                'image_content 引用位置错误(当前为单独写入文件模式： False)！应在 save_write_all 引用 >后< 引用(仅影响图修改)')
        elif not write_image_bool and self.__image_flag:
            self.__prompt('已开启图片内容单独写入，将不计图改...', '\nimage_content[prompt]: ')
            self.__image_content(None, None)
        elif not self.__image_content_location and write_image_bool:
            self.__err(
                'table_revise 引用位置错误(当前为统一写入行模式： True)！应在 save_write_all 引用 >前< 引用(仅影响图修改)')

    # 表格样式
    def __table_revise(self, line, founder_bookmaker_cursor) -> bool | list:
        if self.__table_revise_Bool:
            table_bh_type_t = type(self.__table_bh_type)
            if table_bh_type_t == str:
                try:
                    table_src_top = _src(r'(.*?)(〖BG[(（])(.*?)〗(.*)', line)
                    table_src_bottom = _src(r'(.*?)(〖BG[)）])(.*?)〗(.*)', line)
                    tr_src = _src(r'(.*?)(〖BH)(.*?)〗(.*)', line)
                    if table_src_top is not None and self.__table_top != '':
                        founder_bookmaker_cursor.write(
                            f'{table_src_top.group(1)}{table_src_top.group(2)}{self.__table_top}〗{table_src_top.group(4)}\n')
                    elif tr_src is not None and self.__table_bh_type != '':
                        founder_bookmaker_cursor.write(
                            f'{tr_src.group(1)}{tr_src.group(2)}{self.__table_bh_type}〗{tr_src.group(4)}\n')
                    elif table_src_bottom is not None and self.__table_bottom != '':
                        founder_bookmaker_cursor.write(
                            f'{table_src_bottom.group(1)}{table_src_bottom.group(2)}{self.__table_bottom}〗{table_src_bottom.group(4)}\n')
                        self.__table_count += 1
                    else:
                        return False
                    return True
                except AttributeError:
                    return False
            else:
                self.__err('表行属性填入类型错误！ 应该为字符串类型(当前为统一写入行模式： True)')
        else:
            if self.__write_file_list is not None:
                self.__table_count = 0

                def revise(file_list: str) -> bool:
                    def str_rep_t(string):
                        return (string.replace('\\', '\\\\')
                                .replace('\n', '\\n')
                                .replace('+', '\\+')
                                .replace('.', '\\.'))

                    bh_string = ''
                    try:
                        with open(file_list, 'r', encoding=self.__write_file_encode) as tbr:
                            readlines = tbr.read()
                            with open(file_list, 'w', encoding=self.__write_file_encode) as tbw:
                                table_src = _findall(r'(〖BG[（(])(.*?)〗(.*?)(〖BG[）)])(.*?)〗',
                                                    readlines,
                                                    _DOTALL)
                                self.__table_count = len(table_src)
                                if table_src:
                                    bg_last = ''
                                    for i in table_src:
                                        bh_string += f"\n{i[0]}{self.__table_top}〗\n"
                                        bh = _findall(r'(.*?)(〖BH)(.*?)(〗)', i[2], _S)
                                        bg_position = _src(str_rep_t(f'{i[0]}{i[1]}〗{i[2]}{i[3]}{i[4]}〗'), readlines,
                                                             _S).span()
                                        for k in bh:
                                            if bh.index(k) == len(bh) - 1:
                                                bg_last = f'{k[0]}〖BH{k[2]}〗'
                                                break
                                            try:
                                                if self.__table_bh_type[bh.index(k)] == '':
                                                    self.__table_bh_type[bh.index(k)] = k[2]
                                                bh_string += f'{k[0].replace('\n', '')}\n〖BH{self.__table_bh_type[bh.index(k)]}〗'
                                            except IndexError:
                                                bh_string += f'{k[0].replace('\n', '')}\n〖BH〗'
                                        bg_last_group = _src(rf'{bg_last}(.*?)(〖BG)(.*?)〗', f'{i[2]}{i[3]}{i[4]}〗', _S)
                                        bh_string += f"{bg_last_group.group(1).replace('\n', '')}\n{i[3]}{self.__table_bottom}〗\n"
                                        readlines = _sub(str_rep_t(readlines[bg_position[0]:bg_position[1]]), bh_string,
                                                        readlines, _S)
                                        bh_string = ''
                                    tbw.write(readlines)
                                else:
                                    self.__warn(f'在读取“{file_list}”的时候： 未发现任何表')
                                    return False
                        return True
                    except UnicodeDecodeError:
                        self.__err(
                            f"“{self.__write_file_encode}”编解码器无法解码！在读取“{file_list}”的时候(将到此直接保存)")
                        return False
                    except FileNotFoundError:
                        self.__err(f'文件“{file_list}”不存在！写入失败')
                        return False

                write_file_list_type = type(self.__write_file_list)
                if write_file_list_type == list:
                    revise_bool_arr = list()
                    for item in self.__write_file_list:
                        revise_bool = revise(item)
                        if revise_bool:
                            self.__success(f'成功修改“{item}”中的目标表信息！(共修改 {self.__table_count} 个表)')
                        revise_bool_arr.append(revise_bool)
                    return revise_bool_arr
                elif write_file_list_type == str:
                    revise_bool = revise(self.__write_file_list)
                    if revise_bool:
                        self.__success(
                            f'成功修改“{self.__write_file_list}”中的目标表信息！(共修改 {self.__table_count} 个表)')
                    return revise_bool
                else:
                    self.__err('文件地址填入应该为列表类型或字符串类型！在 table_revise 第一个参数')
                    return False
            else:
                self.__err('文件地址不能为空！在 table_revise 第一个参数')
                return False

    def table_revise(self, write_file_list: list | str = '', write_file_encode: str = 'utf-8', top: str = '',
                     bottom: str = '', bh_type: list | str = '', write_table_bool: bool = True):
        self.__table_revise_Bool = write_table_bool
        self.__write_file_list = write_file_list
        self.__write_file_encode = write_file_encode
        self.__table_top = top
        self.__table_bottom = bottom
        self.__table_bh_type = bh_type
        if not self.__revise_copy_table and not write_table_bool:
            self.__err(
                'table_revise 引用位置错误(当前为单独写入文件模式： False)！应在 save_write_all 引用 >后< 引用(仅影响表修改)')
        elif not write_table_bool and self.__revise_copy_table:
            self.__prompt('已开启表信息单独写入，将不计表改...', '\ntable_revise[prompt]: ')
            self.__table_revise(None, None)
        elif not self.__table_copy_location and write_table_bool:
            self.__err(
                'table_revise 引用位置错误(当前为统一写入行模式： True)！应在 save_write_all 引用 >前< 引用(仅影响表修改)')

    # 参考文献
    def __references_lr(self, line, founder_bookmaker_cursor) -> bool:
        if _match(r'^［\d+］', line) is not None:
            wxNum = _match(r'(^［\d+］)(.*)', line).group(1)
            wxTxt = _match(r'(^［\d+］)(.*)', line).group(2)
            founder_bookmaker_cursor.write(
                f'{self.__references_lr_start}{wxNum}{self.__references_lr_center}{wxTxt}{self.__references_lr_end}\n')
            return True
        else:
            return False

    def references_lr(self, start: str = '', center: str = '', end: str = ''):
        self.__references_lr_Bool = True
        self.__references_lr_start = start
        self.__references_lr_center = center
        self.__references_lr_end = end

    # 保存所有写入
    def save_write_all(self, filepath: list | str = None, rencode: str = 'utf-8', wencode: str = 'utf-8',
                       save_path: str = '') -> None:
        self.__table_copy_location = False
        self.__image_content_location = False

        def write_all(w_filepath, w_rencode, w_wencode, w_save_path):
            w_filepath = w_filepath.replace('\\', '/')
            try:
                with open(w_filepath, 'r', encoding=w_rencode) as rFbd:
                    rezz = r'(.*?)([^/\\]+)\.([a-zA-Z0-9]+)$'
                    if w_save_path == '':
                        w_save_path = _src(rezz, w_filepath).group(1)
                    wfile = f'{_sub(r'/$', '', w_save_path)}/{_src(rezz, w_filepath).group(2)}_copy.{_src(rezz, w_filepath).group(3)}'
                    try:
                        with open(wfile, 'w', encoding=w_wencode) as founder_bookmaker_cursor:
                            read_lines = rFbd.readlines()
                            self.__image_count = 0
                            self.__table_count = 0
                            for line in read_lines:
                                line = line.replace('\n', '')
                                if self.__title_lr_Bool:
                                    if self.__title_lr(line, founder_bookmaker_cursor):
                                        continue
                                if self.__chart_lr_Bool:
                                    if self.__chart_lr(line, founder_bookmaker_cursor):
                                        continue
                                if self.__part_tb_Bool:
                                    if self.__part_tb(line, founder_bookmaker_cursor):
                                        continue
                                if self.__references_lr_Bool:
                                    if self.__references_lr(line, founder_bookmaker_cursor):
                                        continue
                                if self.__image_content_Bool:
                                    if self.__image_content(line, founder_bookmaker_cursor):
                                        continue
                                if self.__table_revise_Bool:
                                    __table_revise_tr = self.__table_revise(line, founder_bookmaker_cursor)
                                    if type(__table_revise_tr) == bool:
                                        if __table_revise_tr:
                                            continue
                                    else:
                                        if __table_revise_tr.pop(0):
                                            continue
                                founder_bookmaker_cursor.write(f'{line}\n')
                            self.wfile_list.append(wfile)
                            self.__read_encode = w_wencode
                            if not self.__table_revise_Bool:
                                self.__revise_copy_table = True
                            if not self.__image_content_Bool:
                                self.__image_flag = True
                            self.__success(
                                f'成功写入所有内容到“{wfile}”！(图改: {self.__image_count} , 表改: {self.__table_count})')

                    except UnicodeEncodeError:
                        self.__err(f"“{w_wencode}”编解码器无法编码！在写入“{wfile}”的时候")
                        return
                    except FileNotFoundError:
                        self.__err(f'目录“{_sub(r'/$', '', w_save_path)}”不存在！写入失败')
                        return
            except UnicodeDecodeError:
                self.__err(
                    f"“{w_rencode}”编解码器无法解码！在读取“{_src(rezz, w_filepath).group(0)}”的时候(将到此直接保存)")
                return
            except FileNotFoundError:
                self.__err(f'文件“{w_filepath}”不存在！写入失败')
                return

        filepath_type = type(filepath)
        if len(filepath) == 0:
            self.__err("未指定文件！在 save_write_all 第1个参数")
            return
        else:
            if filepath_type == str:
                self.__prompt('最好用列表类型填入文件地址！', 'save_write_all[prompt]: ')
                write_all(filepath, rencode, wencode, save_path)
            elif filepath_type == list:
                for i in filepath:
                    write_all(i, rencode, wencode, save_path)
            else:
                self.__err('文件地址填入应为“字符串类型”或“列表类型”！写入失败')

    def __init__(self):
        self.__image_msg_err = True
        self.__image_count = 0
        self.__table_count = 0
        self.__table_copy_location = True
        self.__image_content_location = True
        self.__revise_copy_table = False
        self.__image_flag = False
        self.wfile_list = list()
        self.__read_encode = None
        self.__title_lr_Bool = False
        self.__chart_lr_Bool = False
        self.__part_tb_Bool = False
        self.__references_lr_Bool = False
        self.__image_content_Bool = False
        self.__table_revise_Bool = False
