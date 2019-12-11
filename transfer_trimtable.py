# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:51:11 2019

@author: 1000260046
"""
import os
import pandas as pd
from binary_transform import IO_To_Dec as Get_Dec
from DAC_transform import Get_Trim_Data

#Trim table class, input: path+filename, output:class 通过Get_Transfer_Data()得到主程序需要的list数据 
#transfer Trim table.xlsx to class
class Trim_table:
    def __init__(self, name):
        self.name = name

    def Read_File(self, encols="G, H, N"):
        resource_file = open(self.name, 'rb')
        header_name = ['Addr (Hex)', 'IO', 'DAC (New)']
        origin_df = pd.read_excel(resource_file, sheet_name=1, header=None,
                                names=header_name, skiprows=2, usecols=encols)
        
        del_row = origin_df[origin_df['Addr (Hex)'] == ' '].index
        NoNan_df = origin_df.drop(del_row) #过滤空值
        DS_filter = NoNan_df['DAC (New)'].isin(['DS'])
        NoDS_df = NoNan_df[~DS_filter] #过滤DS行
        #print (NoDS_df['IO'].str.len() == 3)
        self.sorted_df = NoDS_df.sort_values(by = "Addr (Hex)", ascending=True)
        #print(self.sorted_df)

    def Data_Process(self):
        # IO列转换为16进制数字
        bin_tran = lambda x : hex ( int(Get_Dec(x), 10))
        self.sorted_df['IO'] = self.sorted_df['IO'].apply(bin_tran)
        #DAC列处理
        self.sorted_df['DAC (New)'] = self.sorted_df['DAC (New)'].apply(Get_Trim_Data)
        #打入对应list
    
    def Get_Transfer_Data(self):
        #print(self.sorted_df.at[41, 'IO'], type (self.sorted_df.at[41, 'IO']))
        df_f = self.sorted_df['DAC (New)'].apply(lambda x: x[0])
        df_Trim_v = self.sorted_df['DAC (New)'].apply(lambda x: x[1])
        df_Trim_s = self.sorted_df['DAC (New)'].apply(lambda x: x[2])
        special_df = self.sorted_df['DAC (New)'].str.len() >= 4
        special_df = self.sorted_df[special_df]
        df_Add = special_df['DAC (New)'].apply(lambda x: x[3])
        df_condit_mask = special_df['DAC (New)'].apply(lambda x: x[4])
        df_compara = special_df['DAC (New)'].apply(lambda x: x[5])
        df_shift1 = special_df['DAC (New)'].apply(lambda x: x[6])
        df_shift2 = special_df['DAC (New)'].apply(lambda x: x[7])
        self.Address_list = self.sorted_df['Addr (Hex)'].tolist()
        self.Fix_or_Trim_list = df_f.tolist()
        self.Trim_value_list= df_Trim_v.tolist()
        self.Trim_mask_list = self.sorted_df['IO'].tolist()
        self.Trim_shift_list = df_Trim_s.tolist()
        self.UR_address_list = df_Add.tolist()
        self.condition_mask_list = df_condit_mask.tolist()
        self.comparator_value_list = df_compara.tolist()
        self.Trim_shift_conditional1_list = df_shift1.tolist()
        self.Trim_shift_conditional2_list = df_shift2.tolist()
        '''
        print('1: ',self.Address_list,
        '2: ', self.Fix_or_Trim_list,
        '3: ',self.Trim_value_list,
        '4: ',self.Trim_mask_list, 
        '5: ',self.Trim_shift_list,
        '6: ',self.UR_address_list,
        '7: ',self.condition_mask_list,
        '8: ',self.comparator_value_list,
        '9: ',self.Trim_shift_conditional1_list,
        '10: ',self.Trim_shift_conditional2_list)
        '''
#open xlsx file
desktop_path = os.path.join (os.path.join(os.environ['USERPROFILE']), 'Desktop')
filepath = desktop_path + r'\Checkout_tool'
filename = 'Copy of BiCS4_512Gb_VLV_eX3_MT-KGD_Parameter_rev5.2D_for_ECB_SIE-AWS_2019-10-15.xlsx'
Trim_file = filepath + '\\' + filename
Trim_Class = Trim_table(Trim_file)
Trim_Class.Read_File() #读取指定的列
Trim_Class.Data_Process()
Trim_Class.Get_Transfer_Data()