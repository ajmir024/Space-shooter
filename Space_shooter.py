import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 650, 1400
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Ajmir vs Nayem")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 60)

#sound things
sound2=pygame.mixer.Sound("sound.wav")
sound=pygame.mixer.Sound("laser.wav")

pygame.mixer.music.load("music.mp3")
i=0.5
Click_sound=True
bullet_sound=True

bgmu=False

pygame.mixer.music.play(-1)




#image things
bg=pygame.image.load("bg.png")
bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))
Ship1=pygame.image.load("ship1.png")
Ship2=pygame.image.load("ship2.png")
ship1=pygame.transform.scale(Ship1,(100,90))
ship2=pygame.transform.scale(Ship2,(100,90))
ajmir=ship1.get_rect()
nayem=ship2.get_rect()

ajmir.x,ajmir.y=285,1270
nayem.x,nayem.y=285,60
ajmir.topleft=(ajmir.x,ajmir.y)
nayem.topleft=(nayem.x,nayem.y)

#menu
menu_button = pygame.Rect(590, 10, 50, 40)
menu_open = False
menu_items = [
    ("Restart", pygame.Rect(540, 65, 100, 40)),
    ("Back", pygame.Rect(540, 110, 100, 40)),
    ("Quit", pygame.Rect(540, 155, 100, 40)),
    ("Background music on/off",pygame.Rect(340,200,300,40)),
    ("Click sound on/off",pygame.Rect(390,245,250,40)),
     ("Bullet sound on/off",pygame.Rect(390,290,250,40))
]





# Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GREEN = (20, 220, 60)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (160, 160, 160)
YELLOW = (255, 215, 0)

# Game state
game_state = "start"
game_over = False

# Player name inputs
ajmir_name = ""
nayem_name = ""
input_active = {"ajmir": False, "nayem": False}

# Input boxes
ajmir_input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 120, 200, 50)
nayem_input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)

# Buttons
start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2  , 200, 50)
quit_button = pygame.Rect(550, HEIGHT - 60, 100, 40)
restart = pygame.Rect(550, 60, 100, 40)
back_button=pygame.Rect(550,20,100,40)

# Player setup
PLAYER_WIDTH, PLAYER_HEIGHT = 70, 50
BULLET_WIDTH, BULLET_HEIGHT = 5, 15
BULLET_SPEED = 25
MAX_LIFE = 100


ajmir_life = MAX_LIFE
nayem_life = MAX_LIFE

# Shelters
l = 70
w = 30
shelters = [
    pygame.Rect(80, 435, l, w),##
    pygame.Rect(80, 140, l, w),##
    pygame.Rect(495,110,l,w),##
    pygame.Rect(535, 1050, l, w),#
    pygame.Rect(470,815, l, w),#
    pygame.Rect(410,260, l+10, w),##
    pygame.Rect(550,395,l,w),##
    pygame.Rect(180,240,l-10,w),##
    pygame.Rect(445, 1210, l, w),#
    pygame.Rect(475, 630, l-10, w),##
    pygame.Rect(80, 1200, l+20, w),#
    pygame.Rect(110,960,l,w),#
    pygame.Rect(55,775,l-10,w),#
    
    pygame.Rect(300, 170, l + 20, w - 20),
    pygame.Rect(295, 1250, l + 20, w - 20)
]

# Bullets
ajmir_bullets = []
nayem_bullets = []

# Touch drag
active_touches = {}

# Timing
ajmir_last_shot = 0
nayem_last_shot = 0
SHOOT_DELAY = 100

def draw_text(text, x, y, color=WHITE, center=False, big=False):
    used_font = big_font if big else font
    label = used_font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        screen.blit(label, rect)
    else:
        screen.blit(label, (x, y))

def draw_life_bar(x, y, life, name):
    pygame.draw.rect(screen, RED, (x, y, 100, 10))
    pygame.draw.rect(screen, GREEN, (x, y, life, 10))
    draw_text(name, x + 110, y - 5)

def is_behind_shelter(ship, direction):
    for shelter in shelters:
        if direction == "up":
            if ship.bottom > shelter.bottom and abs(ship.centerx - shelter.centerx) < 35:
                return True
        elif direction == "down":
            if ship.top < shelter.top and abs(ship.centerx - shelter.centerx) < 35:
                return True
    return False

def reset_game():
    global ajmir, nayem, ajmir_life, nayem_life, ajmir_bullets, nayem_bullets, game_over
    ajmir.x, ajmir.y = 285,1270
    nayem.x, nayem.y = WIDTH // 2 - 30, 60
    ajmir_life = MAX_LIFE
    nayem_life = MAX_LIFE
    ajmir_bullets.clear()
    nayem_bullets.clear()
    game_over = False

