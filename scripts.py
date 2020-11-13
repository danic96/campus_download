# -*- coding: utf-8 -*-

from os import mkdir
from time import sleep
import requests


def is_directory(files, directories, real_directories, base_directory):
    i = 0
    while i < len(files):
        if files[i][1] == 0 and files[i][4] == '':
            found = False
            for directory in directories:
                if directory == files[i][0]:
                    found = True
                    break
            if not found:
                directories.append(files[i][0])
                temp = files[i][0].replace(base_directory, "")
                real_directories.append(temp)

            del files[i]
            i -= 1
        i += 1

    return files, directories, real_directories


def fix_string(temp):
    temp = temp.replace('%20', ' ')  # BLANK SPACES

    temp = temp.replace('%C3%A0', 'a')  # à
    temp = temp.replace('%C3%A1', 'a')  # á falta À i Á

    temp = temp.replace('%C3%88', 'E')  # È
    temp = temp.replace('%C3%A8', 'e')  # È???
    temp = temp.replace('%C3%A9', 'e')  # é

    temp = temp.replace('%C3%8D', 'I')  # Í
    temp = temp.replace('%C3%89', 'I')  # Ì ???
    # temp = temp.replace('%C3%8D', 'i') # í ???
    temp = temp.replace('%C3%AD', 'i')  # í

    temp = temp.replace('%C3%93', 'O')  # Ó
    temp = temp.replace('%C3%B2', 'o')  # ò ???
    temp = temp.replace('%C3%B3', 'o')  # ó ???

    temp = temp.replace('%C3%BA', 'u')  # ú

    temp = temp.replace('%C3%B1', u'ñ')  # ñ
    temp = temp.replace('n%CC%83', u'ñ')  # ñ

    temp = temp.replace('%CC%81', '')  # ´ simbol

    return temp


def generate_dir(name):
    try:
        mkdir(fix_string(name))
    except:
        # print "Unexpected error:", sys.exc_info()[0]
        pass


def login(login_url, username, password):
    login_data = {
        'eid': username,
        'pw': password,
        'submit': 'inicia+la+sessió'
    }
    user_agent = {'User-agent': 'Mozilla/5.0'}
    session = requests.Session()
    r = session.post(login_url, data=login_data, headers=user_agent)

    return session


def get_ulr_with_session(session, url):
    statuscode = -1
    while statuscode != 200:
        try:
            html = session.get(url)
            statuscode = html.status_code
        except Exception as e:
            print("   Error por el lado de la pagina")
            sleep(10)
    return html.text
