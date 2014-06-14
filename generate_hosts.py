#!/usr/bin/env python2

'''
required modules
'''
import os
import re
import requests
import fileinput
from tempfile import NamedTemporaryFile


MVPS = 'http://winhelp2002.mvps.org/hosts.txt'
HOST = 'http://hosts-file.net/.%5Cad_servers.txt'
YOYO = 'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext'

MVPS_TEMP = NamedTemporaryFile(delete=False)
HOST_TEMP = NamedTemporaryFile(delete=False)
YOYO_TEMP = NamedTemporaryFile(delete=False)
SORT_TEMP = NamedTemporaryFile(delete=False)


def fetch_files():
    '''
    fetch the three public hosts files and write to disk
    '''

    mvps = requests.get(MVPS)
    if '200' in str(mvps.status_code):
        with MVPS_TEMP as mvps_file:
            mvps_file.write(mvps.content)
            format_mvps()
    host = requests.get(HOST)
    if '200' in str(host.status_code):
        with HOST_TEMP as host_file:
            host_file.write(host.content)
            format_host()
    yoyo = requests.get(YOYO)
    if '200' in str(yoyo.status_code):
        with YOYO_TEMP as yoyo_file:
            yoyo_file.write(yoyo.content)
            format_yoyo()
    else:
        massage_files()


def massage_files():
    '''
    call all the formatting functions to clean everything up
    '''
    format_mvps()
    format_host()
    format_yoyo()


def format_mvps():
    '''
    format the mvps file (remove comments, etc)
    '''
    for line in fileinput.input(MVPS_TEMP.name, inplace=True):
        pass1 = re.sub(r'#.*$', '', line).strip()
        print pass1

    for line in fileinput.input(MVPS_TEMP.name, inplace=True):
        if re.match(r'^\s.*', line):
            continue
        if re.search(r'localhost', line):
            continue
        if re.match(r'::1', line):
            continue
        else:
            print line.strip()

    for line in fileinput.input(MVPS_TEMP.name, inplace=True):
        pass3 = re.sub(r'^0.0.0.0 ', '127.0.0.1\t', line).strip()
        print pass3


def format_host():
    '''
    format the host file (remove comments, etc)
    '''
    for line in fileinput.input(HOST_TEMP.name, inplace=True):
        pass1 = re.sub(r'#.*$', '', line).strip()
        print pass1

    for line in fileinput.input(HOST_TEMP.name, inplace=True):
        if re.match(r'^\s.*', line):
            continue
        if re.match(r'::1', line):
            continue
        if re.search(r'localhost', line):
            continue
        if re.sub(r'127.0.0.1\t', '127.0.0.1\t', line):
            print line.strip()
        else:
            print line.strip()


def format_yoyo():
    '''
    format the yoyo file (remove comments, etc)
    '''
    for line in fileinput.input(YOYO_TEMP.name, inplace=True):
        pass1 = re.sub(r'^#.*$', '', line).strip()
        print pass1

    for line in fileinput.input(YOYO_TEMP.name, inplace=True):
        if re.match(r'^\s.*$', line):
            continue
        else:
            print line.strip()

    for line in fileinput.input(YOYO_TEMP.name, inplace=True):
        pass3 = re.sub(r'127.0.0.1 ', '127.0.0.1\t', line).strip()
        print pass3


def merge_lists():
    '''
    combine the lists, sift out duplicates, sort and write to disk
    '''
    filenames = [HOST_TEMP.name, MVPS_TEMP.name, YOYO_TEMP.name]
    with SORT_TEMP as fh_:
        for fname in filenames:
            with open(fname) as files:
                fh_.write(files.read())

    uniq = sorted(set(open(SORT_TEMP.name).readlines()))
    if not os.path.exists('hosts'):
        open('hosts', 'w').writelines(uniq)

    ## cleanup
    os.unlink(HOST_TEMP.name)
    os.unlink(MVPS_TEMP.name)
    os.unlink(YOYO_TEMP.name)
    os.unlink(SORT_TEMP.name)

    print ""
    print "You should now have a 'hosts' file in the current working directory."
    print "Append this file to your existing /etc/hosts and you're done."
    print ""


if __name__ == '__main__':
    fetch_files()
    merge_lists()
