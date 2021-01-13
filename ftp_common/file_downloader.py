# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:11:21 2020

@author: sunco
"""


import os
from ftplib import FTP
#from multiprocessing import Pool

# connect to ftp site
def ftpConnect(ftpserver,port=21): # default ftp port number is 21
    ftp = FTP()
    try:
        ftp.connect(ftpserver, port)
        ftp.login()
    except:
        raise IOError('\n FTP connection failed, please check the code!')
    else:
        print(ftp.getwelcome())  # print welcome
        print('\n+------- ftp connection successful!!! --------+')
    return ftp

# download single file
def ftpDownloadFile(ftp, ftpfile, localfile):
    bufsize = 1024*100 # more speed more buf
    path = os.path.join(localfile,ftpfile)
    with open(path, 'wb') as fid:
        print('Downloading：',ftpfile)
        ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, bufsize)  # recevie ftp file and write into local file
        print ('Successful download')
    return True

# download all file in a dir
def ftpDownload(ftp, ftpath, localpath):
    # print remote path
    print('Remote Path: {0}'.format(ftpath))
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    ftp.cwd(ftpath)
    print ('Successful cd into ',ftpath)
    
    for file in ftp.nlst():
        print ('file: ',file)
        local = os.path.join(localpath, file)
        file_path = os.path.join(ftpath, file)
        if not os.path.exists(local):
            os.makedirs(local)    
        ftp.cwd(file_path)
        print('enter sub dir：--', file_path)
        for sub_file in ftp.nlst():
            ftpDownloadFile(ftp, sub_file, local)
        ftp.cwd('..')     
    return True

# list files in a ftp dir
def list_ftp_dir(ftp, ftpath):
    ftp.cwd(ftpath)
    files_list = ftp.nlst()
    return files_list


if __name__ == '__main__':
    # input param
    ftpserver = 'data1.commons.psu.edu' # ftp server
    ftppath = 'pub/commons/meteorology/greybush/emars-1p0/data/emars-1p0-cntl/' # dir in the ftp server
    localpath = '/root/'
    #pool = Pool(processes=6)
    
    # connect to ftp site
    ftp = ftpConnect(ftpserver)
    
    file_list = list_ftp_dir(ftp,ftppath)
    for file_name_index in range(len(file_list)):
        with open("download_list.txt", 'r') as f: 
            lines = f.readlines()  
            last_line = lines[-1] # get where to restart
        print(last_line)
        if file_name_index==0:
            file_name_index = int(last_line)
        file_name = file_list[file_name_index]
        file_size = ftp.size(file_name)/1024./1024./1024. # trans unit to Gb
        st = os.statvfs(localpath)
        vol_res = st.f_bavail * st.f_frsize/1024./1024./1024. # trans unit to Gb
        if file_size < (vol_res-0.2): # check if the remain storage is ok for the file
            ftpDownloadFile(ftp,file_name,localpath) # download the file
            if file_name==file_list[-1]:
                os.system('mv download_list.txt') # rm the download_list.txt as a sign to the host
        else:
            print ('start data transfer')
            with open("download_list.txt", 'a') as f: # write what to restart next time
                f.write(str(file_name_index)+'\n')
            break

    
    
    # disconnect to ftp site 
    ftp.quit() 
    
    
    
    
    
    
    
                
