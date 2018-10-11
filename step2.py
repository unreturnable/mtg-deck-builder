# Import all our needed modules
import os
import re
import pickle
from random import shuffle

# The path to our deck files
decks_path = './decks'

# Lists for storing results
deck_lists = []
all_cards = []
processed_deck_lists = []

# Regex for scraping the number of each card in a deck
num_finder = re.compile('[0-9]*')

# Get all the files in the decks dir
for file in os.listdir(decks_path):
    deck_list = []

    # Open each decks file
    with open(decks_path + '/' + file) as file:
        # Read the file, spliting on newline characters
        deck_list = file.read().splitlines()
        deck_lists.append(deck_list)

    # Loop through the decks cards to build a list of all the cards played
    for card in deck_list:
        # Check for empty string leftover when we removed newline characters
        if card != '':
            # Get the cards name
            all_cards.append(re.sub('[0-9]*', '', card)[1:])

# Filter the list of cards to be unique
all_cards = sorted(set(all_cards))

# Loop through all the previously loaded deck lists
for deck_list in deck_lists:
    processed_deck_list = []

    # Loop through each card in the deck
    for card in deck_list:
        # Check for empty string leftover when we removed newline characters
        if card != "":
            # Get the total number of this card the deck runs
            number_of = int(num_finder.findall(card)[0])
            # Get the cards ID number from the all_cards list
            card_id = all_cards.index(re.sub('[0-9]*', '', card)[1:])

            # Create a list with a value for each copy of the card the deck runs
            for x in range(0, number_of):
                processed_deck_list.append(card_id)

    # Ignore decks that are not 75 cards in size (60 mainboard + 15 sideboard)
    # This makes life way easier with the LSTM
    if len(processed_deck_list) == 75:
        processed_deck_lists.append(processed_deck_list)
        # Create 9 Shuffled versions of the decks as well
        for i in range(0, 9):
            processed_deck_lists.append(shuffle(processed_deck_list))

# Save the all_cards list for later use
with open('cards_lists.pkl', 'wb') as fp:
    pickle.dump(all_cards, fp)

# Save the processed_deck_lists for later use
with open('deck_lists.pkl', 'wb') as fp:
    pickle.dump(processed_deck_lists, fp)
