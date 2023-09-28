import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

        super().__init__()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('sound/latch_squelsh_thing_wet-83071.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 318:
            self.gravity = -20
            self.jump_sound.play()
            self.image = self.player_jump
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 318:
            self.rect.bottom = 318
            
    def animation_state(self):
        if self.rect.bottom < 318: 
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'water':
            water_frame1 = pygame.image.load('graphics/water/water1.png').convert_alpha()
            water_frame2 = pygame.image.load('graphics/water/water2.png').convert_alpha()
            self.frames = [water_frame1, water_frame2]
            y_pos = 210
        else:
            napkin_frame1 = pygame.image.load('graphics/snail/napkin2.png').convert_alpha()
            napkin_frame2 = pygame.image.load('graphics/snail/napkin3.png').convert_alpha()
            self.frames = [napkin_frame1, napkin_frame2]
            y_pos = 327
        
        self.animation_index = 0
        
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time//1000
    score_surf = test_font.render(str(current_time), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 327:
                screen.blit(napkin_surf, obstacle_rect)
            else:
                screen.blit(water_surf, obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 318:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runny Nose')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('sound/happy-14585.mp3')
bg_music.set_volume(0.5)
bg_music.play()

#GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/sky2.png').convert_alpha()
grass_surface = pygame.image.load('graphics/grass.png').convert_alpha()

# OBSTACLES
napkin_frame1 = pygame.image.load('graphics/snail/napkin2.png').convert_alpha()
napkin_frame2 = pygame.image.load('graphics/snail/napkin3.png').convert_alpha()
napkin_frames = [napkin_frame1, napkin_frame2]
napkin_frame_index = 0
napkin_surf = napkin_frames[napkin_frame_index]

water_frame1 = pygame.image.load('graphics/water/water1.png').convert_alpha()
water_frame2 = pygame.image.load('graphics/water/water2.png').convert_alpha()
water_frames = [water_frame1, water_frame2]
water_frame_index = 0
water_surf = water_frames[water_frame_index]

obstacle_rect_list = []

# PLAYER
player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 318))
player_gravity = 0

# INTRO SCREEN
player_stand = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 175))

game_name = test_font.render('Runny Nose', False, 'Green')
game_name_rect = game_name.get_rect(center = (400, 90))

game_message = test_font.render('Press SPACE to run', False, 'Green')
game_message_rect = game_message.get_rect(center = (400, 320))

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

napkin_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(napkin_animation_timer, 500)

water_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(water_animation_timer, 200)

while True:
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 318:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['napkin', 'water', 'napkin', 'napkin'])))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 318:
                    player_gravity = -20
                    
            if event.type == napkin_animation_timer:
                if napkin_frame_index == 0:
                    napkin_frame_index = 1
                else:
                    napkin_frame_index = 0
                napkin_surf = napkin_frames[napkin_frame_index]
                
            if event.type == water_animation_timer:
                if water_frame_index == 0:
                    water_frame_index = 1
                else:
                    water_frame_index = 0
                water_surf = water_frames[water_frame_index]
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
            
        
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(grass_surface, (0, 300))
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 318)
        player_gravity = 0
        
        score_message = test_font.render("Your score: " + str(score), False, 'Green')
        score_message_rect = score_message.get_rect(center = (400, 320))
        
        screen.blit(game_name, game_name_rect)
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)