'''
WARNING!

This script crawls the mtgoldfish website. They probably won't be to happy if lots
of people start running it at once. A populated copy of the ./decks directory is
included with this repository. Consider just training on this version of the metagame
before running this script to get a new dataset. Not only is it's nicer on their site
it also saves you the 30 minutes this script roughly takes to run.

Remember kids, always web crawl responsibly!
'''

# Import all our needed modules
import requests
import os
import shutil
from bs4 import BeautifulSoup

# Delete the existing decks dir
decks_path = './decks'

if os.path.isdir(decks_path):
    shutil.rmtree(decks_path)

# Create new decks dir
os.makedirs(decks_path)

# Log some pretty progress text
print("\n")
print("\n")
print("Starting up web crawl. We will be going to www.mtggoldfish.com")
print("--------------------------------------------------------------")

# Fetch the metagame page for Modern
# In theory we could change the value for different formats
req = requests.get('https://www.mtggoldfish.com/metagame/modern/full#paper')

# Convert response to searchable HTML
html = BeautifulSoup(req.text, 'html.parser')

# More pretty progress text
print("HTML retrived. Processing deck lists")

# Find all instances of a <span> tag that have the class "deck-price-paper"
decks = html.findAll("span", {"class": "deck-price-paper"})

# Loop through the returned instances
for deck in decks:
    # Check to make sure these instances contain a link
    if deck.a is not None:
        deck_link = deck.a['href']

        # Check the link isn't to another format
        # This can be hardcoded for now but updates to the page should be watched for
        if deck_link != "/metagame/standard/full#paper":
            # Pretty print the decks meta name
            print("Fetching deck lists for: " + deck_link[18:-12])

            # Get the page for this decks meta version
            deck_html = requests.get('https://www.mtggoldfish.com/' + deck_link)
            deck_html = BeautifulSoup(deck_html.text, 'html.parser')

            print(" Finding deck versions")

            # Find all versions of this deck
            versions = deck_html.findAll("span", {"class": "deck-price-paper"})

            # Loop through all versions
            for version in versions:
                # Check for link
                if version.a is not None:
                    version_link = version.a['href']
                    print("     Downloading version: " + version_link[6:-6])

                    # Grab the deck list
                    deck_list = requests.get('https://www.mtggoldfish.com/deck/download/' + version_link[6:-6])

                    # Write deck list to file
                    f = open(decks_path + '/' + deck_link[18:-12] + '_' + version_link[6:-6], "a")
                    f.write(deck_list.text)
                    f.close()

# Output a message to notify the user of completion
print("--------------------------------------------------------------")
print("Done fetching all deck lists.")
print("Output can be found in: " + decks_path)
