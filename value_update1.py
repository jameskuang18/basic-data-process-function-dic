# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:42:45 2019

@author: 1000260046
"""

import pandas as pd
import os
import re

class ReadDat():
    def __init__(self, filename, assign_col, skip_rows): #指定读数据的列， 需要跳过的行数
        self.filename = filename
        self.assign_col = assign_col
        self.skip_rows = skip_rows
    def getdata(self):
        df = pd.read_csv(self.filename, sep=',', header = None,
                         skiprows=[i for i in range(self.skip_rows)])      
        selected_df = df.iloc[:,[0, self.assign_col]]
        selected_df.columns = ['ID', 'Value']
        return selected_df

def ReplaceValue(last_df, current_df):
    #concat + drop_duplicates
    last_df = pd.concat([last_df, current_df]).drop_duplicates(['ID'], keep='last')
    '''
    overflow_item_list = list(set(currentdf_index_list).difference(set(lastdf_index_list)))
    print(overflow_item_list)
    for item in overflow_item_list:
        last_df = last_df.reindex(index=last_df.index.tolist()+[item])
        last_df.loc[item] = current_df.loc[item】
    '''    
    return last_df
    
#原始文件，re文件名获取
filepath = 'C:\\Users\\1000260046\\Desktop\\xinyu\\body thickness\\ULT'
relog_list = []   
for filename in os.listdir (filepath):
    log_match = re.match('(Q[0-9]{4}[A-Z]+\d{1,6}[A-Z]+.\d{1,4})_\d{8}_.*.dat', filename)
    if log_match:
        log_name = log_match.group(1) #先做一个文件匹配的情况
        original_filename = filename  #作为Input的原始文件
    relog_match = re.match('(Q[0-9]{4}[A-Z]+\d{1,6}[A-Z]+.\d{1,4})R\d+_\d{8}_.*.dat', filename)
    if relog_match:
        relog_filename = filename #预留
        relog_list.append(filename)
        
#表头
#input data获取
original_df = ReadDat(original_filename, 36, 10).getdata() #文件前10行跳过        
writer = pd.ExcelWriter('result.xlsx')
original_df.to_excel(writer, sheet_name = 'result') #初始数据
#print('test: ', original_df[0].values)
relog_count =  len(relog_list)
for i in range(relog_count):
    re_df = ReadDat(relog_list[i], 36 , 10).getdata()
    re_df.to_excel(writer, sheet_name='result', startcol = 4 * (i + 1)) #Re数据
    original_df = ReplaceValue(original_df, re_df)


original_df.to_excel(writer, sheet_name='result', startcol = 4 * (relog_count + 1))#结果数据
writer.save()
print(original_df)
