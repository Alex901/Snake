import sys
import pygame
from Menu import Menu

CELL_SIZE = 15  # Storleken på varje cell i pixlar
GRID_SIZE = 20  # Antal celler i varje riktning
SCREEN_SIZE = CELL_SIZE * GRID_SIZE # Definierar storleken på fönstret i pixlar
SCORE = 0 # Variabel som håller koll på poängen
SCORE_MULTIPLIER = 1 # Variabel som håller koll på poängmultiplikatorn
GAME_SPEED = 10 # Variabel som håller koll på spelets hastighet


class Game: # Klassen som hanterar spelet
    def __init__(self, board_size=GRID_SIZE): 
        self.board_size = board_size
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) # Skapar ett fönster
        self.running = True # Variabel som håller koll på om spelet körs eller inte
        self.menu = Menu(self.screen, self) # Skapar Meny-objektet
        self.DIFFICULTY = ["Easy", "Medium", "Hard","Impossible"] # Svårighetsgraderna
        self.BORDERS = ["On", "Off"] # Variabel som håller koll på om det ska finnas kanter eller inte
        self.borders = 0 # Index för borders
        self.difficulty = 0 # Index för svårgihetsgraden
        self.game_board = [[0 for _ in range(board_size)] for _ in range(board_size)] # Skapar spelplanen, skulle kunna göra en Board.py men CBA
        self.update_border() # Annars får borders inget initialvärde
        
    
    def update_border(self): # Funktion som uppdaterar om det ska finnas kanter eller inte
        if self.borders == 0:
            for i in range(self.board_size):
                self.game_board[0][i] = 1 
                self.game_board[self.board_size - 1][i] = 1
                self.game_board[i][0] = 1
                self.game_board[i][self.board_size - 1] = 1
        else:
            for i in range(self.board_size):
                self.game_board[0][i] = 0
                self.game_board[self.board_size - 1][i] = 0
                self.game_board[i][0] = 0
                self.game_board[i][self.board_size - 1] = 0
        
        for row in self.game_board:
            print(row)
            
        print()
                        
    def draw_grid(self): # Funktion som ritar ut spelplanen
        for i in range(self.board_size):
            for j in range(self.board_size):
                x = i * CELL_SIZE
                y = j * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)

                inner_rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                if self.game_board[i][j] == 1:  
                    pygame.draw.rect(self.screen, (255, 255, 255), inner_rect, 0)
                else:  
                    pygame.draw.rect(self.screen, (47, 79, 79), inner_rect, 0)
        
    def run(self): # Huvudloopen för spelet
        choice = None
        while choice != "Start":
            self.menu.display()
            pygame.display.flip()
            choice = self.menu.handle_input()

        print("choice ", str(choice))

        if choice == "Exit":
            pygame.quit()
            
        else:
            while self.running: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                self.draw_grid()   
                pygame.display.flip()  # Uppdaterar fönstret

        pygame.quit()  # Stänger ner pygame
        
        
def main():
    game = Game() # Skapar ett objekt av klassen Game
    game.run() # Kör spelet
        
if __name__ == "__main__":
    main()