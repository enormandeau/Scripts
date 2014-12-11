#!/bin/bash

# Delete users in batch from a file of usernames and passwords
# The file is in the following format:
# user1 password
# user2 password
# ...
# userN password
#
# Usage:
#     ./delusers.sh file_with_user_info

USERFILE=$1

cat $USERFILE |
    while read i
    do
        u=$(echo $i | cut -d " " -f 1)
        p=$(echo $i | cut -d " " -f 2)
        echo "Removing: $u"
        sudo userdel $u
        sudo rm -rf /home/$u
    done
