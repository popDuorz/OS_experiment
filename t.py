import os                           #，不存在就退出
lines = open('ProcessManager.py').readlines()  #打开文件，读入每一行
fp = open('ProcessManager2.py','w')  #打开你要写得文件pp2.txt
for s in lines:
       fp.write(s.replace('\t','    '))
fp.close()  
