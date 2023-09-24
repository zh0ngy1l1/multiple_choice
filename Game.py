import Questions
import pygame
import textwrap

class Game:
    def __init__(self, questions_dir: str):
        pygame.init()
        
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (172, 172, 172)
        self.FONT = pygame.font.Font(None, 36)
        
        self.BUTTONWIDTH, self.BUTTONHEIGHT = 400, 200
        
        self.questions = Questions.Questions(dir=questions_dir)
        
        # Create a window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Multiple Choice: " +  questions_dir)
        
        
        
    def run_game_loop(self) -> None:
        '''
        main game loop
        '''
        
        definition, options = self.questions.generate_prompt()
        
        self.running = True
        while self.running:
            for event in pygame.event.get():
                choice = self.handle_event(event)
                if choice >= 0:
                    print(self.questions.check_choice(choice))
                    definition, options = self.questions.generate_prompt()
            self.render(definition, options)
            pygame.display.flip()


        pygame.quit()
        return None
    
    
    def draw_definition(self, definition: str):
        '''
        Function to draw definition with text wrapping
        '''
        rect = pygame.Rect(10, 10, 780, 180)
        
        # Wrap the text to fit inside the rectangle
        wrapped_text = textwrap.fill(definition, width=60)

        lines = wrapped_text.split('\n')
        line_height = self.FONT.get_linesize()

        y = rect.top
        for line in lines:
            text_surface = self.FONT.render(line, True, self.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (rect.centerx, y)
            self.screen.blit(text_surface, text_rect)
            y += line_height
        return None
    
    
    def render(self, definition: list, options: list) -> None:
        '''
        renders the screen and definition and options.
        does not flip.
        '''
        
        
        self.screen.fill(self.WHITE)
        
        pygame.draw.rect(
                    self.screen, self.GREY, (0, self.BUTTONHEIGHT, self.BUTTONWIDTH * 2, self.BUTTONHEIGHT * 2)
                )
        
        for col in range(2):
            for row in range(2):
                x = col * self.BUTTONWIDTH
                y = row * self.BUTTONHEIGHT + 200

                pygame.draw.rect(
                    self.screen, self.WHITE, (x, y, self.BUTTONWIDTH, self.BUTTONHEIGHT), width=5
                )
                
                option_text = self.FONT.render(options[col + 2 * row], True, self.BLACK)
                self.screen.blit(option_text, (x + 50, y + 50))
                
        self.draw_definition(definition)

        return None
    
    def handle_event(self, event: pygame.event.Event) -> int:
        '''
        Returns the choice the player made. -1 if player did not make any.
        '''
        if event.type == pygame.QUIT:
            self.running = False
        
        if event.type == pygame.KEYDOWN:
            k: int = event.key
            if k >= 49 and k <= 52: #1234 -> 0123
                return k - 49
            elif k >= 97 and k <= 100: #abcd -> 0123
                return k - 97
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y >= 200:
                return mouse_x // self.BUTTONWIDTH + ((mouse_y - 200)// self.BUTTONHEIGHT) * 2    
        return -1
        