#!/bin/bash

# Usage: ftp_add_user.sh USERNAME

# TODO
# - Generate password
# - create user
# - remove examples.desktop
# - copy ftp_files
# - change permission
   #- only read

USER=$1
PASSWD=$(pwgen -c -N 1 -n 8)

echo "THIS SCRIPT DOES NOTHING EXCEPT PRINTING"
echo "---"
echo "Adding user $USER to ftp users"
echo "With password: $PASSWD"
#sudo useradd -p $PASSWD

