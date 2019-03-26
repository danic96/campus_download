# -*- coding: utf-8 -*-

from scripts import *

import easywebdav
import getpass
from time import sleep
import ast


def get_base_directories():

    return []

        
def main(user, pswd):
    base = "downloads/"
    generate_dir(base)
    global mod_files
    try:
        f = open('files.txt', 'r')
        mod_files = f.read()
        mod_files = ast.literal_eval(mod_files)
        f.close()
    except:
        mod_files = {}
    
    # 5e curs
    base_directories = [["/dav/102021-1819", "ASPECTES LEGALS"],
                        ["/dav/101321-1819", "PRESSUPOSTARIA"],
                        ["/dav/101323-1819", "ECONOMIA MUNDIAL"],
                        ["/dav/101313-1819", "ECONOMIA 2"],
                        ["/dav/101322-1819", "PLANIFICACIO FISCAL"],
                        ["/dav/101327-1819", "ANALISI ESTATS"],
                        ["/dav/102029-1819", "ARQUITECTURES PROGRAMARI"],
                        ["/dav/101329-1819", "ECONOMETRIA"],
                        ["/dav/101328-1819", "DIRECCIO FINANCERA"]]

    base_directories = get_base_directories()

    print base_directories

    exit()
    for base_directory in base_directories:
        search_directory(base + base_directory[1] + "/", base_directory[0], user, pswd)
        print "\n"
    
    f = open('files.txt', 'w')
    f.write(str(mod_files))    
    f.close()


def search_directory(base, base_directory, user, pswd):
    global mod_files
    directories = []
    files = []
    real_directories = []

    directories.append(base_directory)
    
    time = 0

    print base.split("/")[1]
    print "https://cv.udl.cat" + base_directory
    # passw = open("pass", "r")
    
    webdav = easywebdav.connect('cv.udl.cat',
                                username=user,
                                password=pswd,
                                protocol='https',
                                cert='')

    # LISTAR DIRECTORIOS A CREAR Y ARCHIVOS A DESCARGAR
    i = 0
    while i < len(directories):
        webdav.cd(directories[i])
        files += webdav.ls()
        sleep(time)
        files, directories , real_directories = is_directory(files, directories, real_directories, base_directory)
        sleep(time)
        i += 1
    
    # EMPEZAMOS LAS DESCARGAS    

    generate_dir(base)
    for dir in real_directories:
        generate_dir(base+dir)
    
    i = 0
    for file in files:
        file_name = file[0]
        file_date = file[2]
        # print "   " + fix_string(file[0].encode("utf8"))
        temp1 = file[0].replace(base_directory, "")
        temp1 = temp1.split('/')
        if len(temp1) == 1:
            # webdav.download(file[0], fix_string(base+temp1[len(temp1)-1]))
            download_file(file[0], file[2], base, "", temp1, webdav)
            mod_files[file_name] = file_date
        else:        
            for directory in real_directories:
                if len(temp1) == len(directory.split("/")):
                    j = 0
                    temp2 = directory.split('/')
                    match = True
                    while j < len(temp1) - 1:
                        if temp1[j] != temp2[j]:
                            match = False
                            break
                        j += 1
                    if match:
                        download_file(file[0], file[2], base, directory, temp1, webdav)
                        mod_files[file_name] = file_date
                        # print mod_files
                    pass
        i += 1
        
        
def download_file(filen, filed, base, directory, temp, webdav):
    if ".URL" not in filen and (filen not in mod_files or filed != mod_files[filen]):
        print "   " + fix_string(filen.encode("utf8"))
        webdav.download(filen, fix_string(base+directory+temp[len(temp)-1]))
    else:
        # print "     Not downloaded"
        pass


if __name__ == "__main__":
    user = raw_input("User: ")
    pswd = getpass.getpass("Password: ")
    main(user, pswd)
