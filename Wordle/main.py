import pygame
import sys
import requests

from pygame.locals import *

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
grey = (211, 211, 211)
black = (0, 0, 0)
green = (0, 255, 0)
lightGreen = (153, 255, 204)

height = 650
width = 500

square_size = 50
square_spacing = 10
incr_spacing = square_size + square_spacing
letter_spacing = 10
up_spacing = 50
down_spacing = 70
left_text_spacing = 170

FPS = 30
clock = pygame.time.Clock()

smallFont = pygame.font.SysFont("Helvetica neue", 30)
font = pygame.font.SysFont("Helvetica neue", 40)
bigFont = pygame.font.SysFont("Helvetica neue", 80)

url5 = "https://matthiaswyss.fr/projects/Wordle/word5.txt"
url6 = "https://matthiaswyss.fr/projects/Wordle/word6.txt"
url7 = "https://matthiaswyss.fr/projects/Wordle/word7.txt"

wordle_text = bigFont.render("WORDLE", True, lightGreen)
nouveaux_mots_text = smallFont.render("NOUVEAUX MOTS A 00H00", True, lightGreen)
press_key_text = font.render("PRESSEZ LA TOUCHE", True, lightGreen)
press_a_text = font.render("A : 5 LETTRES", True, lightGreen)
press_z_text = font.render("Z : 6 LETTRES", True, lightGreen)
press_e_text = font.render("E : 7 LETTRES", True, lightGreen)
bravo_text = bigFont.render("BRAVO !", True, lightGreen)
win_text = font.render("VOUS AVEZ GAGNE", True, lightGreen)
press_space_text = font.render("PRESSEZ ESPACE", True, lightGreen)
dommage_text = bigFont.render("DOMMAGE...", True, lightGreen)
lose_text = font.render("VOUS AVEZ PERDU", True, lightGreen)
word_was_text = font.render("LE MOT ETAIT :", True, lightGreen)


def checkGuess(turn, word, userGuess, window, nb_letter):
    renderList = []
    spacing = 0
    guessColourCode = []
    fullGreen = []

    left_spacing = (width - (nb_letter * square_size) - ((nb_letter - 1) * square_spacing)) / 2

    for x in range(0, nb_letter):
        renderList.append("")
        guessColourCode.append(grey)
        fullGreen.append(green)

    for x in range(0, nb_letter):
        if userGuess[x].lower() in word:
            guessColourCode[x] = yellow

        if word[x] == userGuess[x].lower():
            guessColourCode[x] = green

    list(userGuess)

    for x in range(0, nb_letter):
        renderList[x] = font.render(userGuess[x], True, black)
        pygame.draw.rect(window, guessColourCode[x],
                         pygame.Rect(left_spacing + spacing, up_spacing + (turn * incr_spacing), square_size,
                                     square_size))
        window.blit(renderList[x], (left_spacing + letter_spacing + spacing, up_spacing + (turn * incr_spacing)))
        spacing += incr_spacing

    if guessColourCode == fullGreen:
        return True


def chooseUrl(nb_letter):
    url = ""
    if nb_letter == 5:
        url = url5
    elif nb_letter == 6:
        url = url6
    elif nb_letter == 7:
        url = url7
    return url


def wordle(nb_letter, nb_try):
    word = requests.get(chooseUrl(nb_letter)).text

    left_spacing = (width - (nb_letter * square_size) - ((nb_letter - 1) * square_spacing)) / 2

    window = pygame.display.set_mode((width, height))
    window.fill(black)

    guess = ""

    for x in range(0, nb_letter):
        for y in range(0, nb_try):
            pygame.draw.rect(window, grey,
                             pygame.Rect(left_spacing + (x * incr_spacing), up_spacing + (y * incr_spacing),
                                         square_size, square_size), 2)

    pygame.display.set_caption("Wordle!")

    turn = 0
    win = False

    while not win or turn == nb_try:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.exit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                guess += event.unicode.upper()

                if event.key == pygame.K_BACKSPACE or len(guess) > nb_letter:
                    guess = guess[:-1]

                if event.key == K_RETURN and len(guess) >= nb_letter:
                    win = checkGuess(turn, word, guess, window, nb_letter)
                    turn += 1
                    guess = ""
                    window.fill(black, (0, 550, 500, 100))

        window.fill(black, (0, 550, 500, 100))
        renderGuess = font.render(guess, True, grey)
        window.blit(renderGuess, (left_text_spacing, height - down_spacing))

        if win:
            win_page()

        if turn == nb_try and not win:
            lose_page(nb_letter)

        pygame.display.update()
        clock.tick(FPS)


def win_page():
    window = pygame.display.set_mode((width, height))
    window.fill(black)
    pygame.display.set_caption("Wordle!")

    window.blit(bravo_text, (100, 50))
    window.blit(win_text, (70, 200))
    window.blit(press_space_text, (70, 400))

    while True:
        end()


def lose_page(nb_letter):
    word = requests.get(chooseUrl(nb_letter)).text
    word_text = font.render(word.upper(), True, lightGreen)

    window = pygame.display.set_mode((width, height))
    window.fill(black)
    pygame.display.set_caption("Wordle!")

    window.blit(dommage_text, (10, 50))
    window.blit(lose_text, (70, 200))
    window.blit(word_was_text, (110, 300))
    window.blit(word_text, (160, 350))
    window.blit(press_space_text, (70, 500))

    while True:
        end()


def end():
    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.exit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_SPACE:
            main()


def main():

    window = pygame.display.set_mode((width, height))
    window.fill(black)
    pygame.display.set_caption("Wordle!")

    window.blit(wordle_text, (80, 50))
    window.blit(nouveaux_mots_text, (60, 150))
    window.blit(press_key_text, (50, 300))
    window.blit(press_a_text, (110, 420))
    window.blit(press_z_text, (110, 470))
    window.blit(press_e_text, (110, 520))

    while True:

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.exit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == K_a:
                    wordle(5, 6)

                if event.key == K_z:
                    wordle(6, 7)

                if event.key == K_e:
                    wordle(7, 8)


main()
