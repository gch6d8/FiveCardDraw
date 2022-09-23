######################################################
##                   Imports                        ##
######################################################

import fiveCardDrawBasicClasses
import winningHand
import random

######################################################
##                   Functions                      ##
######################################################

#This is a good hand, keep it
def royalFlushDiscard(hand):
    return []

#This is a good hand, keep it
def straightFlushDiscard(hand):
    return []

#Trash the kicker if it is low
def quadsDiscard(hand):
    discards = []
    kickerIndex = -1
    values = winningHand.getValues(hand)
    l = list(values)
    for x in range(0,5):
        quads = l.count(values[x])
        if quads != 4:
            kickerIndex = x
            break
    if(values[kickerIndex] < 8):
        discards.append(kickerIndex)
    return discards

#This is a good hand, keep it
def fullHouseDiscard(hand):
    return []

#This is a good hand, keep it
def flushDiscard(hand):
    return []

#This is a good hand, keep it
def straightDiscard(hand):
    return []

#Trash the low card and the kicker
def tripsDiscard(hand):
    discards = []
    lowCardIndex, kickerIndex, kickerValue = -1, -1, -1
    values = winningHand.getValues(hand)
    l = list(values)
    for x in range(0,5):
        trips = l.count(values[x])
        if trips != 3:        
            discards.append(x)
    return discards

#Keep everything except the kicker to aim for a full house
def twoPairDiscard(hand):
    discards = []
    values = winningHand.getValues(hand)
    l = list(values)
    for x in range(0,5):
        pair = l.count(values[x])
        if pair != 2:
            discards.append(x)
            break
    return discards

#This is more complicated
def pairDiscard(hand):
    #First, get information about the hand
    discards = []
    pairValue, highValue, highValueIndex, lowValueIndex = -1, -1, -1, -1
    lowValue = 15
    values = winningHand.getValues(hand)
    l = list(values)
    suits = []
    for x in range(0,5):
        pair = l.count(values[x])
        if pair == 2:
            pairValue = values[x]
        if(hand.getCard(x).cardValue > highValue):
            highValue = hand.getCard(x).cardValue
            highValueIndex = x
        if(hand.getCard(x).cardValue < lowValue):
            lowValue = hand.getCard(x).cardValue
            lowValueIndex = x
        suits.append(hand.getCard(x).suit)
    sameSuit = 2
    sameSuitName = ''
    for x in range(0,3):
        if(sameSuit < suits.count(hand.getCard(x).suit)):
            sameSuit = suits.count(hand.getCard(x).suit)
            sameSuitName = hand.getCard(x).suit
    #If we almost have a flush, we aim to complete it
    if(sameSuit == 4):
        for x in range(0,5):
            if(hand.getCard(x).suit != sameSuitName):
                discards.append(x)
                break
    #Else if we almost have a straight, we aim to complete it
    else:
        lowStraight = [lowValue, lowValue+1, lowValue+2, lowValue+3, lowValue+4]
        highStraight = [highValue, highValue-1, highValue-2, highValue-3, highValue-4]
        actualLowStraight = set(values).intersection(lowStraight)
        actualHighStraight = set(values).intersection(highStraight)
        if(len(actualHighStraight) == 4):
            for x in range(0,5):
                if(hand.getCard(x).cardValue == pairValue):
                    discards.append(x)
                    break
        elif(len(actualLowStraight) == 4):
            for x in range(0,5):
                if(hand.getCard(x).cardValue == pairValue):
                    discards.append(x)
                    break
        #Else we discard everything but the pair
        else:
            for x in range(0,5):
                if (hand.getCard(x).cardValue != pairValue):
                    discards.append(x)
    return discards

