#!/usr/bin/env python

import os, subprocess, time, sys, glob, shutil, datetime, platform

# where is this script getting invoked from?
#see: http://stackoverflow.com/questions/19322836/how-do-i-find-directory-of-the-python-running-script-from-inside-the-script#19323023

script_path = os.path.dirname(os.path.realpath(__file__))

curr_path = os.getcwd()

var_name = 'QT_BINARIES_REPO'

if script_path != curr_path:
    print 'FAIL. the whole POINT is to run this FROM the directory it came in. go there and run exactly: ./set_env.py'
    exit()

if sys.platform == 'darwin':

    # the file actually has the extention 'plist', but the call to 'defaults write' wants us to OMIT that suffix
    environment_plist_path = os.path.expanduser("~/.MacOSX/environment")

    subprocess.check_call(
        ["defaults", "write", environment_plist_path, var_name, curr_path])

    # calling 'defaults write' makes it turn into a BINARY PLIST, which is such a bummer. turn it back to human readable:
    subprocess.check_call(
        ["plutil", "-convert", "xml1", str(environment_plist_path + '.plist') ])

elif sys.platform == 'win32':

    setx_ret = os.system( 'setx.exe %s "%s" /M' % ( var_name, curr_path ) )
    if ( setx_ret != 0 ):
        print 'FAIL. unable to call setx. are you Admin? is setx on the path? (you can manually set ' + var_name + ' instead)'
        exit()

else:
    print 'FAIL. script not designed for your OS.'
    exit()



if sys.platform == 'darwin':

    print 'SUCCESS. Finished calling updates for [~/.MacOSX/environment]. You should LOG OUT and log in for full effect.'

elif sys.platform == 'win32':

# NOTE: is logout/login only a requirement on mac? i suppose it doesn't hurt to do it on win32 also...
    print 'SUCCESS. Added env var ' + var_name + '. You should open a new shell and/or reopen Visual Studio, etc.'

