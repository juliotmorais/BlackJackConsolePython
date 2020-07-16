import random

suitsList = ["Spades", "Hearts", "Clubs", "Diamonds"]
valuesList = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
actualValues = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
                "Jack": 10,
                "Queen": 10, "King": 10, "Ace": 11}
playing = True

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck():
    def __init__(self):
        self.deckList =[]
        for suit in suitsList:
            for value in valuesList:
                self.deckList.append(Card(suit,value))

    def __str__(self):
        for card in self.deckList:
            print (card.__str__())

    def shuffleDeck(self):
        random.shuffle(self.deckList)

    def deal(self):
        return self.deckList.pop()

class Hand():
    def __init__(self):
        self.cardsInHand = []
        self.handValue = 0
        self.aces = 0

    def addCard(self,card):
        self.cardsInHand.append(card)
        self.handValue += actualValues[card.value]
        if card.value=="Ace":
            self.aces +=1

    def adjustForAce(self):
        while self.handValue>21 and self.aces:
            self.handValue-=10
            self.aces-=1

class Chips():
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
    def winBet(self):
        self.total+=self.bet
    def loseBet(self):
        self.total-=self.bet

def takeBet(chips):
    while True:
        try:
            chips.bet= int(input("How many chips would you like to bet?"))
        except:
            print("Please type in a numerical amount of chips.")
        else:
            if chips.bet > chips.total:
                print(f"Not enough chips. You have {chips.total}")
            else:
                break

def hit(deck,hand):
    hand.addCard(deck.deal())
    hand.adjustForAce()

def hitOrStay(deck,hand):
    global playing
    while True:
        x=input("Hit or Stay? Type 'h' or 's'")
        if x[0].lower()=="h":
            hit(deck,hand)
        elif x[0].lower()=="s":
            print("Player Stays")
            playing = False
        else:
            "Sorry, I didn't understand, Hit or stand? Type 'h' or 's'"
            continue
        break

def showCards(playerHand, dealerHand):
    print("\nPlayer's Hand:", *playerHand.cardsInHand, sep='\n ')
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealerHand.cardsInHand[1])

def showAllCards(playerHand,dealerHand):
    print("\nPlayer's Hand:", *playerHand.cardsInHand, sep='\n ')
    print("Player's Hand =",playerHand.handValue)
    print("\nDealer's Hand:", *dealerHand.cardsInHand, sep='\n ')
    print("Dealer's Hand =",dealerHand.handValue)

def playerBusts(player,dealer,chips):
    print("Player Busts!")
    chips.loseBet()

def playerWins(player,dealer,chips):
    print("Player Wins!")
    chips.winBet()

def dealerBusts(player,dealer,chips):
    print("Dealer Busts! Player Wins!")
    chips.winBet()

def dealerWins(player,dealer,chips):
    print("Dealer Wins!")
    chips.loseBet()

def push(player,dealer):
    print("Dealer and player are tied! PUSH!")

while True:
    print("Welcome to the Game! Take a seat!")
    gameDeck = Deck()  ##initialize deck
    gameDeck.shuffleDeck()  # shuffle the deck

    playerHand = Hand()
    dealerHand = Hand()
    playerChips = Chips()

    dealerHand.addCard(gameDeck.deal())
    playerHand.addCard(gameDeck.deal())
    dealerHand.addCard(gameDeck.deal())
    playerHand.addCard(gameDeck.deal())

    takeBet(playerChips)

    showCards(playerHand,dealerHand)

    while playing:
        hitOrStay(gameDeck,playerHand)

        showCards(playerHand, dealerHand)

        if playerHand.handValue >21:
            playerBusts(playerHand,dealerHand,playerChips)
            break

    if playerHand.handValue <= 21:
        while dealerHand.handValue < 17:
            hit(gameDeck,dealerHand)

        showAllCards(playerHand,dealerHand)

        if dealerHand.handValue >21:
            dealerBusts(playerHand, dealerHand, playerChips)
        elif dealerHand.handValue > playerHand.handValue:
            dealerWins(playerHand, dealerHand, playerChips)
        elif dealerHand.handValue < playerHand.handValue:
            playerWins(playerHand, dealerHand, playerChips)
        else:
            push(playerHand,dealerHand)

    print("Player, you have {} chips".format(playerChips.total))
    newGame = input("Want to play again?")
    if newGame[0].lower() =="y":
        playing = True
        continue
    else:
        print("Thank you for playing")
        break