# Main loop
while True:
    screen.fill(BLACK)
    screen.blit(bg,(0,0))
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ajmir_input_rect.collidepoint(event.pos):
                    input_active["ajmir"] = True
                    input_active["nayem"] = False
                elif nayem_input_rect.collidepoint(event.pos):
                    input_active["ajmir"] = False
                    input_active["nayem"] = True
                else:
                    input_active["ajmir"] = False
                    input_active["nayem"] = False

                if start_button.collidepoint(event.pos):
                    '''if ajmir_name.strip() != "" and nayem_name.strip() != "":'''
                    reset_game()
                    game_state = "play"

                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if input_active["ajmir"]:
                    if event.key == pygame.K_BACKSPACE:
                        ajmir_name = ajmir_name[:-1]
                    else:
                        ajmir_name += event.unicode
                elif input_active["nayem"]:
                    if event.key == pygame.K_BACKSPACE:
                        nayem_name = nayem_name[:-1]
                    else:
                        nayem_name += event.unicode

        elif game_state == "play":           
            if event.type == pygame.FINGERDOWN:
                if Click_sound:
                    sound2.play()
                fx = int(event.x * 650)
                fy = int(event.y * 1400)
                if menu_button.collidepoint(fx, fy):
                    menu_open = not menu_open
                # menu mechanism
                elif menu_open:                    
                    for label, rect in menu_items:
                        if rect.collidepoint(fx, fy):
                            if label == "Quit":
                                pygame.quit() 
                                sys.exit()
                            elif label=="Restart":
                                reset_game()
                                game_state = "play"
                                menu_open=False
                            elif label=="Back":
                                game_state="start"
                                menu_open=False
                            elif label=="Background music on/off":
                                bgmu=not bgmu
                            elif label=="Click sound on/off":
                                Click_sound=not Click_sound
                            elif label=="Bullet sound on/off":
                                bullet_sound=not bullet_sound
                                
                            
                            
                        elif menu_open:
                            menu_open=False
            
                          
                                
                
                x = int(event.x * WIDTH)
                y = int(event.y * HEIGHT)
                if ajmir.collidepoint(x, y):
                    dx = ajmir.x - x
                    dy = ajmir.y - y
                    active_touches[event.finger_id] = {'rect': ajmir, 'offset': (dx, dy)}
                elif nayem.collidepoint(x, y):
                    dx = nayem.x - x
                    dy = nayem.y - y
                    active_touches[event.finger_id] = {'rect': nayem, 'offset': (dx, dy)}

            
            
             
            elif event.type == pygame.FINGERUP:
                    active_touches.pop(event.finger_id, None)
                                                       
            elif event.type == pygame.FINGERMOTION:
               
                if event.finger_id in active_touches:
                    rect = active_touches[event.finger_id]['rect']
                    dx, dy = active_touches[event.finger_id]['offset']
                    x = int(event.x * WIDTH)
                    y = int(event.y * HEIGHT)
                    rect.x = max(0, min(WIDTH - PLAYER_WIDTH, x + dx))
                    rect.y = max(0, min(HEIGHT - PLAYER_HEIGHT, y + dy))
                    if ajmir.y<HEIGHT//2-10:
                        #ajmir_life=0
                        ajmir.x,ajmir.y=285,1270
                        
                    if nayem.y>HEIGHT//2-60:
                        #nayem_life=0
                        nayem.x,nayem.y=WIDTH // 2 - 30, 60
                                        
                    
    # Start screen
    if game_state == "start":      
        draw_text("Press start to play ", WIDTH // 2, HEIGHT // 2 - 160, YELLOW, center=True, big=True)
        
        '''pygame.draw.rect(screen, GRAY, ajmir_input_rect)
        pygame.draw.rect(screen, GRAY, nayem_input_rect)
        draw_text("Player 1:", ajmir_input_rect.x - 100, ajmir_input_rect.y + 5)
        draw_text("Player 2:", nayem_input_rect.x - 100, nayem_input_rect.y + 5)
        draw_text(ajmir_name, ajmir_input_rect.x + 5, ajmir_input_rect.y + 5)
        draw_text(nayem_name, nayem_input_rect.x + 5, nayem_input_rect.y + 5)'''

        pygame.draw.rect(screen, BLUE, start_button)
        draw_text("Start", start_button.centerx, start_button.centery, WHITE, center=True)

        pygame.draw.rect(screen, RED, quit_button)
        draw_text("Quit", quit_button.x + 10, quit_button.y + 10)

    elif game_state == "play":
       
        pygame.draw.line(screen,(00,0,70),(0,HEIGHT//2-10),(650,HEIGHT//2-10))

#------------------bullet mechanism--------------#
                 
        if not game_over:
            if current_time - ajmir_last_shot > SHOOT_DELAY and not is_behind_shelter(ajmir, "up"):
                ajmir_bullets.append(pygame.Rect(ajmir.centerx, ajmir.top, BULLET_WIDTH, BULLET_HEIGHT))
                ajmir_last_shot = current_time
                    
            if current_time - ajmir_last_shot > SHOOT_DELAY and  is_behind_shelter(ajmir, "up"):
                ajmir_bullets.append(pygame.Rect(ajmir.centerx, ajmir.top, BULLET_WIDTH, BULLET_HEIGHT))
                    
                ajmir_last_shot = current_time
    
            if current_time - nayem_last_shot > SHOOT_DELAY and not is_behind_shelter(nayem, "down"):
                nayem_bullets.append(pygame.Rect(nayem.centerx, nayem.bottom, BULLET_WIDTH, BULLET_HEIGHT))
                
                
                    
                nayem_last_shot = current_time
                    
            if current_time - nayem_last_shot > SHOOT_DELAY and  is_behind_shelter(nayem, "down"):
                    
                nayem_bullets.append(pygame.Rect(nayem.centerx, nayem.bottom, BULLET_WIDTH, BULLET_HEIGHT))
                nayem_last_shot = current_time
                    
        for bullet in ajmir_bullets[:]:
            bullet.y -= BULLET_SPEED
            if bullet.colliderect(nayem):
                if bullet_sound:
                    sound.play()
                nayem_life -= 5
                ajmir_bullets.remove(bullet)
            elif any(bullet.colliderect(s) for s in shelters) or bullet.y < 0:
                ajmir_bullets.remove(bullet)
    
        for bullet in nayem_bullets[:]:
            bullet.y += BULLET_SPEED
            if bullet.colliderect(ajmir):
                if bullet_sound:
                    sound.play()
                ajmir_life -= 5
                nayem_bullets.remove(bullet)
            elif any(bullet.colliderect(s) for s in shelters) or bullet.y > HEIGHT:
                nayem_bullets.remove(bullet)

#------------------bullet mechanism--------------#

        if ajmir_life <= 0:
            draw_text("Player 2 Wins!", WIDTH // 2, HEIGHT // 2, YELLOW, center=True, big=True)
            game_over = True
            
        elif nayem_life <= 0:
            draw_text("Player 1 Wins!", WIDTH // 2, HEIGHT // 2, YELLOW, center=True, big=True)
            game_over = True
        if bgmu:
            i=0
            pygame.mixer.music.set_volume(i)
        else:
            i=0.5
            pygame.mixer.music.set_volume(i)
        
        
            

        '''pygame.draw.rect(screen, BLUE, ajmir)
        pygame.draw.rect(screen, RED, nayem)'''
        screen.blit(ship1,ajmir)
        screen.blit(ship2,nayem)
        draw_text("Player 1", ajmir.x + 5, ajmir.y + PLAYER_HEIGHT + 25)
        draw_text("Player 2", nayem.x + 5, nayem.y - 25)

        for bullet in ajmir_bullets:
            pygame.draw.rect(screen,(0,0,255), bullet)
        for bullet in nayem_bullets:
            pygame.draw.rect(screen,(255,0,0), bullet)

        '''for shelter in shelters:
            pygame.draw.rect(screen, GRAY, shelter)'''

        draw_life_bar(20, HEIGHT - 30, ajmir_life, ajmir_name)
        draw_life_bar(20, 20, nayem_life, nayem_name)
         # --- Draw Hamburger Button ---
    
        pygame.draw.rect(screen, (0, 0, 0), menu_button)
    # Three lines
        for i in range(3):
            pygame.draw.line(screen, (255, 255, 255), (605, 10 + i * 15), (630, 10 + i * 15), 3)

        '''pygame.draw.rect(screen, RED, quit_button)
        draw_text("Quit", quit_button.x + 10, quit_button.y + 10)
        pygame.draw.rect(screen,GREEN,restart)
        draw_text("Restart", restart.x + 10, restart.y + 10)
        pygame.draw.rect(screen,(80,80,80),back_button)
        draw_text("Back", back_button.x + 10, back_button.y + 10)'''
        
       

    # --- Draw Menu ---
    if menu_open:
        for label, rect in menu_items:
            pygame.draw.rect(screen, (100, 100, 100), rect)
            text = font.render(label, True, (255,255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    pygame.display.flip()
