from re import search, sub, MULTILINE, DOTALL
from utils.FilesUtil import FilesUtil

ftool = FilesUtil()

# 合并文件
def merge_file():
    # ftool.help()
    filePath = 'E:\\文档\\方正书版\\001  压电与声光\\压电与声光2025年1期\\item\\2'
    fbd_list = list()
    for fbd in ftool.query_files(filePath)['file_path']:
        if search(r'\.fbd$', fbd):
            fbd_list.append(fbd)
    ftool.merge_files_b(fbd_list, './压电正文2')

# 换行处理：最好进行此步骤（最好只执行一次）
def huanhang(fbd_path):
    with open(fbd_path, 'r', encoding='GB18030') as f_read:
        read_all = sub(r'([]$)', '\1\n', sub(r'〖', '\n〖', f_read.read()))
        with open(fbd_path, 'w', encoding='GB18030') as f_write:
            f_write.write(read_all.replace('\\[', '［').replace('\\]', '］').replace(':', '：').strip('\n'))
            print('换行处理成功！')

# 删除fbd内的注释等
def deleteZS(fbd_path):
    with open(fbd_path, 'r', encoding='GB18030') as f_read:
        read_all = sub(r'(\n〖BP[(（]〗.*?\n〖BP[)）]〗)|(〖FL[(（].*?〗)|(〖FL[)）].*?〗)', '', f_read.read(), DOTALL)
        with open(fbd_path, 'w', encoding='GB18030') as f_write:
            f_write.write(sub(r'^[]\n$|^\n$', '', read_all, MULTILINE))
            print('删除处理成功！')

