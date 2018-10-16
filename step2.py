# Import all our needed modules
import os
import re
import pickle
import random

def chunk(deck):
    processed_x = []
    processed_y = []

    for idx in range(0, len(deck) - 1):
        slot_x = [-1] * 74
        slot_y = [0] * len(all_cards)

        for idx2 in range(0, idx + 1):
            slot_x[idx2] = deck[idx2]

        processed_x.append(slot_x)
        slot_y[deck[idx + 1]] = 1
        processed_y.append(slot_y)

    return processed_x, processed_y

# The path to our deck files
decks_path = './decks'

# Lists for storing results
deck_lists = []
all_cards = []
processed_deck_lists_x = []
processed_deck_lists_y = []

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
        x, y = chunk(processed_deck_list)
        processed_deck_lists_x.append(x)
        processed_deck_lists_y.append(y)
        # Create 9 Shuffled versions of the decks as well
        for i in range(0, 9):
            x, y = chunk(random.sample(processed_deck_list, len(processed_deck_list)))
            processed_deck_lists_x.append(x)
            processed_deck_lists_y.append(y)

# Save the all_cards list for later use
with open('cards_lists.pkl', 'wb') as fp:
    pickle.dump(all_cards, fp)

# Save the processed_deck_lists_x for later use
with open('deck_lists_x.pkl', 'wb') as fp:
    pickle.dump(processed_deck_lists_x, fp)

# Save the processed_deck_lists_y for later use
with open('deck_lists_y.pkl', 'wb') as fp:
    pickle.dump(processed_deck_lists_y, fp)
