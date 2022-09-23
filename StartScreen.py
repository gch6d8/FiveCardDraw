import pygame, sys
import time
import ctypes
from pygame.locals import *
from match import *
import AI
#import textBasedMatch

#Colors for various objects
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

#Declare music variables
SONG_END = pygame.USEREVENT + 1 #Define song end event value
playlist = ['hedge_your_bets.mp3', 'lukewarm_hazy.mp3', 'remember_september.mp3', 'three_wise_people.mp3', 'walk_through_the_park.mp3']
cur_song = None

class Button:
    def __init__(self, xpos, ypos, width, height, color, text, updateDisplay = True):
        self.xpos = xpos
        self.ypos = ypos
        self.height = height
        self.width = width
        if color == 0:
            self.color = 0
            return
        self.color = color
        self.text = text
        if updateDisplay:
            self.drawButton()
        else:
            self.drawButtonWithoutUpdate()

    def isInButton(self, x,y):
        return ((x > self.xpos) & (x < self.xpos+self.width)) & ((y > self.ypos) & (y < self.ypos+self.height))
    def drawButton(self):
        pygame.draw.rect(gameDisplay, self.color,(self.xpos,self.ypos,self.width,self.height))
        smallText = pygame.font.SysFont("freesansbold",20) 
        textSurf, textRect = text_objects(self.text, smallText)
        textRect.center = ( (self.xpos+(self.width/2)), (self.ypos+(self.height/2)) )
        gameDisplay.blit(textSurf, textRect)
        pygame.display.update()
    def drawButtonWithoutUpdate(self):
        pygame.draw.rect(gameDisplay, self.color,(self.xpos,self.ypos,self.width,self.height))
        smallText = pygame.font.SysFont("freesansbold",20) 
        textSurf, textRect = text_objects(self.text, smallText)
        textRect.center = ( (self.xpos+(self.width/2)), (self.ypos+(self.height/2)) )
        gameDisplay.blit(textSurf, textRect)
    def changeColor(self):
        if self.color != 0:
            if self.color == red:
                self.color = bright_red
            elif self.color == bright_red:
                self.color = red
            elif self.color == green:
                self.color = bright_green
            elif self.color == bright_green:
                self.color = green
            self.drawButton()

pygame.init()#initilize pygame

curButtons = []#the buttons which are currently displayed on the screen

