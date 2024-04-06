import sys
import pygame
from Menu import Menu

CELL_SIZE = 15  # Storleken på varje cell i pixlar
GRID_SIZE = 32  # Antal celler i varje riktning
SCREEN_SIZE = CELL_SIZE * GRID_SIZE # Definierar storleken på fönstret i pixlar



class Game: # Klassen som hanterar spelet
    def __init__(self): 
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) # Skapar ett fönster
        self.running = True # Variabel som håller koll på om spelet körs eller inte
        self.menu = Menu(self.screen) # Skapar Meny-objektet


            
    def draw_grid(self): # Funktion som ritar ut 
        for x in range(0, SCREEN_SIZE, CELL_SIZE): 
            for y in range(0, SCREEN_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)
                
                if x == 0 or y == 0 or x == SCREEN_SIZE - CELL_SIZE or y == SCREEN_SIZE - CELL_SIZE: # Om det är en kantcell
                    inner_rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2) 
                    pygame.draw.rect(self.screen, (255, 255, 255), inner_rect, 0)  
                else: # Om det inte är en kantcell
                    inner_rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2) 
                    pygame.draw.rect(self.screen, (47, 79, 79), inner_rect, 0)
        
    def run(self): # Huvudloopen för spelet
        choice = None
        while choice is None:
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