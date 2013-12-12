#!/usr/bin/env python

import os, subprocess, time, sys, glob, shutil, datetime, platform

# where is this script getting invoked from?
#see: http://stackoverflow.com/questions/19322836/how-do-i-find-directory-of-the-python-running-script-from-inside-the-script#19323023

script_path = os.path.dirname(os.path.realpath(__file__))

curr_path = os.getcwd()

if script_path != curr_path:
    print 'FAIL. the whole POINT is to run this FROM the directory it came in. go there and run exactly: ./set_env.py'
    exit()

# the file actually has the extention 'plist', but the call to 'defaults write' wants us to OMIT that suffix
environment_plist_path = os.path.expanduser("~/.MacOSX/environment")

subprocess.check_call(
    ["defaults", "write", environment_plist_path, 'QT_BINARIES_REPO', curr_path])

# calling 'defaults write' makes it turn into a BINARY PLIST, which is such a bummer. turn it back to human readable:
subprocess.check_call(
    ["plutil", "-convert", "xml1", str(environment_plist_path + '.plist') ])


print 'Finished calling updates for [~/.MacOSX/environment]. You should LOG OUT and log in for full effect.'