#Load card front image files
ace_club = pygame.image.load('visualAssets/card_fronts/ace_club.png')
ace_diamond = pygame.image.load('visualAssets/card_fronts/ace_diamond.png')
ace_heart = pygame.image.load('visualAssets/card_fronts/ace_heart.png')
ace_spade = pygame.image.load('visualAssets/card_fronts/ace_spade.png')
two_club = pygame.image.load('visualAssets/card_fronts/two_club.png')
two_diamond = pygame.image.load('visualAssets/card_fronts/two_diamond.png')
two_heart = pygame.image.load('visualAssets/card_fronts/two_heart.png')
two_spade = pygame.image.load('visualAssets/card_fronts/two_spade.png')
three_club = pygame.image.load('visualAssets/card_fronts/three_club.png')
three_diamond = pygame.image.load('visualAssets/card_fronts/three_diamond.png')
three_heart = pygame.image.load('visualAssets/card_fronts/three_heart.png')
three_spade = pygame.image.load('visualAssets/card_fronts/three_spade.png')
four_club = pygame.image.load('visualAssets/card_fronts/four_club.png')
four_diamond = pygame.image.load('visualAssets/card_fronts/four_diamond.png')
four_heart = pygame.image.load('visualAssets/card_fronts/four_heart.png')
four_spade = pygame.image.load('visualAssets/card_fronts/four_spade.png')
five_club = pygame.image.load('visualAssets/card_fronts/five_club.png')
five_diamond = pygame.image.load('visualAssets/card_fronts/five_diamond.png')
five_heart = pygame.image.load('visualAssets/card_fronts/five_heart.png')
five_spade = pygame.image.load('visualAssets/card_fronts/five_spade.png')
six_club = pygame.image.load('visualAssets/card_fronts/six_club.png')
six_diamond = pygame.image.load('visualAssets/card_fronts/six_diamond.png')
six_heart = pygame.image.load('visualAssets/card_fronts/six_heart.png')
six_spade = pygame.image.load('visualAssets/card_fronts/six_spade.png')
seven_club = pygame.image.load('visualAssets/card_fronts/seven_club.png')
seven_diamond = pygame.image.load('visualAssets/card_fronts/seven_diamond.png')
seven_heart = pygame.image.load('visualAssets/card_fronts/seven_heart.png')
seven_spade = pygame.image.load('visualAssets/card_fronts/seven_spade.png')
eight_club = pygame.image.load('visualAssets/card_fronts/eight_club.png')
eight_diamond = pygame.image.load('visualAssets/card_fronts/eight_diamond.png')
eight_heart = pygame.image.load('visualAssets/card_fronts/eight_heart.png')
eight_spade = pygame.image.load('visualAssets/card_fronts/eight_spade.png')
nine_club = pygame.image.load('visualAssets/card_fronts/nine_club.png')
nine_diamond = pygame.image.load('visualAssets/card_fronts/nine_diamond.png')
nine_heart = pygame.image.load('visualAssets/card_fronts/nine_heart.png')
nine_spade = pygame.image.load('visualAssets/card_fronts/nine_spade.png')
ten_club = pygame.image.load('visualAssets/card_fronts/ten_club.png')
ten_diamond = pygame.image.load('visualAssets/card_fronts/ten_diamond.png')
ten_heart = pygame.image.load('visualAssets/card_fronts/ten_heart.png')
ten_spade = pygame.image.load('visualAssets/card_fronts/ten_spade.png')
jack_club = pygame.image.load('visualAssets/card_fronts/jack_club.png')
jack_diamond = pygame.image.load('visualAssets/card_fronts/jack_diamond.png')
jack_heart = pygame.image.load('visualAssets/card_fronts/jack_heart.png')
jack_spade = pygame.image.load('visualAssets/card_fronts/jack_spade.png')
queen_club = pygame.image.load('visualAssets/card_fronts/queen_club.png')
queen_diamond = pygame.image.load('visualAssets/card_fronts/queen_diamond.png')
queen_heart = pygame.image.load('visualAssets/card_fronts/queen_heart.png')
queen_spade = pygame.image.load('visualAssets/card_fronts/queen_spade.png')
king_club = pygame.image.load('visualAssets/card_fronts/king_club.png')
king_diamond = pygame.image.load('visualAssets/card_fronts/king_diamond.png')
king_heart = pygame.image.load('visualAssets/card_fronts/king_heart.png')
king_spade = pygame.image.load('visualAssets/card_fronts/king_spade.png')


#Get the dimensions of the user's screen
user32 = ctypes.windll.user32

#determine whether we should display in fullscreen or windowed mode
if user32.GetSystemMetrics(0) == 1600 and user32.GetSystemMetrics(1) == 900:
    #fullscreen mode
    display_width = user32.GetSystemMetrics(0)
    display_height = user32.GetSystemMetrics(1)
    #Displays a fullscreen window that is white
    gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
    display_width = 1600
    display_height = 900
    #display in windowed mode
    gameDisplay = pygame.display.set_mode((display_width, display_height))

#Card dimensions
cardOffset = 10
cardSizex = 100
cardSizey = 140
cardx = (display_width / 2) - ((5 * (cardSizex + cardOffset))/2) #Will allow hand to be displayed in the middle
cardy = 700

#Displays a fullscreen window that is white
gameDisplay.fill(white)
clock = pygame.time.Clock()

