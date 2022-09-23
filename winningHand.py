######################################################
##                   Imports                        ##
######################################################

import fiveCardDrawBasicClasses

######################################################
##              Switch Functions                    ##
######################################################

# Determines if the hand is a Royal Flush
def royalFlush(hand):
    if(sameSuit(hand)):
        values = getValues(hand)

        # Determines if there is the Royal Straight
        if (14 in values) and (13 in values) and (12 in values) and (11 in values) and (10 in values):
            return (9,14)
    
    # Royal Flush was not found
    return (0,0)

# Determines if the hand is a Straight Flush
def straightFlush(hand):
    if(sameSuit(hand)):
        values = getValues(hand)

        # Grab the lowest value and see if the next four cards are in the hand
        low = getLowest(values)
        if ((low+1) in values) and ((low+2) in values) and ((low+3) in values) and ((low+4) in values):
            return (8,low+4)

    # Straight Flush was not found
    return (0,0)

# Determines if the hand is a Quads
def quads(hand):
    # Creates a list of the values in a hand
    values = getValues(hand)
    l = list(values)

    # Counts the occurences of card 1 then 2 to determine quad
    for x in range(0,2):
        quad = l.count(values[x])

        # If quad=4 return 7, else continue
        if quad == 4:
            return (7,l[x])
    
    # Quad was not found
    return (0,0)
        
# Determines if the hand is a Full House
def fullHouse(hand):
    # Creates a list of the values in a hand
    values = getValues(hand)
    l = list(values)

    # Counts the occurences of card 1, 2, then 3 to determine first set
    for x in range(0,3):
        match = l.count(values[x])

        # if match = 3, remove and check for 2
        if match == 3:
            l = removeValues(l, values[x])

            # Checks the two cards left for a pair
            if l.count(l[0]) == 2:
                return (6,values[x])
            # Returns 0 if no pair since flush might be present
            else:
                return (0,0)

        # if match = 2, remove and check for 3
        elif match == 2:
            l = removeValues(l, values[x])

            # Checks the three cards left for a triple
            if l.count(l[0]) == 3:
                return (6,l[0])
            # Returns 0 if no triple since flush might be present
            else:
                return (0,0)

    # Full House was not Found
    return (0,0)


# Determines if the hand is a Flush
def flush(hand):
    if sameSuit(hand):
        values = getValues(hand)
        l = list(values)
        return (5,getHighest(l))
    
    # Flush was not found
    return (0,0)

# Determines if the hand is a Straight
def straight(hand):
    values = getValues(hand)

    # Grab the lowest value and see if the next four cards are in the hand
    low = getLowest(values)
    if ((low+1) in values) and ((low+2) in values) and ((low+3) in values) and ((low+4) in values):
        return (4,low+4)
    
    # Straight was not found
    return (0,0)

# Determines if the hand is a Trips
def trips(hand):
    # Creates a list of the values in a hand
    values = getValues(hand)
    l = list(values)

    # Counts the occurences of card 1, 2, then 3 to determine trips
    for x in range(0,3):
        trips = l.count(values[x])

        # If trips=3 return 3, else continue
        if trips == 3:
            return (3,values[x])
    
    # Trips was not found
    return (0,0)

# Determines if the hand is a Two Pair
def twoPair(hand):
    # Creates a list of the values in a hand
    values = getValues(hand)
    l = list(values)

    # Counts the occurences of card 1, 2, 3, then 4 to determine pair
    for x in range(0,4):
        pair = l.count(values[x])

        # If pair=2 check for next pair
        if pair == 2:
            l = removeValues(l, values[x])

            # Checks the smaller list for second 
            # Takes the higher value of the two pairs
            for y in range(0,2):
                pair = l.count(l[y])

                # If pair=2 return 2, else continue
                if pair == 2:
                    if values[x] > l[y]:
                        return (2,values[x])
                    else:
                        return (2,l[y])

            # Second Pair was not found
            return (0,0)
    
    # Two Pair was not found
    return (0,0)

# Determines if the hand is a Pair
def pair(hand):
    # Creates a list of the values in a hand
    values = getValues(hand)
    l = list(values)

    # Counts the occurences of card 1, 2, 3, then 4 to determine pair
    for x in range(0,4):
        pair = l.count(values[x])

        # If pair=2 return 1, else continue
        if pair == 2:
            return (1,values[x])
    
    # Pair was not found
    return (0,0)

# Creates the switch statement for determining hand
options = {
    0 : royalFlush,
    1 : straightFlush,
    2 : quads,
    3 : fullHouse,
    4 : flush,
    5 : straight,
    6 : trips,
    7 : twoPair,
    8 : pair,
}


