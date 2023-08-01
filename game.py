
from itertools import count
from secrets import choice
import sys, random
import pygame

def draw_floor():
    screen.blit(floor, (floor_x_pos, 600))
    screen.blit(floor, (floor_x_pos + 432, 600))

def draw_floor_hard_mode():
    screen.blit(floor_hard_mode, (floor_x_hard_mode_pos, 620))
    screen.blit(floor_hard_mode, (floor_x_hard_mode_pos + 1000, 620))

def draw_floor_hard_mode_red():
    screen.blit(floor_hard_mode_red, (floor_x_hard_mode_red_pos, 620))
    screen.blit(floor_hard_mode_red, (floor_x_hard_mode_red_pos + 1000, 620))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe_rect = pipe_surface.get_rect(midtop = (800, random_pipe_pos))
    top_pipe_rect = pipe_surface.get_rect(midtop = (800, random_pipe_pos - 700))
    return bot_pipe_rect, top_pipe_rect

def create_gold_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe_gold_rect = pipe_gold_surface.get_rect(midtop = (800, random_pipe_pos))
    top_pipe_gold_rect = pipe_gold_surface.get_rect(midtop = (800, random_pipe_pos - 700))
    return bot_pipe_gold_rect, top_pipe_gold_rect

def create_red_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe_red_rect = pipe_red_surface.get_rect(midtop = (800, random_pipe_pos))
    top_pipe_red_rect = pipe_red_surface.get_rect(midtop = (800, random_pipe_pos - 700))
    return bot_pipe_red_rect, top_pipe_red_rect

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx  -= 5
    return pipes

def move_hard_mode_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 7
    return pipes

def move_pipe_red(pipes):
    for pipe in pipes:
        pipe.centerx -= 7
    return pipes

def move_pipe_y(pipes, count_pipe, cmt, random_pos):
    for i in range(0, len(pipes)):
        if i in random_pos:
            if count_pipe < 100:
                pipes[i].centery -= 1
                count_pipe += 20
                cmt = count_pipe
            elif cmt <= 100:
                pipes[i].centery += 1
                cmt -= 20
                if cmt == 0:
                    count_pipe = 0
    return pipes

def draw_pipe(pipes, index, index_red_pipe):
    for i in range(0, len(pipes)):
        if pipes[i].bottom >= 600:
            if i in index:
                screen.blit(pipe_gold_surface, pipes[i])
            elif i in index_red_pipe:
                screen.blit(pipe_red_surface, pipes[i])
            else:
                screen.blit(pipe_surface, pipes[i])
        else:
            if i in index:
                flip_pipe = pygame.transform.flip(pipe_gold_surface, False, True)
            elif i in index_red_pipe:
                flip_pipe = pygame.transform.flip(pipe_red_surface, False, True)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipes[i])

def check_collision(pipes, index):
    for i in range(0, len(pipes)):
        if i not in index and bird_rect.colliderect(pipes[i]):
            hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 600:
        hit_sound.play()
        return False
    return True

def check_collision_basic_mode(pipes, index, index_red_pipe): 
    for i in range(0, len(pipes)):
        if (i not in index) and (i not in index_red_pipe) and (bird_rect.colliderect(pipes[i])):
            hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 600:
        hit_sound.play()
        return False
    return True