#Object created for making text
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def getCardFile(card):
    if card.cardValue == 14:
        if card.suit == "CLUB":
            return ace_club
        elif card.suit == "DIAMOND":
            return ace_diamond
        elif card.suit == "HEART":
            return ace_heart
        else:
            return ace_spade
    elif card.cardValue == 2:
        if card.suit == "CLUB":
            return two_club
        elif card.suit == "DIAMOND":
            return two_diamond
        elif card.suit == "HEART":
            return two_heart
        else:
            return two_spade
    elif card.cardValue == 3:
        if card.suit == "CLUB":
            return three_club
        elif card.suit == "DIAMOND":
            return three_diamond
        elif card.suit == "HEART":
            return three_heart
        else:
            return three_spade
    elif card.cardValue == 4:
        if card.suit == "CLUB":
            return four_club
        elif card.suit == "DIAMOND":
            return four_diamond
        elif card.suit == "HEART":
            return four_heart
        else:
            return four_spade
    elif card.cardValue == 5:
        if card.suit == "CLUB":
            return five_club
        elif card.suit == "DIAMOND":
            return five_diamond
        elif card.suit == "HEART":
            return five_heart
        else:
            return five_spade
    elif card.cardValue == 6:
        if card.suit == "CLUB":
            return six_club 
        elif card.suit == "DIAMOND":
            return six_diamond 
        elif card.suit == "HEART":
            return six_heart 
        else:
            return six_spade 
    elif card.cardValue == 7:
        if card.suit == "CLUB":
            return seven_club
        elif card.suit == "DIAMOND":
            return seven_diamond
        elif card.suit == "HEART":
            return seven_heart
        else:
            return seven_spade
    elif card.cardValue == 8:
        if card.suit == "CLUB":
            return eight_club 
        elif card.suit == "DIAMOND":
            return eight_diamond
        elif card.suit == "HEART":
            return eight_heart 
        else:
            return eight_spade 
    elif card.cardValue == 9:
        if card.suit == "CLUB":
            return nine_club 
        elif card.suit == "DIAMOND":
            return nine_diamond
        elif card.suit == "HEART":
            return nine_heart 
        else:
            return nine_spade
    elif card.cardValue == 10:
        if card.suit == "CLUB":
            return ten_club 
        elif card.suit == "DIAMOND":
            return ten_diamond 
        elif card.suit == "HEART":
            return ten_heart 
        else:
            return ten_spade 
    elif card.cardValue == 11:
        if card.suit == "CLUB":
            return jack_club 
        elif card.suit == "DIAMOND":
            return jack_diamond 
        elif card.suit == "HEART":
            return jack_heart 
        else:
            return jack_spade 
    elif card.cardValue == 12:
        if card.suit == "CLUB":
            return queen_club
        elif card.suit == "DIAMOND":
            return queen_diamond 
        elif card.suit == "HEART":
            return queen_heart 
        else:
            return queen_spade 
    elif card.cardValue == 13:
        if card.suit == "CLUB":
            return king_club
        elif card.suit == "DIAMOND":
            return king_diamond 
        elif card.suit == "HEART":
            return king_heart 
        else:
            return king_spade 

def otherHands(numPlayers): #needs if left, top, and right are still in

    cardBackImg = pygame.image.load('visualAssets/card_backSmall.png')
    rotCard = pygame.image.load('visualAssets/rotated_card.png')
    
    for x in range(5):
        if numPlayers == 2:
            gameDisplay.blit(cardBackImg, (cardx + x * (cardSizex + cardOffset), 20))#top side
        elif numPlayers == 3:
            gameDisplay.blit(rotCard, (1415, 160 + x * (cardSizex + cardOffset)))#right side
            gameDisplay.blit(rotCard, (20, 160 + x * (cardSizex + cardOffset)))#left side
        elif numPlayers == 4:
            gameDisplay.blit(cardBackImg, (cardx + x * (cardSizex + cardOffset), 20))#top side
            gameDisplay.blit(rotCard, (1415, 160 + x * (cardSizex + cardOffset)))#right side
            gameDisplay.blit(rotCard, (20, 160 + x * (cardSizex + cardOffset)))#left side

