#!/bin/bash
# Script to send a reminder to those who have to clean the lab this week

# Create list
nb_people=$(wc -l ~/Documents/Menage/menage_liste.txt | cut -d " " -f 1)

head -2 ~/Documents/Menage/menage_liste.txt \
    > ~/Documents/Menage/menage_cette_semaine_temp.txt

echo Cette semaine :
cat ~/Documents/Menage/menage_cette_semaine_temp.txt

# Get password
read -s -p "Email password: " account_password
echo

cat ~/Documents/Menage/menage_eric.txt \
    ~/Documents/Menage/menage_cette_semaine_temp.txt \
    >  ~/Documents/Menage/menage_cette_semaine.txt

tail -$[ $nb_people - 2] ~/Documents/Menage/menage_liste.txt \
    > ~/Documents/Menage/menage_temp.txt

cat ~/Documents/Menage/menage_temp.txt \
    ~/Documents/Menage/menage_cette_semaine_temp.txt \
    > ~/Documents/Menage/menage_liste.txt

cat ~/Documents/Menage/menage_message_rappel_francais.txt \
    ~/Documents/Menage/menage_cette_semaine_temp.txt \
    ~/Documents/Menage/menage_message_rappel_anglais.txt \
    ~/Documents/Menage/menage_cette_semaine_temp.txt \
    > ~/Documents/Menage/menage_message_rappel_cette_semaine.txt

# Send reminder by email
cat ~/Documents/Menage/menage_cette_semaine.txt | \
    while read i
    do
        echo " -~=( Sending message to $i )=~-"
        gmailsend.py \
            eric.normandeau.qc@gmail.com \
            $i \
            "Rappel - Menage du labo" \
            ~/Documents/Menage/menage_message_rappel_cette_semaine.txt \
            $account_password
    done

