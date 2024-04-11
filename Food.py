import random
import pygame
class Food:     # Klassen för maten
    def __init__(self, game):
        self.game = game # för att hantera maten behöver vi tillgång till spelet
        self.board = game.game_board # för att kunna rita ut maten på spelplanen
        self.eaten = 0; # Variabel som håller koll på hur mycket mat som ätits så vi kan öka svårighetsgraden
        self.exists = False; # Variabel som håller koll på om maten finns på spelplanen
        self.special = False; # Variabel som håller koll på om specialmaten finns på spelplanen
        self.special_TTL = None # Variabel som håller koll på hur länge specialmaten ska existera
 
    def spawn_food(self): # Funktion som spawnar in maten på spelplanen på slumpmässig "ledig" plats
        while True:
            x = random.randint(0, len(self.board) - 1)
            y = random.randint(0, len(self.board[0]) - 1)
            if self.board[x][y] not in [1, 2, 3]:  # för att undvika att maten spawnar på ormen eller i väggar
                self.board[x][y] = 5  # Represent the food with 5 on the board
                self.exists = True
                break
            
        if self.eaten % 5 == 0 and self.eaten != 0:
            while True: 
                x = random.randint(0, len(self.board) - 1)
                y = random.randint(0, len(self.board[0]) - 1)
                if self.board[x][y] not in [1, 2, 3, 5]: # ska inte heller kunna spawna ovanpå annan mat
                    self.special_TTL = pygame.time.get_ticks() + max(500, 12000 - self.game.level * self.game.difficulty+1 * 500)
                    
                    self.board[x][y] = 6
                    self.special = True
                    break
                
    def remove_special_food(self): # Funktion som tar bort specialmaten från spelplanen
        if(self.special and pygame.time.get_ticks() > self.special_TTL):
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == 6:
                        self.board[i][j] = 0
                        self.special = False
            
    def eat_food(self): # Funktion som körs när ormen äter maten
        self.game.score += self.game.level*(self.game.difficulty+1)
        self.eaten += 1
        self.exists = False
        
        if self.eaten % 5 == 0:
            self.game.level += 1
            print("Level up!")
            
    def eat_special_food(self): # Funktion som körs när ormen äter specialmaten
        self.game.score += 5+self.game.level*(self.game.difficulty+1)
        self.eaten += 1
        self.special = False
        print("Special food eaten!")
        