def displayHand(hand, selectedCards,needsButton, hidden):
    displayCard(cardx, cardy - selectedCards[0]*50, getCardFile(hand.getCard(0)),needsButton, hidden)
    displayCard(cardx + cardSizex + cardOffset, cardy - selectedCards[1]*50, getCardFile(hand.getCard(1)),needsButton,hidden)
    displayCard(cardx + 2*(cardSizex + cardOffset), cardy - selectedCards[2]*50, getCardFile(hand.getCard(2)),needsButton,hidden)
    displayCard(cardx + 3*(cardSizex + cardOffset), cardy - selectedCards[3]*50, getCardFile(hand.getCard(3)),needsButton,hidden)
    displayCard(cardx + 4*(cardSizex + cardOffset), cardy - selectedCards[4]*50, getCardFile(hand.getCard(4)),needsButton,hidden)

def displayCard(x,y,cf,needsButton,hidden): #Needs current player's turn to hide cards of other players
    if hidden:
        cardBackImg = pygame.image.load('visualAssets/card_backSmall.png')
        gameDisplay.blit(cardBackImg,(x,y))
    else:
        gameDisplay.blit(cf,(x,y))
    if needsButton:
        curButtons.append(Button(x, y, 100, 140,0,""))#0

def quitgame():
    pygame.quit()
    sys.exit()

def rungame(minBet, anteAmount, players, AIplayers):
    #pygame.screen.fill(white)
    gameDisplay.fill(white)
    backImg = pygame.image.load('visualAssets/table.png')
    gameDisplay.blit(backImg, (0,0))
    curButtons.clear()
    pygame.display.update()

    #run the match
    m = Match(minBet,anteAmount,players)
    while (m.state != State.WIN_BY_FOLD and m.state != State.END):
        if m.state == State.ANTE:
            x = ante(m, AIplayers[m.curPlayerTurn])#get move_____________________________________________________anteUp(m, AIplayers[m.curPlayerTurn])-> bool
            if x == True:
                m.anteUp(m.curPlayerTurn)
            else:
                m.fold(m.curPlayerTurn)
        elif m.state == State.BET1:
            #get bet
            x = bet(m, AIplayers[m.curPlayerTurn])#get bet_____________________________________bet(m, AIplayers[m.curPlayerTurn])-> int (-1 fold, -2 check)

            if x == -1:
                m.fold(m.curPlayerTurn)    
            elif x == -2:
                m.check(m.curPlayerTurn)
            else:# the player wants to bet
                m.bet(m.curPlayerTurn, x)
        elif m.state == State.TRADE:
            x = trade(m, AIplayers[m.curPlayerTurn])#get trade_____________________________________trade(m, AIplayers[m.curPlayerTurn])-> int list of card indexes to trade
            m.trade(m.curPlayerTurn, x)
        elif m.state == State.BET2:
            x = bet(m, AIplayers[m.curPlayerTurn])#get bet_____________________________________bet(m, AIplayers[m.curPlayerTurn])-> int (-1 fold, -2 check)
            if x == -1:
                m.fold(m.curPlayerTurn)
            elif x == -2:
                m.check(m.curPlayerTurn)
            else:# the player wants to bet
                m.bet(m.curPlayerTurn, x)
    
    m.endMatch()#ends the match and distributes the cash

    endScreen(m)#display end screen

