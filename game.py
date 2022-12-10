import pygame as game
from sys import exit
import random



class Player(game.sprite.Sprite):
    def __init__(self):
        ''' intitializes the Player sprite class'''
        super().__init__()
        player_forward_1 = game.image.load('Wraith_03_Moving Forward_000.png').convert_alpha()
        player_forward_2 = game.image.load('Wraith_03_Moving Forward_003.png').convert_alpha()
        player_forward_3 = game.image.load('Wraith_03_Moving Forward_006.png').convert_alpha()
        player_forward_4 = game.image.load('Wraith_03_Moving Forward_009.png').convert_alpha()

        '''Player_move is a list where each index has a different image to resemble movement'''
        self.player_move = [player_forward_1, player_forward_2,player_forward_3,player_forward_4]
        self.player_index = 0
        self.gravity = 0

        self.image = self.player_move[self.player_index]
        self.rect = self.image.get_rect(topleft = (500,330))

    def player_input(self):
        '''checks for specific keypresses and then implements an increase to either x or y'''
        keys = game.key.get_pressed()

        if keys[game.K_d]:
            self.rect.x += 5
            self.player_index += 0.3

        if keys[game.K_a]:
            self.rect.x -= 5
            self.player_index += 0.3

        if keys[game.K_SPACE] and self.rect.top >= 300:
            self.gravity -= 10

        '''Move through player list for each image, index increased through key presses'''
        if self.player_index >= len(self.player_move): self.player_index = 0
        self.image = self.player_move[int(self.player_index)]

    def gravity_check(self):
        '''implements gravity by incrementing players y coordinate'''
        self.gravity += 1
        self.rect.y += self.gravity


    def position_check(self):
        '''Checks specific positions where the player is at and moves them to a specific place'''
        if self.rect.top >= 330 and (self.rect.x < 1100 and self.rect.x > 300):
            self.rect.top = 330
        if self.rect.x <= -200:
            self.rect.x = 1500
        if self.rect.x >= 1500:
            self.rect.x = -100
        if self.rect.top >= 700:
            self.rect.x = 500
            self.rect.y = 330


    def update(self):
        self.player_input()
        self.gravity_check()
        self.position_check()

class Objects(game.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        '''Set object sprites'''
        if type == 'yellowGem':
            yellowGem_1 = game.image.load('yellowGem.png')
            yellowGem_2 = game.image.load('yellowGem1.png')
            self.frames = [yellowGem_1,yellowGem_2]

        elif type == 'cyanGem':
            cyanGem_1 = game.image.load('cyanGem.png')
            cyanGem_2 = game.image.load('cyanGem1.png')
            self.frames = [cyanGem_1, cyanGem_2]

        else:
            purpleGem_1 = game.image.load('purpleGem.png')
            purpleGem_2 = game.image.load('purpleGem1.png')
            self.frames = [purpleGem_1, purpleGem_2]

        '''Changes image base on current index for all types'''
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(500,1000),random.randint(0,400)))

    def animation(self):
        '''Goes through index'''
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation()

def display_time():
    '''Keeps current game time'''
    current_time = int(game.time.get_ticks() / 1000)
    time_surf = font.render(f'Time: {current_time}', False, (255, 255, 255))
    time_rect = time_surf.get_rect(topleft=(100, 0))
    screen.blit(time_surf, time_rect)
    return current_time
def increase(total_score):
    '''Check collision and score increases'''
    if game.sprite.spritecollide(player.sprite, objects, True):
        jewel_sound = game.mixer.Sound('Jewel.mp3')
        jewel_sound.play(loops=0)
        total_score += 1
    return total_score

def display_score(total_score):
    '''Displays score'''
    current_score = total_score
    score_surf = font.render(f'Score: {current_score}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(topleft=(275, 0))
    screen.blit(score_surf, score_rect)
    return current_score


'''Game is initialized here as well as certain variables'''
game.init()
font = game.font.Font('rainyhearts.ttf', 50)
screen = game.display.set_mode((1500,600))
game.display.set_caption('Jewel Thief')
clock = game.time.Clock()
game_run = False
time = 120
score = 0
background_music = game.mixer.Sound('Funky.mp3')
background_music.play(loops = -1)

'''sets up groups for object and player'''
player = game.sprite.GroupSingle()
player.add(Player())
objects = game.sprite.Group()

'''Timer and background images'''
back_surface = game.image.load('mystical.jpg').convert()
object_timer = game.USEREVENT + 1
game.time.set_timer(object_timer,1500)
icon = game.image.load('icon.jpg').convert()
idle = game.image.load('idle.png').convert()

while True:
    '''Looks for specific event triggers'''
    for event in game.event.get():
        if event.type == game.QUIT:
            game.quit()
            exit()
        if game_run:
            '''cycles through object sprites'''
            if event.type == object_timer:
                objects.add(Objects(random.choice(['yellowGem', 'cyanGem', 'purpleGem', 'yellowGem','purpleGem', 'yellowGem'])))
        else:
            '''Starts game'''
            if event.type == game.KEYDOWN and event.key == game.K_SPACE:
                game_run = True


    if game_run:
        '''Sets up visuals for background and sprites'''
        screen.blit(back_surface,(0,0))
        screen.blit(icon,(0,0))
        screen.blit(idle, (10, 15))
        current_time = display_time()
        score = increase(score)
        total_score = display_score(score)

        player.draw(screen)
        player.update()

        objects.draw(screen)
        objects.update()
        if current_time == time:
            game_run = False
    else:
        '''screen is black till game start and end, displaying current score'''
        screen.fill((0, 0, 0))
        score_message = font.render(f'Your score: {score}', False, (255, 255, 255))
        score_message_rect = score_message.get_rect(center=(700, 200))
        screen.blit(score_message, score_message_rect)

    '''updates game display and fps set to 60'''
    game.display.update()
    clock.tick(60)