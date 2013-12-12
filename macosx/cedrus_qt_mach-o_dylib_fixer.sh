#!/bin/bash

# This script "fixes" the "install name id" and also the various Mach-O rel-paths of dylibs.

# When we say "fix" we mean that absolute paths are changed to paths like @executable_path/libNAME.dylib

# ARGUMENT ONE [required] -- the path to your target dir
# ARGUMENT TWO [optional] -- set to anything you like; the mere presence of the second arg enables verbose output

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



if [ -n "$1" ]
then

        echo " --- mach-o_dylib_fixer.sh: BEGIN SCRIPT --- "

        TARGET_DIR=$1

        if [ -n "$2" ]
        then
                VERBOSE="true"
        fi

        # shorten any dylib names like "*.5.1.1.dylib" so that they are simply:  *.5.dylib
        for OUTER_LOOP_LIB_FILENAME in $TARGET_DIR/*.dylib
        do
                mv "$OUTER_LOOP_LIB_FILENAME" "${OUTER_LOOP_LIB_FILENAME/.5.1.1/.5}"
        done # shortening the 5.1.1 names

        for OUTER_LOOP_LIB_FILENAME in $TARGET_DIR/*.dylib
        do

            # strip off any path, even a path as small as "./"
                OUTER_LOOP_LIB_FILENAME_BASENAME=`basename "$OUTER_LOOP_LIB_FILENAME"`

                # find the current install name id of this dylib
                OLD_ID_NAME=`otool -D "$OUTER_LOOP_LIB_FILENAME" | tail -1`

                if [ -n "$VERBOSE" ]
                then
                        echo " --- Considering $OUTER_LOOP_LIB_FILENAME --- "
                fi


                # make sure the install name id is a "fixed" one
                if [[ "$OLD_ID_NAME" != "$OUTER_LOOP_LIB_FILENAME_BASENAME" ]]
                then
                        echo "      --- Fixing install name id on $OUTER_LOOP_LIB_FILENAME_BASENAME --- "

                        SHORT_OUTER_LOOP_LIB_FILENAME=`echo ${OUTER_LOOP_LIB_FILENAME_BASENAME/.3.0.0/}`
                        SHORT_OUTER_LOOP_LIB_FILENAME=`echo ${SHORT_OUTER_LOOP_LIB_FILENAME/.3/}`
                        install_name_tool -id "@executable_path/$SHORT_OUTER_LOOP_LIB_FILENAME" "$OUTER_LOOP_LIB_FILENAME"
                fi


                # we used to do "part two" conditionally, but now just aggressively do it no matter what!

                        # PSEUDO-CODE FOR SECOND PORTION OF THIS ROUTINE:
                        #
                        #         For each dylib in this folder (i.e. "for each PEER of the outer-loop file"):
                        #         {
                        #                        If the list of linkages inside outer-loop-file CONTAINS a reference to peer:
                        #                        {
                        #                                Ensure that the linkage is a fixed reference.
                        #                        }
                        #         }
                        for INNER_LOOP_LIB_FILENAME in $TARGET_DIR/*.dylib
                        do
                                # strip off any path, even as small a path as "./"
                                INNER_LOOP_LIB_FILENAME_BASENAME=`basename "$INNER_LOOP_LIB_FILENAME"`

                                if [ -n "$VERBOSE" ]
                                then
                                        echo "      --- Checking for link to $INNER_LOOP_LIB_FILENAME_BASENAME in $OUTER_LOOP_LIB_FILENAME --- "
                                fi


                                # query for the presence of "peer" in the list of linkages (rel-paths) inside of the "outer-loop" dylib:
                                FOUND_LINK=`otool -L "${OUTER_LOOP_LIB_FILENAME}" | grep   "${INNER_LOOP_LIB_FILENAME_BASENAME}" | grep version | awk '{print $1}'`

                                # strip of any whitespace so that our "-n" test (for empty string) will work
                                FOUND_LINK=`echo ${FOUND_LINK/ /}`

                                # if the linkage is present in the list, then make sure it is "fixed"
                                if [ -n "$FOUND_LINK" ]
                                then

                                                echo "           --- Inside $OUTER_LOOP_LIB_FILENAME_BASENAME found $FOUND_LINK. Proceeding to fix this Mach-O rel-path --- "

                                                SHORT_INNER_LOOP_LIB_FILENAME=`echo ${INNER_LOOP_LIB_FILENAME_BASENAME/.3.0.0/}`
                                                SHORT_INNER_LOOP_LIB_FILENAME=`echo ${SHORT_INNER_LOOP_LIB_FILENAME/.3/}`

                                                install_name_tool -change "$FOUND_LINK" "@executable_path/$SHORT_INNER_LOOP_LIB_FILENAME" "$OUTER_LOOP_LIB_FILENAME"
                                fi
                        done # done with "Portion Two", the Inner Loop

        done # done processing the input folder (folder given in argument one to this script)

        echo " --- mach-o_dylib_fixer.sh: END SCRIPT --- "

else
        echo "****************************** This script requires one argument. ******************************"
        false # terminates our script with an ERROR value
fi
