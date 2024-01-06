import random


"""
.-.
._.




1. deck of cards
2. interaction with cards
3. ~~~Game~~~  --> Draw & Stick
4. Check For Win 

"""




class deck_class:
    def __init__ (self):
        self.deck = []
        for i in range(1,5):
            for o in range(1,14):
              self.deck.append([i,o])

    def shuffle(self):
        random.shuffle(self.deck)

    def display(self):
        print(self.deck)
        
    


def main():
    deck1 = deck_class()
    deck2 = deck_class()
    deck2.shuffle()
    deck1.shuffle()
    deck1.display()


main()