def rotte_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_move * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (270, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (270, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (270, 584))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def create_sliver_coin():
    random_height_coin = random.choice(pipe_height)
    bot_coin_rect = sliver_coin.get_rect(midbottom = (600, random_height_coin))
    return bot_coin_rect

def create_gold_coin():
    random_height_coin = random.choice(pipe_height1)
    bot_coin_rect = gold_coin.get_rect(midbottom = (600, random_height_coin))
    return bot_coin_rect

def move_coin(coins):
    for coin in coins:
        coin.centerx -= 5
    return coins

def draw_sliver_coin(coins):
    for coin in coins:
        screen.blit(sliver_coin, coin)

def draw_gold_coin(coins):
    for coin in coins:
        screen.blit(gold_coin, coin)

def sliver_coin_animation():
    new_coin = sliver_coin_list[sliver_index]
    new_coin_rect = new_coin.get_rect(midbottom  = (600, 600))
    return new_coin, new_coin_rect 

def gold_coin_animation():
    new_coin = gold_coin_list[gold_index]
    new_coin_rect = new_coin.get_rect(midbottom = (600, 600))
    return new_coin, new_coin_rect

def check_coin_sliver_collision(coins):
    for coin in coins:
        if bird_rect.colliderect(coin):
            score_sound.play()
            return False      # xóa xu
    return True               # không làm gì

def check_coin_gold_collision(coins):
    for coin in coins:
        if bird_rect.colliderect(coin):
            score_sound.play()
            return False      # xóa xu
    return True  

def result(coins):
    for coin in coins:
        if bird_rect.colliderect(coin):
            return coin

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen = pygame.display.set_mode((600, 768))  # tạo cửa sổ cho game
clock = pygame.time.Clock()                   # điều chỉnh tốc độ của game
game_font = pygame.font.Font('04B_19.ttf', 40)

#tạo các biến cho game
gravity = 0.25
bird_move = 0
game_active = True
score = 0
high_score = 0
index = []      # luu vi tri gold pipe trong pipe list
index1 = []     # luu vi tri gold pipe trong pipe list in hard mode
hard_mode = False
hard_mode_red = False
check = []      # kiem tra gold pipe va cham voi chim trong basic mode
tmp_pos = 0
check1 = []     # kiem tra gold pipe va cham voi chim trong hard mode
count_pipe = 0       # dem chu ki di chuyen cot len xuong
cmt = 0         # dem chu ki di chuyen cot len xuong

remove_sliver_coin = True    # biến kiểm tra chim va chạm đến xu bac
remove_gold_coin = True    # biến kiểm tra chim va chạm đến xu vang

# tạo background
bg = pygame.image.load("assets/background-night.png").convert()
bg = pygame.transform.scale(bg, (700, 768))

# tạo sàn
floor = pygame.image.load("assets/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

floor_hard_mode = pygame.image.load("assets/cloud.png").convert_alpha()
floor_hard_mode = pygame.transform.scale(floor_hard_mode, (1050, 100))
floor_x_hard_mode_pos = -100

floor_hard_mode_red = pygame.image.load("assets/cloud.png").convert_alpha()
floor_hard_mode_red = pygame.transform.scale(floor_hard_mode_red, (1050, 100))
floor_x_hard_mode_red_pos = -100

#tạo chim
bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))

bird_list = [bird_down, bird_mid, bird_up]
bird_index = int(0)
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))

#thời gian chim thay đổi trạng thái cánh
bird_flap_time = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap_time, 200)

#tạo xu 
gold_coin_1 = pygame.transform.scale(pygame.image.load("assets/gold1.png").convert_alpha(), (40, 40))
gold_coin_2 = pygame.transform.scale(pygame.image.load("assets/gold2.png").convert_alpha(), (40, 40))
gold_coin_3 = pygame.transform.scale(pygame.image.load("assets/gold3.png").convert_alpha(), (40, 40))
gold_coin_4 = pygame.transform.scale(pygame.image.load("assets/gold4.png").convert_alpha(), (40, 40))

sliver_coin_1 =  pygame.transform.scale(pygame.image.load("assets/sliver1.png").convert_alpha(), (40, 40))
sliver_coin_2 =  pygame.transform.scale(pygame.image.load("assets/sliver2.png").convert_alpha(), (40, 40))
sliver_coin_3 =  pygame.transform.scale(pygame.image.load("assets/sliver3.png").convert_alpha(), (40, 40))
sliver_coin_4 =  pygame.transform.scale(pygame.image.load("assets/sliver4.png").convert_alpha(), (40, 40))

gold_coin_list = [gold_coin_1, gold_coin_2, gold_coin_3, gold_coin_4,]   # xoay xu vàng
sliver_coin_list = [sliver_coin_1, sliver_coin_2, sliver_coin_3, sliver_coin_4]    # xoay xu bạc
gold_index = 0
sliver_index = 0
gold_coin = gold_coin_list[gold_index]
sliver_coin = sliver_coin_list[sliver_index]

gold_coin_rect = gold_coin.get_rect(midbottom = (600, 600))
sliver_coin_rect = sliver_coin.get_rect(midbottom = (600, 600))
coin_sliver_list = []      # chứa các xu bac
coin_gold_list = []        # chua cac xu vang

roted_coin = pygame.USEREVENT + 2
pygame.time.set_timer(roted_coin, 200)

