import sys
import pygame
from Menu import Menu
from Snake import Snake
from Food import Food

CELL_SIZE = 15  # Storleken på varje cell i pixlar
GRID_SIZE = 21  # Antal celler i varje riktning
SCREEN_SIZE = CELL_SIZE * GRID_SIZE # Definierar storleken på fönstret i pixlar
SCORE = 0 # Variabel som håller koll på poängen
SCORE_MULTIPLIER = 1 # Variabel som håller koll på poängmultiplikatorn
GAME_SPEED = 10 # Variabel som håller koll på spelets hastighet
LEVEL = 1


class Game: # Klassen som hanterar spelet
    def __init__(self, board_size=GRID_SIZE): 
        pygame.display.set_caption("Snake") 
        self.score = 0;
        self.level = 1;
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
        self.food = Food(self) # Skapar mat
        self.snake = Snake(self.game_board, self.food) # Skapar en orm
        self.clock = pygame.time.Clock() # Skapar en klocka
        self.game_speed = 10
        self.start = False # Variabel som håller koll på om spelet har startat eller inte
    
    def update_gamespeed(self): # Funktion som uppdaterar spelets hastighet
        self.game_speed = 8 + self.difficulty*5 * self.level*0.1 # TODO: remember to tune this
        
    
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
        
    def draw_score_level(self):
        font = pygame.font.Font(None, 36)  # Choose the font for the text
        score_text = font.render(f"Score: {self.score}", True, (176,196,222))  # Create the score text
        level_text = font.render(f"Level: {self.level}", True, (176,196,222))  # Create the level text

        # Draw the score and level text
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
                        
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
                elif self.game_board[i][j] == 2: # Ormens Huvud
                    pygame.draw.rect(self.screen, (72, 61, 139), inner_rect, 0)
                elif self.game_board[i][j] == 3: # Ormens Kropp
                    pygame.draw.rect(self.screen, (0, 0, 128), inner_rect, 0)
                elif self.game_board[i][j] == 5: # Maten
                    pygame.draw.circle(self.screen, (0, 255, 0), inner_rect.center, inner_rect.width//2)
                elif self.game_board[i][j] == 6: # Specialmaten
                    pygame.draw.circle(self.screen, (255, 0, 0), inner_rect.center, inner_rect.width//2)
                else:  
                    pygame.draw.rect(self.screen, (47, 79, 79), inner_rect, 0)
        
    def run(self): # Huvudloopen för spelet
        choice = None
        while choice != "Start":
            self.menu.display()
            pygame.display.flip()
            choice = self.menu.handle_input()
        
        self.draw_grid()   
        self.draw_score_level()  
        pygame.display.flip()

        while self.running: 
            for event in pygame.event.get():
                print("Event")
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]: 
                        self.start = True
                        self.update_gamespeed()
                        print("Game started")
                        print(self.DIFFICULTY[self.difficulty])
                        print(self.BORDERS[self.borders])
                        self.snake.set_direction(event.key)

            if self.start:  # Only update the game state and draw the grid if the game has started
                    
                self.draw_grid()  
                self.draw_score_level() 
                pygame.display.flip()  # Uppdaterar fönstret
                
                self.clock.tick(self.game_speed)  
                if not self.food.exists:
                    self.food.spawn_food()
                    
            self.snake.move()

        pygame.quit()  # Stänger ner pygame
        
        
def main():
    game = Game() 
    game.run() 
        
if __name__ == "__main__":
    main()