# 一键排版
def ydysg_text_all(fbd_path):
    with open(fbd_path, 'r', encoding='GB18030') as read_f:
        lines = ''
        trCount = 0
        for i in read_f.readlines():
            i = i.strip()
            if i == '' or i == '' or i == '':
                continue
            # 摘要替换
            zyt_zh = search(r'(^[]?)摘\s*\t*〓*要[:：]\s*\t*〓*(.*)', i)
            zyt_en = search(r'(^[]?)Abstract[:：]\s*\t*〓*(.*)', i)
            # 序列替换
            xl = search(r'(^[]?)\s*\t*〓*(\d+)[)）]\s*\t*〓*(.*)([]?$)', i)
            # 点数标题替换
            dbt1 = search(r'(^[]?)(\d+\.\d+\.\d+)\s*\t*〓*(.*)', i)
            dbt2 = search(r'(^[]?)(\d+\.\d+)\s*\t*〓*(.*)', i)
            # 整数标题替换
            zst = search(r'(^[]?)(\d+?)\s*\t*〓*(.*)', i)
            # 表标题替换
            tbt = search(r'(^[]?表)\s*\t*〓*(\d+)\s*\t*〓*(.*)', i)
            # 表头替换
            thead = search(r'(^[]?)〖BG[(（].*?〗', i)
            # 表行替换
            tr = search(r'〖BH.*?〗(.*)', i)
            # 表尾替换
            tbody = search(r'(^[]?)〖BG[)）].*?〗', i)
            # 图标题替换
            imgT_max = search(r'^[]?图\s*\t*〓*(\d+)\s*\t*〓*(.*)', i)
            imgT_min = search(r'^[]?[(（]([a-z])[)）]\s*\t*〓*(.*)', i)
            # 图标签替换
            imgH = search(r'(^[]?)〖XC.*?〗(.*)', i)
            # 关键词替换
            kwd_zh = search(r'(^[]?)关键词[:：]\s*\t*〓*(.*)', i)
            kwd_en = search(r'(^[]?)Key\s*\t*〓*word(s?)[:：]\s*\t*〓*(.*)', i)
            # 中图分类号 和 文献标识码 的替换
            zw = search(r'(^[]?)中图分类号[:：]\s*\t*〓*(.*?)〓+\s*\t*〓*文献标识码[:：]\s*\t*〓*(.*)〓*\s*\t*〓*', i)
            # 公式替换
            gs = search(r'(^[]?)\s*\t*〓*(.*?)〓*\s*\t*〓*[(（](\d+)[)）]〓*([]?$)', i)
            # 文献头部替换
            wxt = search(r'^[]?参考文献[:：]\s*\t*〓*', i)
            # 单数文献替换
            dwx = search(r'^[]?\s*\t*〓*[\[［](\d)[]］]〓*\s*\t*〓*(.*)[]?', i)
            # 双数文献替换
            swx = search(r'^[]?\s*\t*〓*[\[［](\d{2,})[]］]〓*\s*\t*〓*(.*)[]?', i)
            # 结尾符号
            over = search(r'^$', i)
            if zyt_zh or zyt_en:
                try:
                    lines += i.replace(i, f'{zyt_zh.group(1)}〖HK5：42〗〖HT5”H〗〓〓摘〓要：〖HT5”SS〗{zyt_zh.group(2)}')
                except AttributeError:
                    lines += i.replace(i, f'{zyt_en.group(1)}〖HK5：42〗〖WT5”HZ〗Abstract：〖WT5”BZ〗{zyt_en.group(2)}')
            elif xl:
                lines += i.replace(i, f'{xl.group(1)}{xl.group(2)}）〓{xl.group(3)}{xl.group(4)}')
            elif dbt1 or dbt2:
                try:
                    lines += i.replace(i, f'{dbt1.group(1)}〖BT3〗{dbt1.group(2)}〓{dbt1.group(3)}')
                except AttributeError:
                    lines += i.replace(i, f'{dbt2.group(1)}〖BT3〗{dbt2.group(2)}〓{dbt2.group(3)}')
            elif zst:
                if int(zst.group(2)) == 0:
                    lines += i.replace(i, f'〖KH*5D〗〖FL(K2〗\n〖BT2〗{zst.group(2)}〓{zst.group(3)}')
                else:
                    lines += i.replace(i, f'{zst.group(1)}〖BT2〗{zst.group(2)}〓{zst.group(3)}')
            elif tbt:
                lines += i.replace(i, f'\n〖JZ(〗〖HT5F〗{tbt.group(1)}{tbt.group(2)}〓{tbt.group(3)}〖JZ)〗\n〖HT0.2〗〖HT〗〖HT5”SS〗')
            elif thead:
                lines += i.replace(i, f'〖BG(!BTXDF〗〖XB,HT5”SS;M<续表>〗\n〖BHDFTK+1.3mmJK+1.3mm,WK16mm,WK19mm。2,WK11mm,WKW〗')
            elif tr:
                trCount += 1
                if trCount > 1:
                    if trCount == 2:
                        lines += i.replace(i, f'〖BHD〗{tr.group(1)}')
                    elif trCount == 3:
                        lines += i.replace(i, f'〖BHDW〗{tr.group(1)}')
                    else:
                        lines += i.replace(i, f'〖BH〗{tr.group(1)}')
                else:
                    lines = sub('\n$', '', lines)
            elif tbody:
                lines += i.replace(i, f'〖BHDFG1mm,WKW〗\n〖BG)W〗')
                trCount = 0
            elif imgT_max or imgT_min:
                try:
                    lines += i.replace(i,f'〖HT0.2〗〖HT〗〖HT5”SS〗〖JZ(〗图{imgT_max.group(1)}〓{sub(r'[]?$', '', imgT_max.group(2))}〖JZ)〗〖HT〗')
                except AttributeError:
                    lines += i.replace(i,f'〖HT0.2〗〖HT〗〖HT5”SS〗〖JZ(〗（{imgT_min.group(1)}）{sub(r'[]?$', '', imgT_min.group(2))}〖JZ)〗〖HT〗')
            elif imgH:
                lines += i.replace(i, f'{imgH.group(1)}〖JZ〗〖XC<./eps/.eps>;P〗\n{imgH.group(2)}')
            elif kwd_zh or kwd_en:
                try:
                    lines += i.replace(i, f'{kwd_zh.group(1)}〖HT〗关键词：〖HT5”SS〗{kwd_zh.group(2)}')
                except AttributeError:
                    lines += i.replace(i, f'{kwd_en.group(1)}〖WT5”HZ〗Key words：〖WT5”BZ〗{kwd_en.group(3)}\n〖ST〗〖WT〗〖HK〗〖HT〗〖HJ〗\n')
            elif zw:
                lines += i.replace(i, f'{zw.group(1)}〖HTH〗中图分类号：〖HT5”SS〗{zw.group(2)}〓〓〖HTH〗文献标识码：{zw.group(3).replace('〓', '')}〖HJ〗〖HK〗')
            elif gs:
                lines += i.replace(i, f'{gs.group(1)}{gs.group(2)}〖JY(〗（{gs.group(3)}）〖JY)〗{gs.group(4)}')
            elif wxt:
                lines += i.replace(i, f'〖HS1*2〗〖HTH〗参考文献：〖HT〗〖HT5”SS〗')
            elif dwx or swx:
                try:
                    lines += i.replace(i, f'［{swx.group(1)}］〖ZK(〗{swx.group(2)}〖ZK)〗')
                except AttributeError:
                    lines += i.replace(i, f'［{dwx.group(1)}］〓〖ZK(〗{dwx.group(2)}〖ZK)〗')
            elif over:
                lines += i.replace(i, f'\n〖HT〗〖HJ〗〖FL)〗\n')
            else:
                lines += i

            lines += '\n'

        with open(sub(r'\.fbd', '_new.fbd', fbd_path), 'w', encoding='GB18030') as write_f:
            write_f.write(sub(r'\s*\t*〓*\n$', '', lines) + '')
            print('初步排版完成！')


fbd_p = '压电正文2.fbd'
merge_file()
huanhang(fbd_p)
deleteZS(fbd_p)
ydysg_text_all(fbd_p)