######################################################
##               Logic Functions                    ##
######################################################

## Determines the winning hand between the players 
def winningHand(players):
    # Gets the hands each player has
    hands = []
    for p in players:
        hands.append(determineHand(p))

    # Determines if there is a winner or tie
    index = 0
    winner = [0]
    for x in range(1,len(hands)):
        # If a hand is better than the current best hand, new best hand
        if hands[index][0] < hands[x][0]:
            index = x
            winner = [x]
        # Players have the same best hand
        elif hands[index][0] == hands[x][0]:
            winner.append(x)

    # Determines wheter a tie breaker is needed
    if len(winner) > 1:
        win = tieBreaker(hands, winner, players)
        return players[winner[win]]

    # No tie breaker
    return players[winner[0]]

## Determines the hand of a specific player
def determineHand(player):
    hand = (0,0)

    # Executes the swtich statement
    # Returns an int with a ranking for hand found
    for x in range(0,9):
        if hand[0] == 0:
            hand = options[x](player.hand)

    # Gets highest card if no other hand is found
    if hand[0] == 0:
        values = getValues(player.hand)
        l = list(values)
        hand = (0,getHighest(l))

    # Returns tuple (hand found, highest value)
    return hand

## Determines the winner in a tie breaker with same hands
def tieBreaker(hands, winners, players):
    # Assume first index is the winner
    winner = 0

    # Cycle through the other players
    for x in range(1,len(winners)):
        # If hands are the same with the same value, use the kicker to decide the winner
        if hands[winners[winner]][1] == hands[winners[x]][1]:
            temp = kickerBreaker(players, hands, winner, x)

            # If there is a new winner
            if temp != -1:
                winner = temp
            # If the kicker is the same, use a suit tie breaker
            else:
                winner = suitBreaker(players, hands[winner][1], winner, x)
        # Uses the high card of the hand to determine winner (pair of kings beat pair of 2s)
        elif hands[winners[winner]][1] < hands[winners[x]][1]:
            winner = x

    return winner

## Determines the winner in a tie breaker using the kicker
## Cases: two pair, pair
def kickerBreaker(players, hands, win1, win2):
    # Creates a list of the values to shorten hand
    values1 = getValues(players[win1].hand)
    l1 = list(values1)
    values2 = getValues(players[win2].hand)
    l2 = list(values2)

    # Use kicker to determine winner
    high1 = getHighest(l1)
    high2 = getHighest(l2)

    if high1 > high2:
        return win1
    elif high2 > high1:
        return win2

    # Kickers are the same
    return -1        

## Determines the winner in an Extra tie breaker using suits
## diamond (lowest), club, hearts, spades (highest)
def suitBreaker(players, high, win1, win2):
    # Gets the suits of the high cards of the two hands
    suits1 = getHighSuits(players[win1].hand, high)
    suits2 = getHighSuits(players[win2].hand, high)

    #print()
    #print(suits2)

    # Finds the winner and returns the index in winners
    if 'SPADE' in suits1:
        return win1
    elif 'SPADE' in suits2:
        return win2
    else:
        if 'HEART' in suits1:
            return win1
        elif 'HEART' in suits2:
            return win2
        else:
            if 'CLUB' in suits1:
                return win1
            elif 'CLUB' in suits2:
                return win2
    #print('Here I am')



######################################################
##              Helper Functions                    ##
######################################################

# Determines if all cards are the same suit
def sameSuit(hand):
    for x in range(1,5):
        # If not the same suit, return 0
        if not(hand.getCard(0).suit == hand.getCard(x).suit):
            return 0
    return 1

# Gets the values of all cards in a hand
def getValues(hand):
    values = []
    for x in range(0,5):
        values.append(hand.getCard(x).cardValue)
    return values

# Finds the lowest value in a hand
def getLowest(hand):
    low = hand[0]
    for x in range(1,5):
        if low > hand[x]:
            low = hand[x]
    return low

# Finds the highest value in a hand
def getHighest(hand):
    high = hand[0]
    for x in range(1,len(hand)):
        if high < hand[x]:
            high = hand[x]
    return high

# Removes instances of a card (Hand still has each card)
def removeValues(hand, val):
    return [value for value in hand if value != val]

## Gets the suits of the high cards for the tie breaker
def getHighSuits(hand, val):
    suits = []
    for x in range(0,5):
        if hand.getCard(x).cardValue == val:
            suits.append(hand.getCard(x).suit)
    return suits
