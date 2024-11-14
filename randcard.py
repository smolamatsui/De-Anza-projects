import random
cards = {1:'ACE', 11:'JACK', 12:'QUEEN', 13:'KING'}
suits = {0:'SPADES', 1:'CLUBS', 2:'HEARTS', 3:'DIAMONDS'}
i = 0
while i < 5:
    i += 1
    card = random.randint(1,13)
    suit = random.randint(0, 3)
    if card == 1 or card >= 11:
        print(cards[card] + " of " + suits[suit])
    else: 
        print(str(card) + " of " + suits[suit])
    

