#!/bin/bash
# Create users in batch from a file of usernames and passwords
# The file is in the following format:
# user1 password
# user2 password
# ...
# userN password
#
# Usage:
#     ./addusers.sh file_with_user_info

USERFILE=$1

cat $USERFILE |
    while read i
    do
        u=$(echo $i | cut -d " " -f 1)
        p=$(echo $i | cut -d " " -f 2)
        echo "Adding: $u"
        sudo useradd -d /home/$u -g users -k /etc/skel/ -m \
            -p $(openssl passwd -crypt $p) -s /bin/bash $u
    done
