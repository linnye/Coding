# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:04:28 2020

@author: LiJinling
"""

import re
import csv

out = open('hulianwang.csv','w', newline='')
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(['IP_Member','Name_Pool ','Name_Monitor'])


with open('hulianwang.conf','r') as f:
    content = list(f)
    length=len(content)
    i=0    
    while i<length:
        if 'ltm pool' in content[i] and '{' in content[i]:
            #print(content[i])
            brace=1
            result=[]

            Name_Pool=re.split(' ',content[i])[2]
            #result[0].append[Name_Pool]
            #print('Name_Pool=',Name_Pool)
            j=0
            while True:
                i=i+1
                if '{' in content[i]:
                    brace=brace+1
                if '}' in content[i]:
                    brace=brace-1            
                

                if ('/Common/'in content[i]) and ('{'in content[i]):
                    result.append([])
                    IP_Member=re.split('/| {',content[i])[2]
                    #result[j].append[Name_Pool]                        
                    result[j].append(IP_Member)
                    result[j].append(Name_Pool)
                    #print('IP_Member=',IP_Member)
                    j=j+1
                    #print(result)
                if 'monitor' in content[i] and brace<2:                   
                    #print(re.split(' ',content[i])[5])
                    Name_Monitor=re.split(' ',content[i])[5]
                    #print('Name_Monitor=',Name_Monitor)
                    #result.append(Name_Monitor)
                    for k in range(j):
                        result[k].append(Name_Monitor)
                        #csv_write.writerow(result[k])
                    #print(result)
                    #break
                if brace==0:
                    for k in range(j):
                        csv_write.writerow(result[k])
                    print('break!')
                    break

        i=i+1
out.close()