import pygame, sys, random
#Tạo hàm cho game
def draw_floor():
    screen.blit(floor,(floor_x_pos,550))
    screen.blit(floor,(floor_x_pos+432,550))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-650))
    return top_pipe, bottom_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 668:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if fuu_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if fuu_rect.top <= -100 or fuu_rect.bottom >= 600:
        return False
    return True
def ratate_fuu(fuu1):
    new_fuu = pygame.transform.rotozoom(fuu1, -fuu_movement*3, 1)
    return new_fuu
def fuu_animation():
    new_fuu = fuu_list[fuu_index]
    new_fuu_rect = new_fuu.get_rect(center = (100,fuu_rect.centery))
    return new_fuu, new_fuu_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,70))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score:{int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,70))
        screen.blit(score_surface, score_rect)

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,668))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Russo_One.ttf',30)
#tạo biến cho game
gravity = 0.25
fuu_movement = 0
game_active = True
score = 0
#chèn bg
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#chèn fuuchan
fuu_down = pygame.image.load('assets/fuu1.png').convert_alpha()
fuu_mid = pygame.image.load('assets/fuu2.png').convert_alpha()
fuu_up = pygame.image.load('assets/fuu3.png').convert_alpha()
fuu_list= [fuu_down,fuu_mid,fuu_up] #0 1 2
fuu_index = 0
fuu = fuu_list[fuu_index]
#fuu = pygame.image.load('FileGame/assets/sheep.png').convert_alpha()
#fuu = pygame.transform.scale2x(fuu)
fuu_rect = fuu.get_rect(center = (100,334))
#tao timer cho fuu
fuuflap = pygame.USEREVENT +1
pygame.time.set_timer(fuuflap,200)
#chèn ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400]
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216,334))
#flap_sound = pygame.mixer.Sound('baa.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/baa.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                fuu_movement = 0
                fuu_movement = -5
            #    flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                fuu_rect.center = (100,334)
                fuu_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == fuuflap:
            if fuu_index < 2:
                fuu_index +=1
            else:
                fuu_index =0
            fuu, fuu_rect = fuu_animation()

    screen.blit(bg,(0,-50))
    if game_active:
        #fuu
        fuu_movement += gravity
        ratated_fuu = ratate_fuu(fuu)
        fuu_rect.centery += fuu_movement
        screen.blit(ratated_fuu,fuu_rect)
        game_active= check_collision(pipe_list)
        #ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.05
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        score_display('game over')
    #sanf
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0

    pygame.display.update()
    clock.tick(60)