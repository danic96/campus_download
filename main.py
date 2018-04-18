# -*- coding: utf-8 -*-

import easywebdav
from os import mkdir
from time import sleep
import sys

import getpass

from time import sleep

import ast

def isDirectory(files, directories, realDirectories, baseDirectory):
    i = 0
    while i < len(files):
        if files[i][1] == 0 and files[i][4] == '':
            found = False
            for directory in directories:
                if directory == files[i][0]:
                    found = True
                    break
            if found != True:
                directories.append(files[i][0])
                temp = files[i][0].replace(baseDirectory, "")
                realDirectories.append(temp)
                
            del files[i]
            i-=1
        i+=1
    
    return files, directories, realDirectories
    
def fixString(temp):
    temp = temp.replace('%20', ' ') # BLANK SPACES

    temp = temp.replace('%C3%A0', 'a') # à
    temp = temp.replace('%C3%A1', 'a') # á falta À i Á
    
    temp = temp.replace('%C3%88', 'E') # È
    temp = temp.replace('%C3%A8', 'e') # È???
    temp = temp.replace('%C3%A9', 'e') # é
    
    temp = temp.replace('%C3%8D', 'I') # Í
    temp = temp.replace('%C3%89', 'I') # Ì ???
    # temp = temp.replace('%C3%8D', 'i') # í ???
    temp = temp.replace('%C3%AD', 'i') # í
    
    temp = temp.replace('%C3%93', 'O') # Ó
    temp = temp.replace('%C3%B2', 'o') # ò ???
    temp = temp.replace('%C3%B3', 'o') # ó ???
    
    temp = temp.replace('%C3%BA', 'u') # ú
        
    temp = temp.replace('%C3%B1', u'ñ') # ñ
    temp = temp.replace('n%CC%83', u'ñ') # ñ
    
    temp = temp.replace('%CC%81', '') # ´ simbol
    
    return temp
    
def generateDir(name):
    try:
        mkdir(fixString(name))
    except:
        # print "Unexpected error:", sys.exc_info()[0]
        pass
        
def main(user, pswd):
    base = "downloads/"
    generateDir(base)
    global mod_files
    try:
        f = open ('files.txt','r')
        mod_files = f.read()
        mod_files = ast.literal_eval(mod_files)
        f.close()
    except:
        mod_files = {}
        
    baseDirectories =  [["/dav/102013-1718/", "AMSA"], 
                        ["/dav/102022-1718/", "Sistemes"],
                        ["/dav/102020-1718/", "IA"],
                        ["/dav/101313-1718/", "Economia 2"],
                        ["/dav/101324-1718/", "Dret del Treball"],
                        ["/dav/101320-1718/", "Direccio Estrategica"],
                        ["/dav/101317-1718/", "Politica Economica"],
                        ["/dav/102019-1718/", "Ampliacio"],
                        ["/dav/102024-1718/", "Xarxes 2"],
                        ["/dav/101326-1718/", "Direccio Operacions"],
                        ["/dav/101328-1718/", "Direccio Financera"],
                        ["/dav/101329-1718/", "Econometria"],
                        ["/dav/102052-1718/", "Requeriments"]]
    for baseDirectory in baseDirectories:
        main2(base + baseDirectory[1] + "/", baseDirectory[0], user, pswd)
        print "\n"
        break
    # print mod_files
    
    f = open ('files.txt','w')
    f.write(str(mod_files))    
    f.close()
    
def main2(base, baseDirectory, user, pswd):
    global mod_files
    directories = []
    files = []
    realDirectories = []

    directories.append(baseDirectory)
    
    time = 0

    print base.split("/")[1]
    print "https://cv.udl.cat" + baseDirectory
    # passw = open("pass", "r")
    
    webdav = easywebdav.connect('cv.udl.cat',
                                username=user,
                                password=pswd,
                                protocol='https',
                                cert='')

    
    # LISTAR DIRECOTRIOS A CREAR Y ARCHIVOS A DESCARGAR
    i = 0
    while i < len(directories):
        webdav.cd(directories[i])
        files += webdav.ls()
        sleep(time)
        files, directories , realDirectories= isDirectory(files, directories, realDirectories, baseDirectory)
        sleep(time)
        i+=1      
    
    # EMPEZAMOS LAS DESCARGAS    

    generateDir(base)
    for dir in realDirectories:
        generateDir(base+dir)
        
    # FILES DONWLOAD
    
    # print files[0]
    # print " " + str(files[0][0]) # nom fitxer
    # print " " + str(files[0][2]) # data modificacio
    # print " " + str(files[0][3]) # data creacio
    # return 0
    
    i = 0
    for file in files:
        file_name = file[0]
        file_date = file[2]
        print "   " + fixString(file[0].encode("utf8"))
        temp1 = file[0].replace(baseDirectory, "")
        temp1 = temp1.split('/')
        if len(temp1) == 1:
            # webdav.download(file[0], fixString(base+temp1[len(temp1)-1]))
            downloadFile(file[0], file[2], base, "", temp1)
            mod_files[file_name] = file_date
        else:        
            for directory in realDirectories:
                if len(temp1) == len(directory.split("/")):
                    j = 0
                    temp2 = directory.split('/')
                    match = True
                    while j < len(temp1) - 1:
                        if temp1[j] != temp2[j]:
                            match = False
                            break
                        j += 1
                    if match == True:
                        downloadFile(file[0], file[2], base, directory, temp1)
                        mod_files[file_name] = file_date
                        # print mod_files
                    pass
        i+=1
        
def downloadFile(filen, filed, base, directory, temp):
    if ".URL" not in filen and (filen not in mod_files or filed != mod_files[filen]):
        webdav.download(filen, fixString(base+directory+temp[len(temp)-1]))
    else:
        print "     Not downloaded"

if __name__ == "__main__":
    user = raw_input("User: ")
    pswd = getpass.getpass("Password: ")
    main(user, pswd)
