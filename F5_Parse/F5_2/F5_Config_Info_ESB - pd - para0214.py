# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import pandas as pd
import os



def Parse(file_name,df_pool,df_pool_sub,df_virtual,monitor_dic):
    #读取F5配置文件
    with open(file_name,'r',encoding='UTF-8') as f:
        content = list(f)
        length=len(content)
        i=0
        monitor_sub_dic={}
        #逐行读取
        while i<length:
            if ('pool' in content[i]) and ('monitor' in content[i+1]):#定位到pool，下一行为monitor
                Name_Pool=re.split(' ',content[i])[1]#获取pool名称
                j=0
                while True:#读取pool结构下所有内容
                    i=i+1
                    if 'monitor all' in content[i]:#定位到monitor
                        Name_Monitor=re.split(' |\n',content[i])[5]#获取monitor名称
                        brace=10000 #brace为大括号标志，当brace==0时表明跳出了当前括号
                    if 'members' in content[i]:
                        brace=1#进入members结构
                        if '{}' in content[i]:#定位到IP_Member
                            IP_Member=re.split(' ',content[i])[4] #获取 IP_Member              
                            df_pool=df_pool.append({"F5_Name":file_name,"Name_Pool":Name_Pool,"IP_Member":IP_Member,"IP":'',"Name_Monitor":Name_Monitor},ignore_index=True)#写入到df_pool   
                        continue#继续下一次循环
                    else:
                        if '{' in content[i]:#进入下一级大括号brace++
                             brace=brace+1
                        if '}' in content[i]:#跳出当前大括号brace--
                             brace=brace-1            
                        if ':' in content[i] and '{' in content[i] and '.'in content[i]:#特殊情况
                            IP_Member=re.split('      |/| {',content[i])[1]
                            df_pool=df_pool.append({"F5_Name":file_name,"Name_Pool":Name_Pool,"IP_Member":IP_Member,"IP":'',"Name_Monitor":Name_Monitor},ignore_index=True)#写入到df_pool   
                            j=j+1
                            continue
                        if brace==0:#members结构结束，跳出当前循环
                            break
            Name_Pool=Name_Destination=Name_Protocol=Name_profiles=''#初始化
            
            #解析virtual结构
            if 'virtual' in content[i] and 'address' not in content[i]:#定位到virtual
                Name_Virture=re.split(' ',content[i])[1]#获取Name_Virture
                brace=1#作用同上
                while True:
                    i=i+1
                    if '{' in content[i]:
                        brace=brace+1
                    if '}' in content[i]:
                        brace=brace-1    
                    if 'pool' in content[i] :#定位到pool
                        Name_Pool=re.split(' |\n',content[i])[4]
                        continue
                    if 'destination' in content[i] :#定位到destination
                        Name_Destination=re.split(' |\n',content[i])[4]
                        continue
                    if 'protocol' in content[i] :#定位到protocol
                        Name_Protocol=re.split(' |\n',content[i])[5]
                        continue           
                    if 'profiles' in content[i] :#定位到profiles
                        Name_profiles=re.split(' |\n',content[i])[4]
                        continue
                    if brace==0:#跳出当前virtual结构
                        break
                df_virtual.loc[file_name+Name_Virture]=[file_name,Name_Virture,Name_Pool,Name_Destination,Name_Protocol,Name_profiles]#写入到df_virtual 
            
            if 'monitor'in content[i] and '{' in content[i]:
                Name_Monitor=re.split(' ',content[i])[1]
                #print('Name_Monitor=',Name_Monitor)
                brace=1
                monitor_sub_dic={}
                while True:
                    i=i+1
                    if '}' in content[i]:
                        brace=0
                    elif brace==1:
                        monitor_key=re.split(' |\n',content[i])[3]
                        #print(monitor_key)
                        if 'send' in content[i]:
                            monitor_value=re.split('send|\n',content[i])[1]
                        elif 'defaults' in content[i]:monitor_value=re.split(' |\n',content[i])[5]
                        else: monitor_value=re.split(' |\n',content[i])[4]
                        #print(monitor_key,'=',monitor_value)        
                        monitor_sub_dic[monitor_key]=monitor_value
                    if brace==0:
                        monitor_dic[Name_Monitor]=monitor_sub_dic
                        break
    
            i=i+1
    return df_pool,df_virtual,monitor_dic
#解析函数结束        
        
#创建df_pool保存pool信息
df_pool =pd.DataFrame(columns=('F5_Name','Name_Pool','IP_Member','IP','Name_Monitor'))
#创建df_pool_sub保存单个pool信息
df_pool_sub =pd.DataFrame(columns=('F5_Name','Name_Pool','IP_Member','IP','Name_Monitor'))

#创建df_virtual保存virtual信息
df_virtual=pd.DataFrame(columns=('F5_Name','Name_Virture','Name_Pool','Destination','Protocol','Profiles'))
monitor_dic={}            


cwd=os.getcwd()
for files in os.walk(cwd):
    file_list=files[2]  

for file_name in file_list:
    if '.conf' in file_name:
        print(file_name)   
        df_pool,df_virtual,monitor_dic=Parse(file_name,df_pool,df_pool_sub,df_virtual,monitor_dic)

df_monitor_para=pd.DataFrame.from_dict(monitor_dic,orient='index')        
        
df_pool_virtual=pd.merge(df_pool,df_virtual,how='left',on=['F5_Name','Name_Pool'])#以pool为主表关联virtual
df_virtual_pool=pd.merge(df_virtual,df_pool,how='left',on=['F5_Name','Name_Pool'])#以virtual为主表关联pool
writer=pd.ExcelWriter('result.xlsx')#新建excel，输出结果
df_pool.to_excel(writer,sheet_name='pool',index=False)#写入pool
df_virtual.to_excel(writer,sheet_name='virtual',index=False)#写入virtual
df_pool_virtual.to_excel(writer,sheet_name='pool-virtual',index=False)#写入到pool-virtual
df_virtual_pool.to_excel(writer,sheet_name='virtual-pool',index=False)#写入到virtual-pool
df_monitor_para.to_excel(writer,sheet_name='monitor_para',index=True)#写入到monitor_para
writer.save()        