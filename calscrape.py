#! /usr/bin/env python3
# Python web scraping project for federal judicial calendars 
# Ben Hancock. v0.1: in development / no license

# Import necessary modules
from lxml import html
import re, requests, json, sys

# Open the local calendar file // NDCAL ONLY SO FAR
calfile = 'ndcal.json'

try:
    with open (calfile) as f:
        calendars = json.load(f)

except FileNotFoundError:
    print("Court calendar file not found.")
    sys.exit(1)

# Open search terms file 
keyfile = 'searchterms.json'

try:
    with open(keyfile) as g:
        searchkeys = json.load(g)

except FileNotFoundError:
    print("Keyword search file not found.")
    sys.exit(1)


# Set a variable for number of matches
word_matches = 0
judge_matches = 0
total_matches = 0

print("\n=== Keyword search results ===\n") 
# Loop through all calendars
for judge, cal_url in calendars.items():

## Check for good connection
    try:
        cal = requests.get(cal_url)
         
    except requests.exceptions.RequestException as e:
        print("*** Connection problem. Please check internet connection ***")
        print("\nReceived following error: ")
        print(e)
        sys.exit(1)

    print("\n\t>>> Judge " + judge.upper() + ":")
    
    tree = html.fromstring(cal.content)
    content = tree.xpath('//td/text()')

    # Build a list with all the entries on the website

    for keyword in searchkeys:
        
        current_key = r'\b' + keyword + r'\b' 

        # Loop through the contents searching for the calendar
        for entry in content:
            match = re.search(current_key, entry, re.IGNORECASE)
            
            if match:
                word_matches += 1
                judge_matches += 1
                total_matches += 1            
                print(entry)
                hearing_index = content.index(entry) + 1
                print(content[hearing_index])

            else:
                continue

        if word_matches > 0:
            
            # Print the results, neatly formatted
            print(str(word_matches) + " matches for \"" + keyword + "\"\n")
            # Reset match counter to 0
            word_matches = 0 

        else:
            continue
    
    if judge_matches == 0:
        print("None")

    else:
        judge_matches = 0
        continue

print("\n=== Search complete ===")

if total_matches == 0:

    print("No matches on any calendar")    

else:

    pass 

