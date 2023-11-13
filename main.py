import pyautogui
import time

from numpy import random

PEDRAS = ['pedra_1.png', 'pedra_2.png', 'pedra_3.png', 'pedra_4.png', 'pedra_5.png', 'pedra_6.png']


def find_base_coords():
    image = 'base.png'
    place_to_click = None
    print(f'Looking for {image}')

    timeout_trys = 50

    while timeout_trys > 0 and place_to_click is None:
        try:
            place_to_click = pyautogui.locateOnScreen(image, confidence=0.7)
            timeout_trys -= 1
        except Exception as e:
            return False

    if timeout_trys == 0:
        return False
        # raise ValueError(f'Timeout searching for: {image}')

    print(f'Found for {image}')
    return place_to_click


def click_image(image):
    place_to_click = None
    print(f'Looking for {image}')

    timeout_trys = 50

    while timeout_trys > 0 and place_to_click is None:
        try:
            place_to_click = pyautogui.locateOnScreen(image, confidence=0.7)
            timeout_trys -= 1
        except Exception as e:
            return False

    if timeout_trys == 0:
        print(f'time out')
        return False
        # raise ValueError(f'Timeout searching for: {image}')

    print(f'Found for {image}')
    button_to_click = pyautogui.center(place_to_click)
    pyautogui.click(button_to_click)
    time.sleep(random.random())
    return True


def click_mission():
    return click_image('missao.png')


def click_play():
    return click_image('jogar.png')


def click_to_skip():
    time.sleep(2)
    return click_image('toque_para_pular.png')


def click_initiate():
    time.sleep(2)
    return click_image('iniciar.png')


def loop_continue():
    while check_for_continue():
        time.sleep(5)
        if check_for_error():
            return
    return


def loop_try_again():
    while check_for_failed_attempt():
        time.sleep(5)
        if check_for_error():
            return
    return


def check_for_failed_attempt():
    return click_image('tente_novamente.png')


def check_for_error():
    return click_image('ok_error.png')


def check_for_continue():
    return click_image('continuar.png')


def check_for_reward():
    return click_image('receber.png')


def select_any_character():
    click_image(PEDRAS[random.randint(0, 5)])
    # click_image(PEDRAS[0])


def get_random_10_percent_difference_of_location(number):
    return number - number * random.randint(-15, 15) / 100


def place_unit_nearby_base(base_location):
    nearby_base_location = (get_random_10_percent_difference_of_location(base_location[0]),
                            get_random_10_percent_difference_of_location(base_location[1]),
                            base_location[2],
                            base_location[3],
                            )
    nearby_base_location_to_click = pyautogui.center(nearby_base_location)
    pyautogui.click(nearby_base_location_to_click)
    time.sleep(random.random())


def play_a_mission():
    while True:
        if click_mission():
            break
        if check_for_error():
            return
        if check_for_reward():
            return

    time.sleep(2)
    if check_for_reward():
        return
    click_play()
    time.sleep(5)

    while True:
        if click_to_skip():
            break
        if check_for_error():
            return

    while True:
        if click_initiate():
            break
        if check_for_error():
            return

    time.sleep(1)

    base_location = find_base_coords()

    while True:
        select_any_character()
        place_unit_nearby_base(base_location)
        time.sleep(random.random() * 2)

        if check_for_error():
            return

        if check_for_failed_attempt():
            loop_try_again()
            return

        if check_for_continue():
            loop_continue()
            return


while True:
    play_a_mission()
