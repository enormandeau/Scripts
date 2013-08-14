#!/bin/bash
# Automatically create and send weekly report

# Create report
markers_extract_to_screen.py ~/Dropbox/Lab/daily_plan.txt "#BEGIN WEEKLY REPORT" "#END WEEKLY REPORT" > ~/Desktop/weekly_report.txt

# Change name of file to contain date (yyyy-mm-dd)
cd ~/Desktop/
datify.sh weekly_report.txt

# Send report by email
# TODO

# Move report to ~/Documents/weekly_reports/YEAR
mkdir ~/Documents/weekly_reports/$(date +%Y) 2> /dev/null
cp *_weekly_report.txt ~/Documents/weekly_reports/$(date +%Y)

# TODO Change cp to mv when auto-mail-send implemented 
#mv *_weekly_report.txt ~/Documents/weekly_reports/$(date +%Y)

