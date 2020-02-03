# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import pandas as pd
#创建df_pool保存pool信息
df_pool =pd.DataFrame(columns=('Name_Pool ','IP_Member','Name_Monitor'))

#创建df_virtual保存virtual信息
df_virtual=pd.DataFrame(columns=('Name_Virture','Name_Pool ','Destination','Protocol','Profiles'))


with open('hulianwang.conf','r') as f:
    content = list(f)
    length=len(content)
    i=0   
    while i<length:
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
                if 'monitor' in content[i]:
                    Name_Monitor=re.split(' |\n',content[i])[5]
                    #print('Name_Monitor=',Name_Monitor)
                    continue
                #if 'members' in content[i]:
                    #brace=1
                if '/Common/' in content[i] and '{' in content[i]:
                    IP_Member=re.split(' ',content[i])[8]                
                    #print('IP_Member=',IP_Member)
                    df_pool.loc[IP_Member]=[Name_Pool,IP_Member,Name_Monitor]                    
                    continue        
                if ':' in content[i] and '{}' in content[i]:
                    IP_Member=re.split('      |/| {',content[i])[1]
                    df_pool.loc[IP_Member]=[Name_Pool,IP_Member,Name_Monitor]                   
                    #print('IP_Member=',IP_Member)
                    j=j+1
                    continue
                if brace==0:
                    break
        Name_Pool=Name_Destination=Name_Protocol=Name_profiles=''        
        if 'virtual' in content[i] and 'address' not in content[i]:
            Name_Virture=re.split(' ',content[i])[2]
            #print('Name_Virture=',Name_Virture)
            brace=1
            while True:
                i=i+1
                if '{' in content[i]:
                    brace=brace+1
                if '}' in content[i]:
                    brace=brace-1    
                if 'pool' in content[i] :
                    Name_Pool=re.split(' |\n',content[i])[5]
                    #print('Name_Pool=',Name_Pool)
                    continue
                if 'destination' in content[i] :
                    Name_Destination=re.split(' |\n',content[i])[5]
                    #print('Name_Destination=',Name_Destination)
                    continue
                if 'protocol' in content[i] :
                    Name_Protocol=re.split(' |\n',content[i])[5]
                    #print('Name_Protocol=',Name_Protocol)
                    continue           
                if 'profiles' in content[i] :
                    Name_profiles=re.split(' |\n',content[i+1])[8]
                    #print('Name_profiles=',Name_profiles)
                    i=i+1
                    continue
                if brace==0:
                    break
            df_virtual.loc[Name_Virture]=[Name_Virture,Name_Pool,Name_Destination,Name_Protocol,Name_profiles] 
        i=i+1

new=pd.merge(df_pool,df_virtual,how='left')

writer=pd.ExcelWriter('hulianwang.xlsx')#新建excel
df_pool.to_excel(writer,sheet_name='pool',index=False)#写入pool
df_virtual.to_excel(writer,sheet_name='virtual',index=False)#写入virtual
new.to_excel(writer,sheet_name='pool-virtual',index=False)#写入到pool-virtual
writer.save()        