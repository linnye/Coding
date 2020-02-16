# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import pandas as pd
#创建df_pool保存pool信息
df_pool =pd.DataFrame(columns=('Name_Pool ','IP_Member','Name_Monitor'))
#创建df_pool_sub保存单个pool信息
df_pool_sub =pd.DataFrame(columns=('Name_Pool ','IP_Member','Name_Monitor'))

#创建df_virtual保存virtual信息
df_virtual=pd.DataFrame(columns=('Name_Virture','Name_Pool ','Destination','Protocol','Profiles'))


with open('guimian.conf','r',encoding='UTF-8') as f:
    content = list(f)
    length=len(content)
    monitor_dic={}
    profile_dic={}
    i=0   
    while i<length:
        IP_Member=Name_Pool=IP_Member=Name_Monitor=''
        if 'ltm pool' in content[i] and '{' in content[i]:
            brace=1
            Name_Pool=re.split(' ',content[i])[2]
            #print('Name_Pool=',Name_Pool)
            j=0
            while True:
                i=i+1
                if '{' in content[i]:
                    brace=brace+1
                if '}' in content[i]:
                    brace=brace-1   
                if '/Common/' in content[i] and '{' in content[i]:
                    IP_Member=re.split(' ',content[i])[8]
                    if 'address' in content[i+1]:
                        IP=re.split(' |\n',content[i+1])[13]                
                    #print('IP_Member=',IP_Member)
                    df_pool_sub.loc[j]=[Name_Pool,IP_Member,''] 
                    j=j+1                   
                    continue        
                if '    monitor' in content[i]and '            'not in content[i]:
                    Name_Monitor=re.split(' |\n',content[i])[5]
                    df_pool_sub.loc[:,'Name_Monitor']=Name_Monitor#将Name_Monitor写入当前pool信息表中
                    df_pool=pd.concat([df_pool,df_pool_sub])#合并到总的pool信息表中
                    df_pool_sub=df_pool_sub[df_pool_sub.IP_Member == '']#情况当前pool信息，方便存储下一个pool信息
                    #print('Name_Monitor=',Name_Monitor)
                    continue
                if brace==0:
                    break
        Name_Pool=Name_Destination=Name_Protocol=Name_profiles=''        
        if 'virtual' in content[i] and 'address' not in content[i]:
            Name_Virture=re.split(' ',content[i])[2]
            brace=1
            while True:
                i=i+1
                if '{' in content[i]:
                    brace=brace+1
                if '}' in content[i]:
                    brace=brace-1    
                if 'pool' in content[i] :
                    Name_Pool=re.split(' |\n',content[i])[5]
                    continue
                if 'destination' in content[i] :
                    Name_Destination=re.split(' |\n',content[i])[5]
                    continue
                if 'protocol' in content[i] :
                    Name_Protocol=re.split(' |\n',content[i])[5]
                    continue           
                if 'profiles' in content[i] :
                    Name_profiles=re.split(' |\n',content[i+1])[8]
                    i=i+1
                    continue
                if brace==0:
                    break
            df_virtual.loc[Name_Virture]=[Name_Virture,Name_Pool,Name_Destination,Name_Protocol,Name_profiles] 
        
        if 'ltm monitor'in content[i] and '{' in content[i]:
            Name_Monitor=re.split(' ',content[i])[3]
            #print('Name_Monitor=',Name_Monitor)
            brace=1
            monitor_sub_dic={}
            while True:
                i=i+1
                if '}' in content[i]:
                    brace=0
                elif brace==1:
                    monitor_key=re.split(' |\n',content[i])[4]
                    if 'send' in content[i]:
                        monitor_value=re.split('send|\n',content[i])[1]
                    else: monitor_value=re.split(' |\n',content[i])[5]        
                    monitor_sub_dic[monitor_key]=monitor_value
                if brace==0:
                    monitor_dic[Name_Monitor]=monitor_sub_dic
                    break
            
        if 'ltm profile'in content[i] and '{' in content[i]:
            Name_Profile=re.split(' ',content[i])[3]
            #print('Name_Monitor=',Name_Monitor)
            brace=1
            profile_sub_dic={}
            while True:
                i=i+1
                if '}' in content[i]:
                    brace=0
                elif brace==1:
                    profile_key=re.split(' |\n',content[i])[4]
                    profile_value=re.split(' |\n',content[i])[5]        
                    profile_sub_dic[profile_key]=profile_value
                if brace==0:
                    profile_dic[Name_Profile]=profile_sub_dic
                    break            
            
        if 'profile'in content[i] and 'ltm' not in content[i]:
            Name_Profile=re.split(' ',content[i])[2]
            #print('Name_Monitor=',Name_Monitor)
            brace=1
            profile_sub_dic={}
            while True:
                i=i+1
                if '}' in content[i]:
                    brace=0
                elif brace==1:
                    #profile_key=str.join(re.split(' ',content[i]).pop(-1))
                    profile_key='-'.join(re.split(' ',content[i])[3:-1])
                    profile_value=re.split(' |\n',content[i])[-2]        
                    profile_sub_dic[profile_key]=profile_value
                if brace==0:
                    profile_dic[Name_Profile]=profile_sub_dic
                    break            
                        
            
            
        i=i+1
        
        
        
df_monitor_para=pd.DataFrame.from_dict(monitor_dic,orient='index')        
df_profile_para=pd.DataFrame.from_dict(profile_dic,orient='index')         
new=pd.merge(df_pool,df_virtual,how='left')

writer=pd.ExcelWriter('guimian.xlsx')#新建excel，输出结果
df_pool.to_excel(writer,sheet_name='pool',index=False)#写入pool
df_virtual.to_excel(writer,sheet_name='virtual',index=False)#写入virtual
new.to_excel(writer,sheet_name='pool-virtual',index=False)#写入到pool-virtual
df_monitor_para.to_excel(writer,sheet_name='monitor_para',index=True)
df_profile_para.to_excel(writer,sheet_name='profile_para',index=True)
writer.save()        