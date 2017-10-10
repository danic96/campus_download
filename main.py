import easywebdav
from os import mkdir
from time import sleep
import sys

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
    return temp.replace('%20', ' ').replace('%C3%A0', 'a').replace('%C3%B3', 'o').replace('%C3%A8', 'e').replace('%C3%A9', 'e').replace('%C3%A1', 'a').replace('%C3%8D', 'I').replace('%C3%93', 'O')
    
def generateDir(name):
    try:
        mkdir(fixString(name))
    except:
        # print "Unexpected error:", sys.exc_info()[0]
        pass
        
def main():
    base = "downloads/"
    generateDir(base)
    baseDirectories = [["/dav/102013-1718/", "AMSA"], 
                        ["/dav/102022-1718/", "Sistemes"],
                        ["/dav/102020-1718/", "IA"],
                        ["/dav/101313-1718/", "Economia 2"],
                        ["/dav/101324-1718/", "Dret del Treball"],
                        ["/dav/101320-1718/", "Direccio Estrategica"]]
    # baseDirectories = [["/dav/102022-1718/", "Sistemes"]]
    for baseDirectory in baseDirectories:
        main2(base + baseDirectory[1] + "/", baseDirectory[0])
        print "\n"
    
def main2(base, baseDirectory):
    directories = []
    files = []
    realDirectories = []

    directories.append(baseDirectory)
    
    time = 0

    print "https://cv.udl.cat" + baseDirectory # DIRECCIO AMSA
    passw = open("pass", "r")
    webdav = easywebdav.connect('cv.udl.cat',
                                username='dcv4',
                                password=passw.read(),
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
    
    for file in files:
        print "   " + str(file[0])
    # print ""
    # print directories
    # print ""
    # print realDirectories
        
    
    # EMPEZAMOS LAS DESCARGAS    

    generateDir(base)
    for dir in realDirectories:
        generateDir(base+dir)
        
    i = 0
    for file in files:
        temp1 = file[0].replace(baseDirectory, "")
        temp1 = temp1.split('/')
        if len(temp1) == 1:
            webdav.download(file[0], base+temp1[len(temp1)-1])
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
                        webdav.download(file[0], fixString(base+directory+temp1[len(temp1)-1]))
                    pass
        i+=1
        
if __name__ == "__main__":
    main()