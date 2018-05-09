'''
Created on 2018年5月3日
中文字符转拼音小写字母
@author: piaopiao
'''
import pinyin

def to_pinyin(var_str):
   
    if isinstance(var_str, str):
        if var_str == 'None':
            return ""
        else:
            return pinyin.get(var_str, format='strip', delimiter="")
    else:
        return '类型不对'