import pygame
import sys
import random
from pygame import mixer

pygame.init ()
pygame.mixer.init() 
width , height = 1500 , 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blitzshot Game")
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
FPS = 60
target_radius = 50
score = 0
highest_score = 0
target_speed = 5

#colors
YELLOW = (255, 255, 0)
RED=(255,0,0)
BLACK = (0,0,0)
WHITE=(255,255,255)

#fonts
score_time_font= pygame.font.Font("NovaSlim-Regular.ttf", 20)
title_game_font= pygame.font.Font("NovaSlim-Regular.ttf", 120)
gameover_font= pygame.font.Font("NovaSlim-Regular.ttf", 120)
highest_score_font= pygame.font.Font("NovaSlim-Regular.ttf", 40)
end_score_font= pygame.font.Font("NovaSlim-Regular.ttf", 40)

#music
hit_sound = mixer.Sound('hit-someting-6037.mp3')
mixer.music.load('metal-blues-120-bpm-loop-15519.mp3')
mixer.music.play(-1)

def play_hit_sound():
    hit_sound = mixer.Sound('hit-someting-6037.mp3') 
    hit_channel = mixer.Channel(1)
    hit_channel.play(hit_sound)

#Create targets
targets = [(random.randint(target_radius, width - target_radius), random.randint(target_radius, height - target_radius)) for _ in range(3)]
def draw_targets():
    for target in targets:
        pygame.draw.circle(screen, YELLOW, target, target_radius)

#Create cross
def crossaim():
    pos = pygame.mouse.get_pos()
    long = 10
    color = RED
    pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0], pos[1] - long), 2)
    pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0] + long, pos[1]), 2)
    pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0], pos[1] + long), 2)
    pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0] - long, pos[1]), 2)

#Shooting targets
def shoot(target, pos):
    x, y = target
    pos = pygame.mouse.get_pos()
    distance = ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** 0.5  #Hypotenuse
    return distance <= target_radius 

#Score
def showScore():
    scoreText = score_time_font.render("Score : " + str(score), True, WHITE)
    screen.blit(scoreText, (10, 10))

#Highest score
def  update_highest_score(score):
    with open('file.txt', 'r+') as f:
        highest_score = int(f.readline())
    if score > highest_score:
        with open ('file.txt', 'w') as f:
            f.write (str(score))
            return score
    return highest_score

def showHighest_score():
    hsText = highest_score_font.render("Highest score : " + str(update_highest_score(score)), True, YELLOW)
    screen.blit(hsText, (550, 350))

#Timer
def time(): 
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = (20 - elapsed_time)
        timer_text = score_time_font.render("Time: " +str(remaining_time)+ "s", True, WHITE)
        screen.blit(timer_text, (700, 10))



#MainMenu
def main_menu():
    
    while True:
        screen.fill(BLACK)
        pygame.mouse.set_cursor(pygame.cursors.arrow)
    
        title_game_Text = title_game_font.render("BLITZSHOT", True, YELLOW) #Game Name Title
        screen.blit(title_game_Text, (500, 150))

        play_button= pygame.image.load('Play Button.png').convert() #Play Button
        play_button_rect = play_button.get_rect(topleft=(600, 350))
        screen.blit(play_button, play_button_rect)
    
        quit_button= pygame.image.load('Quit Button.png').convert() #Quit Button
        quit_button_rect = quit_button.get_rect(topleft=(600, 500))
        screen.blit(quit_button, quit_button_rect)
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                hit_sound.play()
                MENU_MOUSE_POS = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(MENU_MOUSE_POS): #Start game when clicked play button
                    game()
                elif quit_button_rect.collidepoint(MENU_MOUSE_POS): #Quit game when clicked quit button
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



def game_over():
    global score
    global highest_score
    global start_ticks
    global target_radius

    while True:
        screen.fill(BLACK)
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        pygame.mouse.set_visible(True)
        mixer.music.stop()
        gameover_sound = mixer.Sound('elektron-mission-accomplished-160914.mp3')
        gameover_sound.play()
        showHighest_score()
    
        scoreText = end_score_font.render("Score : " + str(score), True, WHITE) #Show the final score
        screen.blit(scoreText, (650, 250))
        display_game_over = gameover_font.render("GAME OVER", True, RED) #Show the GAME OVER
        screen.blit(display_game_over, (400, 80))

        newgame_button= pygame.image.load('New game Button.png').convert() #New Game button
        newgame_button_rect = newgame_button.get_rect(topleft=(600, 430))
        screen.blit(newgame_button, newgame_button_rect)

        quit_button= pygame.image.load('Quit Button.png')  #Quit Button
        quit_button_rect = quit_button.get_rect(topleft=(600, 580))
        screen.blit(quit_button, quit_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_hit_sound()
                END_MOUSE_POS = pygame.mouse.get_pos()
                if newgame_button_rect.collidepoint(END_MOUSE_POS):  #Replay game when clicked the button
                    score=0
                    target_radius = 50
                    start_ticks = pygame.time.get_ticks()
                    mixer.music.load('metal-blues-120-bpm-loop-15519.mp3')
                    mixer.music.play(-1)
                    pygame.event.clear()
                    game()
                elif quit_button_rect.collidepoint(END_MOUSE_POS): #Quit game when clicked the button
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def game():
    global score
    global target_radius
    global target_speed

    while True:
        screen.fill(BLACK)
        pygame.mouse.set_visible(False) #hide the mouse
        draw_targets()
        crossaim() 
        showScore()
        time()
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_hit_sound()
                hit_target = False
                for i, target in enumerate(targets):
                    if shoot(target, event.pos):
                        score += 10 #get 10 points when shot the target
                        targets[i] = (random.randint(target_radius, width - target_radius),
                                    random.randint(target_radius, height - target_radius)) #Create another target at random position
                        hit_target = True
                if not hit_target: #loosing points when miss shots
                    score -= 4

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        if elapsed_time >= 20: #Game over after 20sec
            game_over() 
        
        if  score > 50: #change difficulty medium, smaller targets
            target_radius = 30
        if score > 100: #change difficulty hard, smaller targets start to moving horizontally
             for i in range(len(targets)):
                if targets[i][0] - target_radius <= 0 or targets[i][0] + target_radius >= width:  #if target touch the borders start to move opposite way
                    target_speed= - target_speed
                    targets[i] = (targets[i][0] + target_speed , targets[i][1])
                    
                else:
                    targets[i] = (targets[i][0] + target_speed , targets[i][1])



        pygame.display.flip()
        clock.tick(FPS)
main_menu()

