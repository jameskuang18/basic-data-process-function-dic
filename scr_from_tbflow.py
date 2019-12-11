# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:56:17 2019

@author: 1000260046
"""

import pandas as pd
import os
import re
#若存在中间有注释的情况，匹配可能会被覆盖， 待验证

filename = 'MTCT_flow.txt' #手动更改
resource_file = open(filename)
scr_name_list = []
tb_name_list = [] #获取到的TB——line打入
df_dict = {} #为了df，将行逻辑置为列逻辑
for line in resource_file:
    #print(line)
    #tb_match = re.match('\s?new TestFlow \( \"(tb__\d{1,3}__.*)\".*,', line) #所有注释行包括，除了DebugPats 正则少个空格，不需要，没改
    MTCT_tb_pattern = '\s+\{\s+(\d{1,5}),\s+.*,\s+.*,\s+\"(.*)\",.*,'
    tb_match = re.match(MTCT_tb_pattern, line)
    if tb_match:
        tb_full_line = 'tb' + tb_match.group(1) + '_' + tb_match.group(2) #tb+number+content
        #print('tb full item: ', tb_full_line)
        if '//' in tb_full_line:
            tb_split = tb_full_line.split('//')[0]
            tb_special_match = re.match('(tb__\d{1,3}__.*)\".*,', tb_split)
            if tb_special_match:
                tb_name_list.append (tb_special_match.group(1))
        else:
            tb_name_list.append (tb_full_line)
#TB传入dictonary,同时处理scr
for tb_item in tb_name_list:
    if 'SCR' in tb_item:
        #scr_match = re.match('.*_(scr\d{1,5}p?\d{0,4}V?)_.*', tb_item) #包含scr的line，若下行有报错，正则错误
        MTCT_scr_pattern = '.*_(SCR\d{1,5}p?\d{0,4}V?)'
        scr_match = re.match(MTCT_scr_pattern, tb_item)
        scr_item = scr_match.group(1)
        print(scr_item)
        scr_name_list.append (scr_item)
    else:
        scr_name_list.append ('')
#dictonary封装df，并写入excel
df_dict['full tb'] = tb_name_list
df_dict['scr name'] = scr_name_list
df = pd.DataFrame(df_dict)
writer = pd.ExcelWriter('result.xlsx')
df.to_excel(writer, sheet_name = 'result') #初始数据
writer.save()