#This is complicated as well
def junkDiscard(hand):
    #First, get information about the hand
    discards = []
    highValue, secondHighestValue, highValueIndex, secondHighestValueIndex, lowValueIndex = -1, -1, -1, -1 , -1
    lowValue = 15
    values = winningHand.getValues(hand)
    l = list(values)
    suits = []
    for x in range(0,5):
        if(hand.getCard(x).cardValue > highValue):
            highValue = hand.getCard(x).cardValue
            highValueIndex = x
        if(hand.getCard(x).cardValue < lowValue):
            lowValue = hand.getCard(x).cardValue
            lowValueIndex = x
        suits.append(hand.getCard(x).suit)
    sameSuit = 2
    sameSuitName = ''
    for x in range(0,3):
        if(sameSuit < suits.count(hand.getCard(x).suit)):
            sameSuit = suits.count(hand.getCard(x).suit)
            sameSuitName = hand.getCard(x).suit
    #If we almost have a flush, we aim to complete it
    if(sameSuit == 4):
        for x in range(0,5):
            if(hand.getCard(x).suit != sameSuitName):
                discards.append(x)
                break
    #Else if we almost have a straight, we aim to complete it
    else:
        lowStraight = [lowValue, lowValue+1, lowValue+2, lowValue+3, lowValue+4]
        highStraight = [highValue, highValue-1, highValue-2, highValue-3, highValue-4]
        actualLowStraight = set(values).intersection(lowStraight)
        actualHighStraight = set(values).intersection(highStraight)
        if(len(actualHighStraight) == 4):
            for x in range(0,5):
                if(hand.getCard(x).cardValue not in actualHighStraight):#actualHighStraight.count(hand.getCard(x).cardValue) == 0
                    discards.append(x)
                    break
        elif(len(actualLowStraight) == 4):
            for x in range(0,5):
                if(hand.getCard(x).cardValue not in actualLowStraight):#actualLowStraight.count(hand.getCard(x).cardValue) == 0
                    discards.append(x)
                    break
        #Else if we have most of a flush, we aim to complete it
        elif(sameSuit == 3):
            for x in range(0,5):
                if(hand.getCard(x).suit != sameSuitName):
                    discards.append(x)
                    break
        #If we're not close to anything, we trash the three lowest cards
        else:
            for x in range(0,5):
                if(x != highValueIndex and hand.getCard(x).cardValue > secondHighestValue):
                    secondHighestValue = hand.getCard(x).cardValue
                    secondHighestValueIndex = x
            for x in range(0,5):
                if (x != highValueIndex and x != secondHighestValueIndex):
                    discards.append(x)
    return discards

# Creates the switch statement for discarding from different hand types
discardOptions = {
    0 : junkDiscard,
    1 : pairDiscard,
    2 : twoPairDiscard,
    3 : tripsDiscard,
    4 : straightDiscard,
    5 : flushDiscard,
    6 : fullHouseDiscard,
    7 : quadsDiscard,
    8 : straightFlushDiscard,
    9 : royalFlushDiscard,
}

#Go all in
def royalFlushBet(player, currentBet):
    return player.money

#Go all in
def straightFlushBet(player, currentBet):
    return player.money

#Go all in
def quadsBet(player, currentBet):
    return player.money

#Go all in
def fullHouseBet(player, currentBet):
    return player.money

def flushBet(player, currentBet):
    x = random.randint(0,100)
    if(x<20):
        return player.money
    elif(x<50):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    else:
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet

