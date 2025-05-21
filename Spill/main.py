import pygame, sys, random, asyncio


#Functions for game
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def create_pipe():
  
  random_pipe_position = random.choice(pipe_height)
  bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_position))
  top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_position - 300))
  return bottom_pipe, top_pipe

def move_pipes (pipes):
  for pipe in pipes:
    pipe.centerx -= 5
  visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
  return visible_pipes

def draw_pipes(pipes):
  for pipe in pipes:
    if pipe.bottom >= 1024:
      screen.blit(pipe_surface,pipe)
    else:
      flip_pipe = pygame.transform.flip(pipe_surface,False, True)
      screen.blit(flip_pipe,pipe)

def check_collision(pipes):
  global can_score
  for pipe in pipes:
    if birb_rect.colliderect(pipe):
      death_sound.play()
      can_score = True
      return False
      
  if birb_rect.top <= -100 or birb_rect.bottom >= 900:
    can_score = True
    return False
 
  return True

def rotate_birb(birb):
  new_birb = pygame.transform.rotozoom(birb,-birb_movement * 3,1)
  return new_birb 
  
def birb_animation():
  new_birb = birb_frames[birb_index]
  new_birb_rect = new_birb.get_rect(center = (100,birb_rect.centery))
  return new_birb,new_birb_rect

def score_display(game_state):
  if game_state =='main_game':
    score_surface = game_font.render(str(int(score)),True,(255,255,255))
    score_rect = score_surface.get_rect(center =(288,100))
    screen.blit(score_surface,score_rect)
  if game_state =='game_over':
     score_surface = game_font.render(f'score:{int(score)}',True,(255,255,255))
     score_rect = score_surface.get_rect(center =(288,100))
     screen.blit(score_surface,score_rect)
    
     high_score_surface = game_font.render(f'High score:{int(high_score)}',True,(255,255,255))
     high_score_rect = score_surface.get_rect(center =(288,850))
     screen.blit(high_score_surface,high_score_rect)
     
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
  
def pipe_score_check():
  global score, can_score
  
  if pipe_list:
    for pipe in pipe_list:
      if 95< pipe.centerx <105 and can_score:
        score +=1
        score_sound.play()
        can_score = False
      if pipe.centerx < 0:
        can_score = True
  
#game init
#pygame.mixer.pre_init(frequency = 44100, size= 16, channels = 1, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()    
game_font = pygame.font.Font('04B_19.ttf', 40) 

# Game variables
gravity = 0.25
birb_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#assets
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

birb_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
birb_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
birb_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
birb_frames = [birb_downflap,birb_midflap,birb_upflap]
birb_index = 0
birb_surface = birb_frames[birb_index]
birb_rect = birb_surface.get_rect(center = (100,512))

BIRBFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRBFLAP,200)

# birb_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# birb_surface = pygame.transform.scale2x(birb_surface)
# birb_rect = birb_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100


#Game Loop(runs game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                birb_movement = 0
                birb_movement -= 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
              game_active = True
              pipe_list.clear() 
              birb_rect.center = (100,512)
              birb_movement = 0
              score = 0
          
        
        if event.type == SPAWNPIPE:
          pipe_list.extend(create_pipe())
         
        if event.type == BIRBFLAP:
          if birb_index < 2:
            birb_index += 1
          else: 
            birb_index = 0
            
          birb_surface,birb_rect = birb_animation()
          
    screen.blit(bg_surface, (0, 0))

    if game_active:
      # Bird movement
      birb_movement += gravity
      rotated_birb = rotate_birb(birb_surface)
      birb_rect.centery += birb_movement
      screen.blit(rotated_birb, birb_rect)
      game_active = check_collision(pipe_list)
      
      #pipes
      pipe_list = move_pipes(pipe_list)
      draw_pipes(pipe_list)

      #score
      pipe_score_check()
      score_display('main_game')
    
        
    else:
      screen.blit(game_over_surface,game_over_rect)
      high_score = update_score(score, high_score)
      score_display('game_over')
      

    # Floor movement
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