# tạo ống
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_gold_surface = pygame.image.load("assets/pipe_gold.png").convert()
pipe_gold_surface = pygame.transform.scale(pipe_gold_surface, (100, 500))

pipe_red_surface = pygame.image.load("assets/pipe_red.png").convert()
pipe_red_surface = pygame.transform.scale(pipe_red_surface, (100, 500))

pipe_list = [] 
pipe_height = [300, 320, 340, 360]
pipe_height1 = [200, 440]
random_number = [1,2,3,4,5,6,7,8,9,10]
pipe_list_hard_mode = []
pipe_list_hard_mode_red = []

index_pipe_hard_mode = []
random_pos = []     # luu cac vi tri cot random dc trong hard mode
index_red_pipe = []   # luu cac vi tri cua red pipe in pipe_list
check_red1 = []      # danh dau nhung red pipe da dam
index_red_pipe_hard_mode = []   # luu vi tri red pipe trong hard mode gold

# tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 800)        # thời gian cột xuất hiện

spawnpipe_hard_mode = pygame.USEREVENT + 7
pygame.time.set_timer(spawnpipe_hard_mode, 150)        # thời gian cột xuất hiện trong hard mode

spawncoin_sliver = pygame.USEREVENT + 3
pygame.time.set_timer(spawncoin_sliver, 3200)       # thời gian xu bạc xuất hiện

spawncoin_gold = pygame.USEREVENT + 5
pygame.time.set_timer(spawncoin_gold, 9600)       # thời gian xu vàng xuất hiện

spawn_change_size_gold = pygame.USEREVENT + 4
pygame.time.set_timer(spawn_change_size_gold, 15000)  # thoi gian thay doi kich thuoc chim

spawn_change_size_sliver = pygame.USEREVENT + 6
pygame.time.set_timer(spawn_change_size_sliver, 30000)  # thoi gian thay doi kich thuoc chim

# tao man hinh ket thuc
game_over_surface = pygame.transform.scale(pygame.image.load("assets/message.png").convert_alpha(), (330, 380))
game_over_rect = game_over_surface.get_rect(center = (270, 360))

# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

cnt = 1     # kiem tra xoa list

