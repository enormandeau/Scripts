#!/bin/bash
# Automatically create and send weekly report

# Create report
markers_extract_to_screen.py ~/Dropbox/Lab/daily_plan.txt "#BEGIN WEEKLY REPORT" "#END WEEKLY REPORT" > ~/Desktop/weekly_report.txt

# Get password
read -s -p "Email password: " account_password

# Send report by email
for i in louis.bernatchez@bio.ulaval.ca eric.normandeau@bio.ulaval.ca
do
    gmailsend.py \
        eric.normandeau.qc@gmail.com \
        $i \
        "Rapport hebdomadaire" \
        ~/Desktop/weekly_report.txt \
        $account_password
done

# Change name of file to contain date (yyyy-mm-dd)
cd ~/Desktop/
datify.sh weekly_report.txt

# Move report to ~/Documents/weekly_reports/YEAR
mkdir ~/Documents/weekly_reports/$(date +%Y) 2> /dev/null
mv *_weekly_report.txt ~/Documents/weekly_reports/$(date +%Y)

