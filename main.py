import pygame
import sys
import random
import os

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Typing Test')

text_files_dir = os.listdir('texts')

text_files = []

for file in text_files_dir:
    text_files.append(file)

random_file = random.randint(0, len(text_files) - 1)

typing_file = open(f'texts/{text_files[random_file]}', 'r')
typing_text = typing_file.read()
typing_file.close()

pygame.font.init()

my_font = pygame.font.SysFont('Arial', int(SCREEN_HEIGHT / 10))

BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

text_surface = my_font.render(typing_text, False, TEXT_COLOR)

text_index = 0

text_list = []

for letter in typing_text:
    text_list.append(letter)

key_pressed = ''

correct_array = []

can_type = False
starttime = 0
endtime = 0

stopwatch = 0

WPM = 0

accuracy = 100
current_letters_wrong = 0

offset = 0

for letter in typing_text:
    correct_array.append('neutral')

def get_keys(event):
    selected_character = '~'
    
    if event.key == pygame.K_a: selected_character = 'a'
    if event.key == pygame.K_b: selected_character = 'b'
    if event.key == pygame.K_c: selected_character = 'c'
    if event.key == pygame.K_d: selected_character = 'd'
    if event.key == pygame.K_e: selected_character = 'e'
    if event.key == pygame.K_f: selected_character = 'f'
    if event.key == pygame.K_g: selected_character = 'g'
    if event.key == pygame.K_h: selected_character = 'h'
    if event.key == pygame.K_i: selected_character = 'i'
    if event.key == pygame.K_j: selected_character = 'j'
    if event.key == pygame.K_k: selected_character = 'k'
    if event.key == pygame.K_l: selected_character = 'l'
    if event.key == pygame.K_m: selected_character = 'm'
    if event.key == pygame.K_n: selected_character = 'n'
    if event.key == pygame.K_o: selected_character = 'o'
    if event.key == pygame.K_p: selected_character = 'p'
    if event.key == pygame.K_q: selected_character = 'q'
    if event.key == pygame.K_r: selected_character = 'r'
    if event.key == pygame.K_s: selected_character = 's'
    if event.key == pygame.K_t: selected_character = 't'
    if event.key == pygame.K_u: selected_character = 'u'
    if event.key == pygame.K_v: selected_character = 'v'
    if event.key == pygame.K_w: selected_character = 'w'
    if event.key == pygame.K_x: selected_character = 'x'
    if event.key == pygame.K_y: selected_character = 'y'
    if event.key == pygame.K_z: selected_character = 'z'
    if event.key == pygame.K_SPACE: selected_character = ' '
    if event.key == pygame.K_PERIOD: selected_character = '.'
    if event.key == pygame.K_MINUS: selected_character = '-'
    if event.key == pygame.K_COMMA: selected_character = ','
    if event.key == pygame.K_QUOTE: selected_character = "'"
    if event.key == pygame.K_SLASH: selected_character = '/'

    if selected_character == "'":
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            return '"'
    if selected_character == '/':
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            return '?'

    return selected_character

start_button_size = (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 10)
start_rect = ((SCREEN_WIDTH / 2) - (start_button_size[0] / 2), SCREEN_HEIGHT / 3, start_button_size[0], start_button_size[1])

def get_wpm(string, time):
    seperated_string = string.split()
    words = len(seperated_string)
    return (int((words) / (time / 60)))

def get_color(index):
    if correct_array[index] == 'correct':
        return (0, 255, 0)
    elif correct_array[index] == 'neutral':
        return TEXT_COLOR
    else:
        return (255, 0, 0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if can_type:

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    key_pressed = (get_keys(event).capitalize())
                else:
                    key_pressed = (get_keys(event))

                if key_pressed == text_list[text_index]:
                    correct_array[text_index] = 'correct'
                    if correct_array[-1] != 'correct':
                        text_index += 1
                        width, height = my_font.size(key_pressed)
                        offset += width
                    else:
                        if endtime == 0:
                            endtime = pygame.time.get_ticks()
                        duration = (endtime - starttime) / 1000
                        WPM = get_wpm(typing_text, duration)

                elif key_pressed != text_list[text_index]:
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        continue
                    else:
                        correct_array[text_index] = 'incorrect'
                        current_letters_wrong += 1

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > start_rect[0] and event.pos[0] < (start_rect[0] + start_rect[2]) and event.pos[1] > start_rect[1] and event.pos[1] < (start_rect[1] + start_rect[3]):
                    can_type = True
                    if starttime == 0:
                        starttime = pygame.time.get_ticks()

    if starttime != 0:
        if endtime == 0:
            stopwatch = int((pygame.time.get_ticks() - starttime) / 1000)
    if accuracy >= 0:
        accuracy = int(((len(typing_text) - current_letters_wrong) / len(typing_text)) * 100)

    screen.fill(BACKGROUND_COLOR)

    total_text_size = 0
    character_index = 0
    for character in text_list:
        text_width, text_height = my_font.size(character)
        screen.blit(my_font.render(character, False, get_color(character_index)), (total_text_size - offset + SCREEN_WIDTH / 8, SCREEN_HEIGHT / 12))
        total_text_size += text_width
        character_index += 1

    pygame.draw.rect(screen, (BACKGROUND_COLOR), pygame.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 8), 0, SCREEN_WIDTH / 8, SCREEN_HEIGHT))

    if can_type == False:
        pygame.draw.rect(screen, (25, 220, 25), start_rect)
        text_width, text_height = my_font.size('Start')
        screen.blit(my_font.render('Start', False, TEXT_COLOR), ((SCREEN_WIDTH / 2) - (text_width / 2), start_rect[1]))

    screen.blit(my_font.render('Time: ' + str(stopwatch) + ' seconds', False, TEXT_COLOR), (50, 400))
    screen.blit(my_font.render('WPM: ' + str(WPM), False, TEXT_COLOR), (50, 500))
    screen.blit(my_font.render('Accuracy ' + str(accuracy) + '%', False, TEXT_COLOR), (50, 600))

    pygame.display.update()
    clock.tick(60)

