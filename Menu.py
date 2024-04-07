import pygame
pygame.init() 

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.game = game
        self.menu_options = ["Start", "Borders", "Difficulty", "Highscore", "Exit"] # Menyvalen

    def display(self): # Funktion som ritar ut menyn
        self.screen.fill((0, 0, 0))
        self.menu_items = []
        title_font = pygame.font.Font(None, 62) # Skapar en font för titeln
        title = title_font.render("SNAKE v_0.0.1", True, (220, 20, 60)) # Skapar titeln
        title_height = title.get_height() 
        option_height = self.font.render(self.menu_options[0], True, (0, 0, 0)).get_height() # Höjden på varje menyval
        spacing = 20  # Avstånd mellan varje menyval
        total_height = title_height + len(self.menu_options) * (option_height + spacing)

        title_y = (self.screen.get_height() - total_height) // 2 
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, title_y)) # Centrerar titeln
        self.screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()  # Hämtar musens position

        for i, option in enumerate(self.menu_options): # Loopar igenom varje menyval for att hitta vilken som ska markeras
            text_y = title_y + title_height + i * (option_height + spacing) + spacing   
            text_rect = pygame.Rect(self.screen.get_width() // 2, text_y, option_height, option_height)

            if i == 2:  # Difficulty option
                text = f"{option}: {self.game.DIFFICULTY[self.game.difficulty]}"
            elif i == 1:  # Borders option
                text = f"{option}: {self.game.BORDERS[self.game.borders]}"
            else:
                text = option

            if text_rect.collidepoint(mouse_pos): 
                color = (225, 225, 222)  
            else:
                color = (75, 75, 75) 

            text_rendered = self.font.render(text, True, color)  # Skapar texten för varje menyval
            text_rect = text_rendered.get_rect(center=(self.screen.get_width() // 2, text_y))
            self.screen.blit(text_rendered, text_rect) 
            self.menu_items.append((option, text_rendered, text_rect))
            
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for option, _, rect in self.menu_items:
                    if rect.collidepoint(mouse_pos):
                        if option == "Difficulty":
                            self.game.difficulty = (self.game.difficulty + 1) % len(self.game.DIFFICULTY)
                        elif option == "Borders":
                            self.game.borders = (self.game.borders + 1) % len(self.game.BORDERS)
                            self.game.update_border()
                        elif option == "Exit":
                            pygame.quit()
                        return option
        return None
            