def endScreen(m: Match):
    curButtons.clear()
    gameDisplay.fill(white)
    backImg = pygame.image.load('visualAssets/table.png')
    gameDisplay.blit(backImg, (0,0))
    largeText = pygame.font.SysFont('freesansbold',72)
    TextSurf, TextRect = text_objects("The winner is: " + m.getWinningPlayer(m.players).name +" with " +str(m.getWinningPlayer(m.players).money)+ " chips!", largeText)
    TextRect.center = (display_width/2,(display_height/6))
    gameDisplay.blit(TextSurf, TextRect)
    
    chips = pygame.mixer.Sound('audioAssets/end_screen.wav')
    chips.play()

    displayHandAtHeight(m.getWinningPlayer(m.players).hand,display_height/4)

    count = 0
    for i in m.players:
        if(not i.hasFolded):
            if(not i == m.getWinningPlayer(m.players)):
                count += 1
                displayHandAtHeight(i.hand, display_height/4+(count*cardSizey+75))
                TextSurf, TextRect = text_objects(i.name + ": ", largeText)
                TextRect.midright = (display_width / 2 - 300, display_height/4+(count*cardSizey+145))
                gameDisplay.blit(TextSurf,TextRect)

                TextSurf, TextRect = text_objects("Balance: " +str(i.money) + ".", largeText)
                TextRect.midleft = (display_width / 2 + 300, display_height/4+(count*cardSizey+145))
                gameDisplay.blit(TextSurf,TextRect)
    pygame.display.update()

    x = waitForMouseUP()
    newGame(m)

def trade(m: Match, aiLevel: int) -> int:
    selectedCards = [False,False,False,False,False]
    hidden = True

    tradeSound = pygame.mixer.Sound('audioAssets/deal.wav')

    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                playDifferentSong()

        numSelected = 0
        for x in selectedCards:
            if x:
                numSelected += 1
        gameDisplay.fill(white)
        backImg = pygame.image.load('visualAssets/table.png')
        gameDisplay.blit(backImg, (0,0))
        largeText = pygame.font.SysFont('freesansbold',72)
        if aiLevel == 0:
            TextSurf, TextRect = text_objects("Trade phase (select up to 3)!", largeText)
            TextRect.center = (display_width/2,display_height/2)
            gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + "'s turn!", largeText)
        TextRect.center = (display_width/2,200)

        gameDisplay.blit(TextSurf, TextRect)
        curButtons.clear()
        
        numPlayers = getPlayers(m)
        otherHands(numPlayers)
        #curBalance(m)
        if aiLevel ==0:
            displayHand(m.players[m.curPlayerTurn].hand, selectedCards, True, hidden)#0-4


            curButtons.append(Button( 3*display_width/4-50, 2*display_height/3-25, 100, 50, red, "Trade"))#5
            if hidden:
                curButtons.append(Button(cardx-110, cardy, 100, 50, red, "View Hand"))#6
            else:
                curButtons.append(Button(cardx-110, cardy, 100, 50, green, "Hide Hand"))#6
            pygame.display.update()

            x = waitForButtonClick()
            if x >= 0 and x < 5:
                tradeSound.play()
                if selectedCards[x]:
                    selectedCards[x] = not selectedCards[x]
                elif numSelected < 3:
                    selectedCards[x] = not selectedCards[x]
            elif x == 5:
                l = []
                for i in range(5):
                    if selectedCards[i]:
                        l.append(i)
                return l
            elif x == 6:
                hidden = not hidden
        else:
            if aiLevel ==1:
                cards = AI.randomAIDraw(m.players[m.curPlayerTurn])
            else:
                cards = AI.smartAIDraw(m.players[m.curPlayerTurn])
            TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + " traded cards: " + str(cards[0:3]), largeText)
            TextRect.center = (display_width/2,display_height/2)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            time.sleep(3)
            return cards[0:3]

