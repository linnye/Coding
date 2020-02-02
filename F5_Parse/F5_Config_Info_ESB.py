# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import csv
import codecs

f = open('esb-bigip.conf')

out = open('esb-bigip.csv','w', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['IP_Member','Name_Pool ','Name_Monitor'])


with open('esb-bigip.conf','r') as f:
    content = list(f)
    length=len(content)
    i=0   
    while i<length:
        if ('pool' in content[i]) and ('monitor' in content[i+1]):
            #print(content[i])

            result=[]
            Name_Pool=re.split(' ',content[i])[1]
            #result[0].append[Name_Pool]
            print('Name_Pool=',Name_Pool)
            j=0
            while True:
                i=i+1
                if 'monitor' in content[i]:
                    Name_Monitor=re.split(' |\n',content[i])[5]
                    print('Name_Monitor=',Name_Monitor)
                    brace=10000
                if 'members' in content[i]:
                    brace=1
                    if '{}' in content[i]:
                        IP_Member=re.split(' ',content[i])[4]                
                        print('IP_Member=',IP_Member)
                        result.append([])
                        result[j].append(IP_Member)
                        result[j].append(Name_Pool)
                        result[j].append(Name_Monitor)
                        csv_write.writerow(result[j])                           
                    continue
                else:
                    if '{' in content[i]:
                         brace=brace+1
                    if '}' in content[i]:
                         brace=brace-1            
                    if ':' in content[i] and '{}' in content[i]:
                        result.append([])
                        IP_Member=re.split('      |/| {',content[i])[1]                    
                        result[j].append(IP_Member)
                        result[j].append(Name_Pool)
                        result[j].append(Name_Monitor)
                        print('IP_Member=',IP_Member)
                        j=j+1
                        continue
#                        print(result)
                    if brace==0:
                        for k in range(j):
                            csv_write.writerow(result[k])
                        print('break!')
                        break
                        


        i=i+1
out.close()