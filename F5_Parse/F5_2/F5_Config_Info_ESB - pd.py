# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import csv
import pandas as pd


#csv_write = csv.writer(out,dialect='excel')

df_members =pd.DataFrame(columns=('IP_Member','Name_Pool ','Name_Monitor'))
df_virtual=pd.DataFrame(columns=('Name_Virture','Name_Pool ','Destination','Protocol','Profiles'))



#csv_write.writerow(['IP_Member','Name_Pool ','Name_Monitor'])


with open('waiqianzhi.conf','r') as f:
    content = list(f)
    length=len(content)
    i=0   
    while i<length:
        if ('pool' in content[i]) and ('monitor' in content[i+1]):
            #print(content[i])

            #result=[]
            Name_Pool=re.split(' ',content[i])[1]
            #result[0].append[Name_Pool]
            #print('Name_Pool=',Name_Pool)
            j=0
            while True:
                i=i+1
                if 'monitor all' in content[i]:
                    Name_Monitor=re.split(' |\n',content[i])[5]
                    #print('Name_Monitor=',Name_Monitor)
                    brace=10000
                if 'members' in content[i]:
                    brace=1
                    if '{}' in content[i]:
                        IP_Member=re.split(' ',content[i])[4]                
                        #print('IP_Member=',IP_Member)
                        #result.append([])
                        df_members.loc[IP_Member]=[IP_Member,Name_Pool,Name_Monitor]
                        #result[j].append(IP_Member)
                        #result[j].append(Name_Pool)
                        #result[j].append(Name_Monitor)
                        #csv_write.writerow(df.loc[IP_Member])                           
                    continue
                else:
                    if '{' in content[i]:
                         brace=brace+1
                    if '}' in content[i]:
                         brace=brace-1            
                    if ':' in content[i] and '{' in content[i] and '.'in content[i]:
                        #result.append([])
                        IP_Member=re.split('      |/| {',content[i])[1]
                        df_members.loc[IP_Member]=[IP_Member,Name_Pool,Name_Monitor]                    
                        #result[j].append(IP_Member)
                        #result[j].append(Name_Pool)
                        #result[j].append(Name_Monitor)
                        #print('IP_Member=',IP_Member)
                        j=j+1
                        continue
#                        print(result)
                    if brace==0:
                        #for k in range(j):
                            #csv_write.writerow(result[k])
                        #print('break!')
                        break

        if 'virtual' in content[i] and 'address' not in content[i]:
            Name_Virture=re.split(' ',content[i])[1]
            #print('Name_Virture=',Name_Virture)
            brace=1
            while True:
                i=i+1
                if '{' in content[i]:
                    brace=brace+1
                if '}' in content[i]:
                    brace=brace-1    
                if 'pool' in content[i] :
                    Name_Pool=re.split(' |\n',content[i])[4]
                    #print('Name_Pool=',Name_Pool)
                    continue
                if 'destination' in content[i] :
                    Name_Destination=re.split(' |\n',content[i])[4]
                    #print('Name_Destination=',Name_Destination)
                    continue
                if 'protocol' in content[i] :
                    Name_Protocol=re.split(' |\n',content[i])[5]
                    #print('Name_Protocol=',Name_Protocol)
                    continue           
                if 'profiles' in content[i] :
                    Name_profiles=re.split(' |\n',content[i])[4]
                    #print('Name_profiles=',Name_profiles)
                    continue
                if brace==0:
                    break
            df_virtual.loc[Name_Virture]=[Name_Virture,Name_Pool,Name_Destination,Name_Protocol,Name_profiles] 
        i=i+1
out.close()

df_members.to_csv('waiqianzhi-members.csv', sep=',', header=True, index=False)
df_virtual.to_csv('esb-bigip-virtual.csv', sep=',', header=True, index=False)
new=pd.merge(df_members,df_virtual)
new.to_csv('waiqianzhi.csv', sep=',', header=True, index=False)