#!/usr/bin/env python


# This script "fixes" the "install name id" and also the various Mach-O rel-paths of dylibs.

# When we say "fix" we mean that absolute paths are changed to paths like @executable_path/libNAME.dylib

# ARGUMENT ONE [required] -- the path to your target dir

# This is designed to be applied to ONE DIRECTORY, at "one depth" of the directory only.
# That means you should have some folder "folder_foo/" that basically contains
# several files such as "folder_foo/some_bar1.dylib", "folder_foo/some_bar2.dylib", etc.
# Usually you will have a folder of dylibs such that at least some of those dylibs
# link against various others of the dylibs sitting side-by-side in that folder.

# This script will NOT recurse into any SUB-FOLDERS under your targeted directory.

# What this script does:
#        1. "fixes" the "install name id" of every dylib in the folder.
#                  This means that if a dylib previously identified itself as
#                  "@loader_path/libCedrusStreams.dylib" then after this script runs
#                  that same dylib will report its id as:
#                  "@executable_path/libCedrusStreams.dylib"
#
#   2. For every dylib in the folder, the dylib will be tested to see if if
#                  links against any of the other dylibs in the folder.  If so, then
#                  EVERY rel-path containing a link to some dylib in the folder will also
#                  be fixed.  For example, if some dylib reports that it has been
#                  linked against "@executable_path/../Frameworks/libboost_filesystem-xgcc811-mt-1_37.dylib",
#                  then after this script runs the dylib will report that it has been
#                  linked against "@executable_path/libboost_filesystem-xgcc811-mt-1_37.dylib"

import os, subprocess, time, sys, glob, shutil, datetime, platform

def run_os_command_expecting_zero_output( command ):
    the_stdout = os.popen( command ).read().rstrip()
    if the_stdout != '':
        print 'UNEXPECTED RESULTS:'
        print the_stdout


if len(sys.argv) < 2:
    print '****************************** This script requires one argument. ******************************'
else:

    target_dir = sys.argv[1]

    print " --- mach-o_dylib_fixer.sh: BEGIN SCRIPT --- "

    outer_glob = glob.glob( target_dir + '/*dylib' )

    outer_loop_dylibs_list = []
    inner_loop_dylibs_list = []

    for dylib in outer_glob:
        if False == os.path.islink( dylib ):
            outer_loop_dylibs_list += [ dylib ]
            inner_loop_dylibs_list += [ dylib ]

    for outer_dylib in outer_loop_dylibs_list:

        outer_file_basename = os.popen( 'basename "' + outer_dylib + '"' ).read().rstrip()

        old_id_name = os.popen( 'otool -D "' + outer_dylib + '" | tail -1'  ).read().rstrip()

        desired_id = '@executable_path/' + outer_file_basename

        if old_id_name != desired_id:

            print '      --- Fixing install name id on ' + outer_file_basename + ' --- '

            command = 'install_name_tool -id "' + desired_id + '" "' + outer_dylib + '"'
            run_os_command_expecting_zero_output( command )

        for inner_dylib in inner_loop_dylibs_list:
            # PSEUDO-CODE FOR SECOND PORTION OF THIS ROUTINE:
            #
            #         For each dylib in this folder (i.e. "for each PEER of the outer-loop file"):
            #         {
            #                        If the list of linkages inside outer-loop-file CONTAINS a reference to peer:
            #                        {
            #                                Ensure that the linkage is a fixed reference.
            #                        }
            #         }

            inner_file_basename_01 = os.popen( 'basename "' + inner_dylib + '"' ).read().rstrip()
            inner_file_basename_02 = '54321098760987654321'

            if inner_file_basename_01.endswith( '5.1.1.dylib' ):
                inner_file_basename_02 = inner_file_basename_01.split('.')[0] + '.5.dylib'

            print '      --- Checking for link to ' + inner_file_basename_01 + ' in ' + outer_file_basename + ' --- '

            # query for the presence of "peer" in the list of linkages (rel-paths) inside of the "outer-loop" dylib:
            command = 'otool -L "' + outer_dylib + '" | grep   "' + inner_file_basename_01 + '" | grep version | awk \'{print $1}\''
            found_link = os.popen( command ).read().rstrip()

            if found_link != '':

                print '           --- Inside ' + outer_file_basename + ' found ' + found_link + '. (A) Proceeding to fix this Mach-O rel-path --- '

                command =  str('install_name_tool -change "' + found_link +
                               '" "@executable_path/' + inner_file_basename_01 + '" "' + outer_dylib + '"')

                run_os_command_expecting_zero_output( command )

            # now query using 02 (inner_file_basename_02)
            command = 'otool -L "' + outer_dylib + '" | grep   "' + inner_file_basename_02 + '" | grep version | awk \'{print $1}\''
            found_link = os.popen( command ).read().rstrip()

            if found_link != '':

                print '           --- Inside ' + outer_file_basename + ' found ' + found_link + '. (B) Proceeding to fix this Mach-O rel-path --- '

                # IMPORTANT: we correct it to inner_file_basename_01 ( one! ) even though we found 02
                command =  str('install_name_tool -change "' + found_link +
                               '" "@executable_path/' + inner_file_basename_01 + '" "' + outer_dylib + '"')

                run_os_command_expecting_zero_output( command )

    print " --- mach-o_dylib_fixer.sh: END SCRIPT --- "