def bet(m: Match, aiLevel: int) -> int:
    selectedCards = [False,False,False,False,False]
    amount = 0
    hidden = True
    curButtons.clear()

    betSound = pygame.mixer.Sound('audioAssets/bet.wav')
    invalidChange = pygame.mixer.Sound('audioAssets/error1.wav')
    invalidSubmit = pygame.mixer.Sound('audioAssets/error2.wav')

    while True:
        backImg = pygame.image.load('visualAssets/table.png')
        gameDisplay.blit(backImg, (0,0))
        largeText = pygame.font.SysFont('freesansbold',72)
        TextSurf, TextRect = text_objects("Current Call: " + str(m.curBet) + "    Your cur bet: " + str(amount + m.amountBetThisRound[m.curPlayerTurn]), largeText)
        TextRect.center = (display_width/2,(display_height/2-100))
        gameDisplay.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + "'s turn!", largeText)
        TextRect.center = (display_width/2,200)
        gameDisplay.blit(TextSurf,TextRect)

        numPlayers = getPlayers(m)
        otherHands(numPlayers)

        for event in pygame.event.get():
            if event.type == SONG_END:
                playDifferentSong()
        
        displayHand(m.players[m.curPlayerTurn].hand, selectedCards,False, hidden)
        curBalance(m)

        if aiLevel == 0:
            curButtons.append(Button(display_width/2-50, display_height/2+25, 100, 50, green,"Enter Bet", False))#0
            curButtons.append(Button(display_width/2-150, display_height/2-75, 100, 50, green, "Bet + 1", False))#1
            curButtons.append(Button(display_width/2-150, display_height/2-25, 100, 50, red, "Bet - 1", False))#2
            curButtons.append(Button(display_width/2-50, display_height/2-75, 100, 50, green, "Bet + 5", False))#3
            curButtons.append(Button(display_width/2-50, display_height/2-25, 100, 50, red,"Bet - 5", False))#4
            curButtons.append(Button(display_width/2+50, display_height/2-75, 100, 50, green,"Bet + 10", False))#5
            curButtons.append(Button(display_width/2+50, display_height/2-25, 100, 50, red, "Bet - 10", False))#6
            curButtons.append(Button(display_width/2-150, display_height/2+25, 100, 50, red, "Fold", False))#7
            if m.lastPlayerChecked:
                curButtons.append(Button(display_width/2+50, display_height/2+25, 100, 50, red, "Check", False))#8
            if hidden:
                curButtons.append(Button(cardx-110, cardy, 100, 50, red, "View Hand", False))#9
            else:
                curButtons.append(Button(cardx-110, cardy, 100, 50, green, "Hide Hand", False))#9
            
            pygame.display.update()

            x = waitForButtonClick()
            if x == 0 and amount + m.amountBetThisRound[m.curPlayerTurn] >= m.curBet:
                return amount
            elif x == 0 and amount + m.amountBetThisRound[m.curPlayerTurn] < m.curBet:
                invalidSubmit.play()
                pygame.draw.rect(gameDisplay,red,(display_width/2-400, display_height/2-200, 800, 400))
                textSurf, textRect = text_objects('Bet must be at least ' + str(m.curBet), largeText)
                textRect.center = (display_width/2,display_height/2 )
                gameDisplay.blit(textSurf, textRect)
                pygame.display.update()
                waitForMouseUP()
            if x == 1 and amount + m.amountBetThisRound[m.curPlayerTurn] < m.players[m.curPlayerTurn].money:
                betSound.play()
                amount += 1
            elif x == 1 and amount + m.amountBetThisRound[m.curPlayerTurn] >= m.players[m.curPlayerTurn].money:
                invalidChange.play()
            if x == 2 and amount + m.amountBetThisRound[m.curPlayerTurn]> 0:
                betSound.play()
                amount -= 1
            elif x == 2 and amount + m.amountBetThisRound[m.curPlayerTurn] == 0:
                invalidChange.play()
            if x == 3 and amount + m.amountBetThisRound[m.curPlayerTurn] + 5 <= m.players[m.curPlayerTurn].money:
                betSound.play()
                amount += 5
            elif x == 3 and amount + m.amountBetThisRound[m.curPlayerTurn] + 5 >= m.players[m.curPlayerTurn].money:
                invalidChange.play()
            if x == 4 and amount + m.amountBetThisRound[m.curPlayerTurn] > 0:
                betSound.play()
                amount -= 5
            elif x == 4 and amount + m.amountBetThisRound[m.curPlayerTurn] == 0:
                invalidChange.play()
            if x == 5 and amount + m.amountBetThisRound[m.curPlayerTurn] + 10 <= m.players[m.curPlayerTurn].money:
                betSound.play()
                amount += 10
            elif x == 5 and amount + m.amountBetThisRound[m.curPlayerTurn] + 10 >= m.players[m.curPlayerTurn].money:
                invalidChange.play()
            if x == 6 and amount + m.amountBetThisRound[m.curPlayerTurn] > 0:
                betSound.play()
                amount -= 10
            elif x == 6 and amount + m.amountBetThisRound[m.curPlayerTurn] == 0:
                invalidChange.play()
            if x == 7:
                return -1
            if x == 8 and m.lastPlayerChecked:
                return -2
            elif x == 8 and not m.lastPlayerChecked:
                hidden = not hidden
            if x == 9:
                hidden = not hidden
        else:
            if aiLevel == 1:
                bet = AI.randomAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
            else:#it is ai level 2
                bet = AI.smartAIBet(m.players[m.curPlayerTurn], m.curBet+m.players[m.curPlayerTurn].amountBet-m.amountBetThisRound[m.curPlayerTurn])
            if bet == -1:
                TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + " folded.", largeText)
                TextRect.center = (display_width/2,display_height/2)
                gameDisplay.blit(TextSurf, TextRect)
                pygame.display.update()
                time.sleep(3)
                return bet
            else:
                TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + " has bet " + str(bet), largeText)
                TextRect.center = (display_width/2,display_height/2)
                gameDisplay.blit(TextSurf, TextRect)
                pygame.display.update()
                time.sleep(3)
                return bet

