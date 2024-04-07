import random

class Food:
    def __init__(self, game):
        self.game = game
        self.board = game.game_board
        self.eaten = 0; # Behöver jag ? 
        self.exists = False;
        self.special = False;

    def spawn_food(self):
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
                    self.board[x][y] = 6
                    self.special = True
                    break
            
    def eat_food(self):
        self.game.score += self.game.level
        self.eaten += 1
        self.exists = False
        
        if self.eaten % 5 == 0:
            self.game.level += 1
            print("Level up!")
            
    def eat_special_food(self):
        self.game.score += 3*self.game.level
        self.eaten += 1
        self.special = False
        print("Special food eaten!")
        