while True:                                   # các sự kiện trong game lặp vô hạn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         # thoát khỏi hệ thống
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #and game_active:
                bird_move = -6
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                hard_mode = False
                hard_mode_red = False

                bg = pygame.image.load("assets/background-night.png").convert()
                bg = pygame.transform.scale(bg, (700, 768))

                bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
                bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
                bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))
                bird_list = [bird_down, bird_mid, bird_up]
                bird_index = int(0)
                bird = bird_list[bird_index]
                bird_rect = bird.get_rect(center = (100, 384))

                game_active = True
                pipe_list.clear()
                pipe_list_hard_mode.clear()
                coin_sliver_list.clear()
                coin_gold_list.clear()
                index.clear()
                index1.clear()
                index_red_pipe.clear()
                index_red_pipe_hard_mode.clear()
                check.clear()
                check1.clear()
                index_pipe_hard_mode.clear()
                random_pos.clear()
                cmt = 0
                count_pipe = 0
                bird_rect.center = (100, 384) 
                bird_move = 0
                score = 0
                cnt = 1

        if event.type == spawnpipe and hard_mode == False:
            if random.choice(random_number) == 4:
                pipe_list.extend(create_gold_pipe())
                index.append(len(pipe_list) - 2)
                index.append(len(pipe_list) - 1)
                check.append(0)
                check.append(0)
                index_pipe_hard_mode.append(len(pipe_list) - 2)
                index_pipe_hard_mode.append(len(pipe_list) - 1)
            elif random.choice(random_number) == 5:
                pipe_list.extend(create_red_pipe())
                index_red_pipe.append(len(pipe_list) - 2)
                index_red_pipe.append(len(pipe_list) - 1)
                check.append(0)
                check.append(0)
                index_pipe_hard_mode.append(len(pipe_list) - 2)
                index_pipe_hard_mode.append(len(pipe_list) - 1)
            else:
                pipe_list.extend(create_pipe())
                check.append(0)
                check.append(0)
                index_pipe_hard_mode.append(len(pipe_list) - 2)
                index_pipe_hard_mode.append(len(pipe_list) - 1)

        if event.type == spawnpipe_hard_mode and hard_mode == True:
            if random.choice(random_number) == 4:
                pipe_list_hard_mode.extend(create_gold_pipe())
                index1.append(len(pipe_list_hard_mode) - 2)
                index1.append(len(pipe_list_hard_mode) - 1)
                check1.append(0)
                check1.append(0)
            elif random.choice(random_number) == 5:
                pipe_list_hard_mode.extend(create_red_pipe())
                index_red_pipe_hard_mode.append(len(pipe_list_hard_mode) - 2)
                index_red_pipe_hard_mode.append(len(pipe_list_hard_mode) - 1)
                check1.append(0)
                check1.append(0)
            else:
                pipe_list_hard_mode.extend(create_pipe())
                check1.append(0)
                check1.append(0)

        if event.type == spawncoin_sliver:
            coin_sliver_list.append(create_sliver_coin())
        
        if event.type == spawncoin_gold:
            coin_gold_list.append(create_gold_coin()) 
        
        if event.type == spawn_change_size_gold:
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))
        
        if event.type == spawn_change_size_sliver:
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))

        if event.type == bird_flap_time:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

        if event.type == roted_coin:
            if sliver_index < 3:
                sliver_index += 1
            else:
                sliver_index = 0
            sliver_coin, sliver_coin_rect = sliver_coin_animation()

        if event.type == roted_coin:
            if gold_index < 3:
                gold_index += 1
            else:
                gold_index = 0
            gold_coin, gold_coin_rect = gold_coin_animation()

    screen.blit(bg, (0, 0))

    # khi game hoat dong
    if game_active:
    # hard mode with gold pipe

        if hard_mode == True and hard_mode_red == False:
            # tao lai chim trong gold hard mode
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))

            for i in range(0, len(pipe_list)):
                if i in index and check[i] == 0:
                    if bird_rect.colliderect(pipe_list[i]):
                        check[i] = 1
                        hard_mode = False
                        cnt = 1
                        bg = pygame.image.load("assets/background-night.png").convert()
                        bg = pygame.transform.scale(bg, (700, 768))
                        score_sound.play()

        elif hard_mode == False and hard_mode_red == False:
            for pos_pipe_gold in index:
                if bird_rect.colliderect(pipe_list[pos_pipe_gold]) and check[pos_pipe_gold] == 0:  
                    check[pos_pipe_gold] = 1
                    tmp_pos = pos_pipe_gold
                    hard_mode = True  
                    bg = pygame.image.load("assets/background2.png").convert()
                    bg = pygame.transform.scale(bg, (700, 768))
                    score_sound.play()
    
    # another hard mode with red pipe
        if hard_mode_red == True and hard_mode == False:

            # tao lai chim trong red hard mode
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (34, 24))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (34, 24))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (34, 24))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))

            for i in range(0, len(pipe_list)):
                if i in index_red_pipe and check[i] == 0:
                    if bird_rect.colliderect(pipe_list[i]):
                        check[i] = 1
                        hard_mode_red = False
                        bg = pygame.image.load("assets/background-night.png").convert()
                        bg = pygame.transform.scale(bg, (700, 768))
                        score_sound.play()
        elif hard_mode_red == False and hard_mode == False:
            for pos_pipe_red in index_red_pipe:
                if bird_rect.colliderect(pipe_list[pos_pipe_red]) and check[pos_pipe_red] == 0:  
                    check[pos_pipe_red] = 1
                    hard_mode_red = True
                    bg = pygame.image.load("assets/background3.png").convert()
                    bg = pygame.transform.scale(bg, (700, 768))
                    score_sound.play()
        
        # vẽ cột
        if hard_mode == False:
            if hard_mode_red == False:
                pipe_list = move_pipe(pipe_list)
                draw_pipe(pipe_list, index, index_red_pipe)
                cnt = 1
            elif hard_mode_red == True:
                if len(pipe_list) > 0: 
                    random_pipe_hard_mode_pos = random.choice(index_pipe_hard_mode)
                    if random_pipe_hard_mode_pos not in random_pos:
                        if random_pipe_hard_mode_pos % 2 != 0 and (random_pipe_hard_mode_pos-1) not in random_pos:
                            random_pos.append(random_pipe_hard_mode_pos)
                        if random_pipe_hard_mode_pos % 2 == 0 and (random_pipe_hard_mode_pos+1) not in random_pos: 
                            random_pos.append(random_pipe_hard_mode_pos)
                    pipe_list = move_pipe_y(pipe_list, count_pipe, cmt, random_pos)
                pipe_list = move_pipe_red(pipe_list)
                draw_pipe(pipe_list, index, index_red_pipe)

            elif hard_mode_red == False:
                index_pipe_hard_mode.clear() 
                random_pos.clear()

        elif hard_mode == True and hard_mode_red == False:
            if cnt == 1: 
                pipe_list.clear()
                index.clear()
                check.clear()
                index_red_pipe.clear()
                cnt += 1
            pipe_list_hard_mode = move_hard_mode_pipe(pipe_list_hard_mode)

            draw_pipe(pipe_list_hard_mode, index1, index_red_pipe_hard_mode)
            
            for i in range(0, len(pipe_list_hard_mode)):
                if i in index1 and check1[i] == 0:
                    if bird_rect.colliderect(pipe_list_hard_mode[i]): 
                        check1[i] = 1
                        hard_mode = False
                        cnt = 1
                        bg = pygame.image.load("assets/background-night.png").convert()
                        bg = pygame.transform.scale(bg, (700, 768))
            if hard_mode == False:
                pipe_list_hard_mode.clear()
                index1.clear()
                check1.clear()
                index_red_pipe.clear()
                index_red_pipe_hard_mode.clear()
                # random_pos.clear()
            
        # vẽ xu
        if hard_mode == False:
            coin_sliver_list = move_coin(coin_sliver_list)
            coin_gold_list = move_coin(coin_gold_list)
            draw_sliver_coin(coin_sliver_list)
            draw_gold_coin(coin_gold_list)

        # vẽ chim
        bird_move += gravity
        roted_bird = rotte_bird(bird)
        bird_rect.centery += bird_move
        screen.blit(roted_bird, bird_rect) 

        # ktra va cham
        if hard_mode == True and hard_mode_red == False:
            game_active = check_collision(pipe_list_hard_mode, index1)
        elif hard_mode == False and hard_mode_red == True:
            game_active = check_collision(pipe_list, index_red_pipe)
        else:
            game_active = check_collision_basic_mode(pipe_list, index, index_red_pipe)
        # ktra ăn xu bac
        remove_sliver_coin = check_coin_sliver_collision(coin_sliver_list)
        if remove_sliver_coin == False:
            coin_sliver_list.remove(result(coin_sliver_list))
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (68, 48))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (68, 48))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (68, 48))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))
        
        # ktra an xu vang
        remove_gold_coin = check_coin_gold_collision(coin_gold_list)
        if remove_gold_coin == False:
            coin_gold_list.remove(result(coin_gold_list))
            bird_down = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (17, 12))
            bird_mid = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (17, 12))
            bird_up = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (17, 12))

            bird_list = [bird_down, bird_mid, bird_up]
            bird_index = int(0)
            bird = bird_list[bird_index]
            bird_rect = bird.get_rect(center = (100, bird_rect.centery))

        # tính điểm
        score_display('main game')
        if hard_mode == True and hard_mode_red == False:
            for pipe in pipe_list_hard_mode:
                if bird_rect.centerx == pipe.centerx:
                    score_sound.play()
                    score += 2
                    break
        elif hard_mode == False and hard_mode_red == True:
            for pipe in pipe_list:
                if bird_rect.centerx == pipe.centerx:
                    score_sound.play()
                    score += 1
                    break
        else:
            for pipe in pipe_list:
                if bird_rect.centerx == pipe.centerx:
                    score_sound.play()
                    score += 1
                    break
        # else:
        #     screen.blit(game_over_surface, game_over_rect)
        #     high_score = update_score(score, high_score )
        #     score_display('game over')

        #vẽ sàn
        if hard_mode == False and hard_mode_red == False:
            draw_floor()
            floor_x_pos -= 1
            if floor_x_pos <= -432:
                floor_x_pos = 0
        elif hard_mode == True and hard_mode_red == False:
            draw_floor_hard_mode()
            floor_x_hard_mode_pos -= 1
            if floor_x_hard_mode_pos <= -1100:
                floor_x_hard_mode_pos = -100
        else:
            draw_floor_hard_mode_red()
            floor_x_hard_mode_red_pos -= 1
            if floor_x_hard_mode_red_pos <= -1100:
                floor_x_hard_mode_red_pos = -100
        
        pygame.display.update()                  # update sự thay đổi background
        clock.tick(120)                           # cài đặt tốc độ game chạy là 120