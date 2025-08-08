#####################################################################
# author:  Kylie 
# date:    5-12-25
# description: 
#####################################################################
import pygame
from random import randint
from constants import *

class Wizard(pygame.sprite.Sprite):

    def __init__(self):
        super(Wizard,self).__init__()
        """image with resizing and measurements of dimensions"""
        self.original_image = pygame.image.load('wizard.png').convert_alpha()
        self.image_width = self.original_image.get_width()
        self.image_height = self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (self.image_width // 2.5, self.image_height // 2.5))
        self.rect = self.image.get_rect()

        self.lasers_group = pygame.sprite.Group()

    def update(self, pressed_keys):
        """when a key is pressed instructions are given if it is the right key"""
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            laser = Laser(self)
            self.lasers_group.add(laser)

        """makes sure the player does not go off screen"""
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def original_position(self):
        """starts the player off in the bottom middle position"""
        bottom_middle_x = WIDTH // 2 - self.image_width//4
        bottom_middle_y = HEIGHT - self.image.get_height()
        return((bottom_middle_x, bottom_middle_y))
    
class Spider(pygame.sprite.Sprite):

    def __init__(self):
        super(Spider, self).__init__()
        """image with resizing and measurements of dimensions; speed of which the spiders move"""
        self.original_image = pygame.image.load('spider.png').convert_alpha()
        self.image_width = self.original_image.get_width()
        self.image_height = self.original_image.get_height()
        self.image = pygame.transform.scale(self.original_image, (self.image_width // 4, self.image_height // 4))
        self.rect = self.image.get_rect(center=(0, self.image.get_height()-50))
        self.speed = randint(1,7)

    def update(self):
        """gives the direction of the spiders: left to right"""
        self.rect.move_ip(self.speed,0)

class Laser(pygame.sprite.Sprite):
    def __init__(self, wizard):
        super(Laser,self).__init__()
        """rectangle with measurements of dimensions; speed of which the lasers move"""
        self.surf = pygame.Surface((2,20))
        self.surf.fill(("SeaGreen2"))
        laser_x = wizard.rect.centerx
        laser_y = wizard.rect.top
        self.rect = self.surf.get_rect(midbottom=(laser_x,laser_y))
    
        self.speed = 5

    def update(self):
        """moves the lasers upward and when they go above the limit of the screen they are killed off"""
        self.rect.move_ip(0,-self.speed)
        if self.rect.top < 0:
            self.kill()
        
            
###########################################################################################################
pygame.init()

"""sound effects created"""
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("spider_hit.wav")
laser_sound = pygame.mixer.Sound("reg_laser_shot.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

title_font = pygame.font.SysFont("Impact", 50)
reg_font = pygame.font.SysFont("Courier New",20)

"""screen display is set"""
screen = pygame.display.set_mode((WIDTH,HEIGHT))

"adds clock"""
clock = pygame.time.Clock()

"""initializes the wizard class and starts calls on the origianl_position function to set the starting position"""
wizard = Wizard()
wizard.rect.topleft = wizard.original_position()

"""used to add lasers when player hits space"""
ADDLASER = pygame.USEREVENT + 1
lasers = pygame.sprite.Group()

"""groups the sprites together to make it easier for other features like deleting"""
spiders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(wizard)
all_sprites.add(lasers)

start_screen = True

"""start screen before playing game"""
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start_screen = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start_screen = False
            elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
                start_screen = False
                running = True
    screen.fill("Slategray4")
    start_screen_text = title_font.render("Start?", True, "SeaGreen1")
    play_text = reg_font.render("Press SPACE to shoot. Use the left and right arrow keys to move. Kill all of the spiders!", True, (BLACK))
    begin_text = reg_font.render("""PRESS "SPACE" OR "S" TO BEGIN""",True, (BLACK))

    screen.blit(start_screen_text, (WIDTH//2 - start_screen_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2 + 10))
    screen.blit(begin_text, (WIDTH//2 - begin_text.get_width()//2, HEIGHT//2 + 60))

    pygame.display.flip()


"""variables altered when in the while running loop"""
escaped_spiders = 0
score = 0
hearts = 5
message = ""
message_start_time = 0
bonus_triggered = False
bonus_display_duration = 2000
hit_spiders = 0
wave_number = 1
spider_each_wave = 1

"""plays the game"""
while running:
    """if a certain key is pressed something will happen, it just defines what happens and implements it"""
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                new_laser = Laser(wizard)
                lasers.add(new_laser)
                all_sprites.add(new_laser)
                laser_sound.play()

        elif event.type == QUIT:
            running = False
    
    """updates the wizard sprite"""
    pressed_keys = pygame.key.get_pressed()
    wizard.update(pressed_keys)

    """updates the spider sprite and redefines some variables"""
    spiders.update()
    for spider in list(spiders):
        if spider.rect.right >= WIDTH:
            spider.kill()
            escaped_spiders += 1
            hearts -= 1
            if hearts <= 0:
                running = False
                game_over = True
                game_over_sound.play()

    """checks if any lasers hit the spiders and kills the sprite of the spider and laser if so; add to score"""
    for laser in lasers:
        hit_spider = pygame.sprite.spritecollideany(laser,spiders)
        if hit_spider:
            hit_spider.kill()
            laser.kill()
            hit_spiders += 1
            score += 15
            hit_sound.play()

    """displays text; shows hearts left and points total"""
    text = f"Hearts: {hearts}   Points: {score}"
    text_surface = reg_font.render(text, True, (WHITE))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (WIDTH - 10, HEIGHT - 10)

    """adds a bonus to the score for every 5 spiders shot"""
    if hit_spiders % 5 == 0 and score != 0 and not bonus_triggered:
        message = "+Bonus"
        message_start_time = pygame.time.get_ticks()
        score += 75
        bonus_triggered = True
    
    lasers.update()

    """set background to an image instead of just a color"""
    background_image = pygame.transform.scale(pygame.image.load("spooky_setting.jpg").convert(), (WIDTH, HEIGHT))
    screen.blit(background_image, (0,0))

    """displays the spiders"""
    for entity in spiders:
        screen.blit(entity.image, entity.rect)

    """displays the lasers"""
    for entity in lasers:
        screen.blit(entity.surf, entity.rect)
    
    """displays the wizard"""
    screen.blit(wizard.image, wizard.rect)

    """displays the text"""
    screen.blit(text_surface,text_rect)
    
    """makes the bonus text appear for two seconds and then disappears"""
    if message and pygame.time.get_ticks() - message_start_time < 2000:
        message_surface = reg_font.render(message, True, WHITE)
        message_rect = message_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(message_surface, message_rect)
    else:
        message = ""
    if pygame.time.get_ticks() -message_start_time >= bonus_display_duration:
        bonus_triggered = False

    """if there are no spiders on the screen more is added"""
    
    if len(spiders) == 0:
        wave_number += 1
        spider_each_wave += 1
        for _ in range(spider_each_wave):
            new_spider = Spider()
            spiders.add(new_spider)
            all_sprites.add(new_spider)

    pygame.display.flip()

"""displays game over screen"""
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                hit_spiders = 0
                escaped_spiders = 0
                hearts = 5
                spiders.empty()
                lasers.empty()
                wizard.rect.topleft = wizard.original_position()
                game_over = False
                running = True
            elif event.key == pygame.K_ESCAPE:
                game_over = False
    screen.fill("Slategray4")
    game_over_text = title_font.render("GAME OVER", True, "tomato1")
    restart_text = reg_font.render("Press ESC to Quit", True, (BLACK))

    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()

pygame.quit()