#time.sleep(3) # Sleep for 3 seconds
def ante(m: Match, aiLevel: int) -> bool:
    curButtons.clear()
    gameDisplay.fill(white)
    backImg = pygame.image.load('visualAssets/table.png')
    gameDisplay.blit(backImg, (0,0))
    largeText = pygame.font.SysFont('freesansbold',72)
    medText = pygame.font.SysFont('freesansbold', 36)
    TextSurf, TextRect = text_objects("Ante Phase", largeText)
    TextRect.center = ((display_width/2),(display_height/2))

    TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + "'s turn!", largeText)
    TextRect.center = (display_width/2,180)

    gameDisplay.blit(TextSurf, TextRect)
    if aiLevel == 0:
        curButtons.append(Button(display_width/2 - 200, display_height/2 - 25, 100, 50, green,"Ante"))
        curButtons.append(Button(display_width/2 + 100, display_height/2 - 25, 100, 50, red,"Fold"))

    TextSurf, TextRect = text_objects("Ante Amount: " + str(m.anteAmount), medText)
    TextRect.center = (display_width/2,7*display_height/12)
    gameDisplay.blit(TextSurf, TextRect)

    TextSurf, TextRect = text_objects("Your Balance: " + str(m.players[m.curPlayerTurn].money), medText)
    TextRect.center = (display_width/2, 2*display_height/3)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    if aiLevel == 0:
        while True:
            for event in pygame.event.get():
                if event.type == SONG_END:
                    playDifferentSong()

            x = waitForButtonClick()
            if x == 0:
                return True
            if x == 1:
                return False
    else:
        if m.players[m.curPlayerTurn].money > m.anteAmount:
            TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + " Anted up.", largeText)
            TextRect.center = (display_width/2,display_height/2)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            time.sleep(3)
            return True#the AI always antes up
        else:
            TextSurf, TextRect = text_objects(m.players[m.curPlayerTurn].name + " folded.", largeText)
            TextRect.center = (display_width/2,display_height/2)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            time.sleep(3)
            return False