def straightBet(player, currentBet):
    x = random.randint(0,100)
    if(x<10):
        return player.money
    elif(x<20):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    elif(x<40):
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet
    elif(x<60):
        if((player.money//3 + player.amountBet) >= currentBet):
            return player.money//3
        else:
            if(currentBet - player.amountBet > player.money*2//3 and player.amountBet < player.money//2):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<90):
        if((player.money//4 + player.amountBet) >= currentBet):
            return player.money//4
        else:
            if(currentBet - player.amountBet > player.money//2 and player.amountBet < player.money*2//3):
                return -1
            else:
                return currentBet - player.amountBet
    else:
        if(currentBet - player.amountBet > player.money//8 and player.amountBet < player.money*3//4):
            return -1
        else:
            return currentBet - player.amountBet

def tripsBet(player, currentBet):
    x = random.randint(0,100)
    if(x<5):
        return player.money
    elif(x<10):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    elif(x<25):
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet
    elif(x<35):
        if((player.money//3 + player.amountBet) >= currentBet):
            return player.money//3
        else:
            if(currentBet - player.amountBet > player.money*2//3 and player.amountBet < player.money//2):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<60):
        if((player.money//4 + player.amountBet) >= currentBet):
            return player.money//4
        else:
            if(currentBet - player.amountBet > player.money//2 and player.amountBet < player.money*2//3):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<85):
        if((player.money//8 + player.amountBet) >= currentBet):
            return player.money//8
        else:
            if(currentBet - player.amountBet > player.money//4 and player.amountBet < player.money*3//4):
                return -1
            else:
                return currentBet - player.amountBet
    else:
        if(currentBet - player.amountBet > player.money//8 and player.amountBet < player.money*3//4):
            return -1
        else:
            return currentBet - player.amountBet

def twoPairBet(player, currentBet):
    x = random.randint(0,100)
    if(x<2):
        return player.money
    elif(x<7):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    elif(x<10):
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet
    elif(x<15):
        if((player.money//3 + player.amountBet) >= currentBet):
            return player.money//3
        else:
            if(currentBet - player.amountBet > player.money*2//3 and player.amountBet < player.money//2):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<25):
        if((player.money//4 + player.amountBet) >= currentBet):
            return player.money//4
        else:
            if(currentBet - player.amountBet > player.money//2 and player.amountBet < player.money*2//3):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<45):
        if((player.money//8 + player.amountBet) >= currentBet):
            return player.money//8
        else:
            if(currentBet - player.amountBet > player.money//4 and player.amountBet < player.money*3//4):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<75):
        if((player.money//10 + player.amountBet) >= currentBet):
            return player.money//10
        else:
            if(currentBet - player.amountBet > player.money//5 and player.amountBet < player.money*4//5):
                return -1
            else:
                return currentBet - player.amountBet
    else:
        if(currentBet - player.amountBet > player.money//8 and player.amountBet < player.money*3//4):
            return -1
        else:
            return currentBet - player.amountBet

def pairBet(player, currentBet):
    x = random.randint(0,100)
    if(x<2):
        return player.money
    elif(x<7):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    elif(x<10):
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet
    elif(x<15):
        if((player.money//3 + player.amountBet) >= currentBet):
            return player.money//3
        else:
            if(currentBet - player.amountBet > player.money*2//3 and player.amountBet < player.money//2):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<25):
        if((player.money//4 + player.amountBet) >= currentBet):
            return player.money//4
        else:
            if(currentBet - player.amountBet > player.money//2 and player.amountBet < player.money*2//3):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<40):
        if((player.money//8 + player.amountBet) >= currentBet):
            return player.money//8
        else:
            if(currentBet - player.amountBet > player.money//4 and player.amountBet < player.money*3//4):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<60):
        if((player.money//10 + player.amountBet) >= currentBet):
            return player.money//10
        else:
            if(currentBet - player.amountBet > player.money//5 and player.amountBet < player.money*4//5):
                return -1
            else:
                return currentBet - player.amountBet
    else:
        if(currentBet - player.amountBet > player.money//8 and player.amountBet < player.money*3//4):
            return -1
        else:
            return currentBet - player.amountBet

def junkBet(player, currentBet):
    x = random.randint(0,100)
    if(x<5):
        return player.money
    elif(x<10):
        if((player.money*2//3 + player.amountBet) >= currentBet):
            return player.money*2//3
        else:
            return currentBet - player.amountBet
    elif(x<15):
        if((player.money//2 + player.amountBet) >= currentBet):
            return player.money//2
        else:
            return currentBet - player.amountBet
    elif(x<20):
        if((player.money//3 + player.amountBet) >= currentBet):
            return player.money//3
        else:
            if(currentBet - player.amountBet > player.money*2//3 and player.amountBet < player.money//2):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<30):
        if((player.money//4 + player.amountBet) >= currentBet):
            return player.money//4
        else:
            if(currentBet - player.amountBet > player.money//2 and player.amountBet < player.money*2//3):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<45):
        if((player.money//8 + player.amountBet) >= currentBet):
            return player.money//8
        else:
            if(currentBet - player.amountBet > player.money//4 and player.amountBet < player.money*3//4):
                return -1
            else:
                return currentBet - player.amountBet
    elif(x<65):
        if((player.money//10 + player.amountBet) >= currentBet):
            return player.money//10
        else:
            if(currentBet - player.amountBet > player.money//5 and player.amountBet < player.money*4//5):
                return -1
            else:
                return currentBet - player.amountBet
    else:
        if(currentBet - player.amountBet > player.money//8 and player.amountBet < player.money*3//4):
            return -1
        else:
            return currentBet - player.amountBet

# Creates the switch statement for betting with different hand types
betOptions = {
    0 : junkBet,
    1 : pairBet,
    2 : twoPairBet,
    3 : tripsBet,
    4 : straightBet,
    5 : flushBet,
    6 : fullHouseBet,
    7 : quadsBet,
    8 : straightFlushBet,
    9 : royalFlushBet,
}

#Function for smart AI to draw
def smartAIDraw(player):
    hand = winningHand.determineHand(player)
    return discardOptions[hand[0]](player.hand)

#Function for completely random AI to draw
def randomAIDraw(player):
    discards = []
    for x in range(0,5):
        if (random.randint(0,1)):
            discards.append(x)
    return discards

#Function for smart AI to bet
def smartAIBet(player, currentBet):
    if(player.hasFolded or player.isAllIn):
        return 0
    else:
        hand = winningHand.determineHand(player)
        return betOptions[hand[0]](player, currentBet)

#Function for completely random AI to bet
def randomAIBet(player, currentBet):
    if(player.hasFolded or player.isAllIn):
        return 0
    else:
        if((player.money + player.amountBet) > currentBet):
            return currentBet - player.amountBet
        else:
            return player.money
