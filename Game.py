import sys
import pygame
from Menu import Menu
from Snake import Snake
from Food import Food

CELL_SIZE = 15  # Storleken på varje cell i pixlar
GRID_SIZE = 31  # Antal celler i varje riktning
SCREEN_SIZE = CELL_SIZE * GRID_SIZE # Definierar storleken på fönstret i pixlar
SCORE = 0 # Variabel som håller koll på poängen
SCORE_MULTIPLIER = 1 # Variabel som håller koll på poängmultiplikatorn
GAME_SPEED = 10 # Variabel som håller koll på spelets hastighet
LEVEL = 1


class Game: # Klassen som hanterar spelet 
    def __init__(self, board_size=GRID_SIZE):   # Konstruktor    
        pygame.display.set_caption("Snake")     # Sätter titeln för fönstret till Snake
        self.score = 0; # Variabel som håller koll på poängen
        self.level = 1; # Variabel som håller koll på vilken nivå spelaren är på
        self.board_size = board_size # Storleken på spelplanen
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))   # Skapar fönstret med definierad storlek
        self.running = True 
        self.menu = Menu(self.screen, self)  # Skapar en huvudmenyn
        self.DIFFICULTY = ["Easy", "Medium", "Hard","Impossible"] 
        self.BORDERS = ["On", "Off"] 
        self.borders = 0    # Denna är nog överflödig
        self.difficulty = 0  
        self.game_board = [[0 for _ in range(board_size)] for _ in range(board_size)]  # Skapar spelmatrisen
        self.update_border()  # Uppdaterar om det ska finnas kanter eller inte
        self.food = Food(self) # Skapar klassen för maten
        self.snake = Snake(self.game_board, self.food)  # Skapar ormen
        self.clock = pygame.time.Clock()  # Skapar en klocka för att hålla koll på spelets hastighet
        self.start = False 
    
    def update_gamespeed(self):     # Funktion som uppdaterar spelets hastighet
        self.game_speed = 8 + self.difficulty*8 * self.level*0.2 
        
    
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
        font = pygame.font.Font(None, 36)  # ritar ut poäng och nivå
        score_text = font.render(f"Score: {self.score}", True, (176,196,222))  
        level_text = font.render(f"Level: {self.level}", True, (176,196,222))  

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
                        
    def draw_grid(self): # Funktion som ritar ut spelplanen baserat på spelmatrisen
        for i in range(self.board_size):
            for j in range(self.board_size):
                x = i * CELL_SIZE
                y = j * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (76, 187, 23), rect, 1) # Ritar ut rutnätet

                inner_rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                if self.game_board[i][j] == 1:      # Stenväggarna
                    pygame.draw.rect(self.screen, (189, 180, 169), inner_rect, 0)
                elif self.game_board[i][j] == 2: # Ormens Huvud
                    pygame.draw.rect(self.screen, (0, 0, 128), inner_rect, 0)
                elif self.game_board[i][j] == 3: # Ormens Kropp
                    pygame.draw.rect(self.screen, (72, 61, 139), inner_rect, 0)
                elif self.game_board[i][j] == 5: # Maten
                    pygame.draw.circle(self.screen, (0, 255, 0), inner_rect.center, inner_rect.width//2)
                elif self.game_board[i][j] == 6: # Specialmaten
                    pygame.draw.circle(self.screen, (255, 0, 0), inner_rect.center, inner_rect.width//2)
                else:   # Tom cell = "gärs"
                    pygame.draw.rect(self.screen, (34,139,34), inner_rect, 0)
        
    def run(self): # Huvudloopen för spelet
        choice = None   # För att hålla spelaren i menyn ända tills spelaren väljer "starta"
        while choice != "Start":
            self.menu.display()
            pygame.display.flip()
            choice = self.menu.handle_input()
        
        self.draw_grid()   
        self.draw_score_level()  
        pygame.display.flip() # Uppdaterar fönstret

        while self.running:     # Huvudloopen för själva spelet
            for event in pygame.event.get():   # Loopar igenom alla händelser som sker
                if event.type == pygame.QUIT:  # Så man kan stänga ner spelet
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Om en tangent trycks ner
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]: # Om det är en riktningstangent = börja spelet
                        self.start = True
                        self.update_gamespeed()
                        self.snake.set_direction(event.key)

            if self.start: # Om spelet har startat     
                self.draw_grid()  
                self.draw_score_level() 
                pygame.display.flip()  # Uppdaterar fönstret
                
                self.clock.tick(self.game_speed)  # Uppdaterar klockan
                if not self.food.exists: # Om det inte finns någon mat på spelplanen
                    self.food.spawn_food() # Skapa ny mat
                    
            self.snake.move()   # Flytta ormen         

        pygame.quit()  # Stänger ner pygame
        
        
def main():
    game = Game() 
    game.run() 
        
if __name__ == "__main__":
    main()