#Function for the start screen of the game
def intro():

    intro = True
    global SONG_END

    backImg = pygame.image.load('visualAssets/table.png')
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load('audioAssets/bgm/walk_through_the_park.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit()
            if event.type == SONG_END:
                playDifferentSong()

        gameDisplay.fill(white)   #Makes a white background
        gameDisplay.blit(backImg, (0,0))

        
        #Creates title text
        largeText = pygame.font.SysFont('freesansbold',115)
        TextSurf, TextRect = text_objects("Five Card Draw", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        curButtons.append(Button(display_width/3,display_height/2 + display_height/6,100,50,green,"START!"))
        curButtons.append(Button(display_width/3 + display_width/4,display_height/2 + display_height/6,100,50,red,"QUIT"))
        #curButtons.append(Button(100,100,100,50,green, "HI"))
        while True:
            x = waitForButtonClick()
            if x == 0:
                rungame(5,10,[g,ai1,t,ai2], [0, 2, 0, 1])
            if x == 1:
                quitgame()

def waitForButtonClick():
    down = waitForMouseDOWN()
    if down != -1:
        toggleButton(down)
    up = waitForMouseUP()
    if down != -1:
        toggleButton(down)
    if down == up:
        return up
    return -1#no button press

def waitForMouseUP():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            return getButton(event.pos[0], event.pos[1])

def waitForMouseDOWN():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            return getButton(event.pos[0], event.pos[1])

def toggleButton(index: int):
    curButtons[index].changeColor()


def getButton(x,y):
    for i in range(len(curButtons)):
        if curButtons[i].isInButton(x,y):
            return i
    return -1

def getPlayers(m: Match):
    numPlayers = 0
    for i in m.players:
        if not i.hasFolded:
            numPlayers += 1
    return numPlayers

def curBalance(m: Match):
    medText = pygame.font.SysFont('freesansbold', 36)
    TextSurf, TextRect = text_objects("Your Balance: " + str(m.players[m.curPlayerTurn].money), medText)
    TextRect.center = (cardx, cardy - 20)
    gameDisplay.blit(TextSurf, TextRect)
    return

def newGame(m: Match):
    curButtons.clear()
    gameDisplay.fill(white)
    backImg = pygame.image.load('visualAssets/table.png')
    gameDisplay.blit(backImg, (0,0))
    largeText = pygame.font.SysFont('freesansbold',72)

    TextSurf, TextRect = text_objects("Play again?", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    curButtons.append(Button(display_width/2 - 150, 2*display_height/3 - 25, 100, 50, green,"Yes"))
    curButtons.append(Button(display_width/2 + 50, 2*display_height/3 - 25, 100, 50, red,"No"))

    shuffleSound = pygame.mixer.Sound('audioAssets/shuffle.wav')

    pygame.display.update()

    while True:
        x = waitForButtonClick()
        if x == 0:
            shuffleSound.play()
            for i in m.players:
                i.unfold()
            rungame(5,10,m.players,[0, 2, 0, 1])
        if x == 1:
            quitgame()

def displayHandAtHeight(hand, h):
    displayCard(cardx, h, getCardFile(hand.getCard(0)),False,False)
    displayCard(cardx + cardSizex + cardOffset,h, getCardFile(hand.getCard(1)),False,False)
    displayCard(cardx + 2*(cardSizex + cardOffset),h, getCardFile(hand.getCard(2)),False,False)
    displayCard(cardx + 3*(cardSizex + cardOffset),h, getCardFile(hand.getCard(3)),False,False)
    displayCard(cardx + 4*(cardSizex + cardOffset),h, getCardFile(hand.getCard(4)),False,False)

#Play random song from bgm folder
def playDifferentSong():
    global cur_song, playlist
    BGM_DIR = 'audioAssets/bgm/'
    next = random.choice(playlist)
    while next == cur_song:
        next = random.choice(playlist)
    cur_song = next
    pygame.mixer.music.load(BGM_DIR+next)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

#load some players
STARTING_CASH = 100
g = Player("George", STARTING_CASH)
ai1 = Player("AIsmart", STARTING_CASH)
t = Player("Tom", STARTING_CASH)
ai2 = Player("AIsimple", STARTING_CASH)

intro()#start the game
pygame.quit()#quit pygame
sys.exit()