import time
import sys
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from playsound import playsound
from pathlib import Path

global state,pointsInScreen,sound,mouse
mouse = Controller()
pointsInScreen = []
state = 0

print('CONTROLES :')
print('')
print('<Ctrl>       ---> Guarda la cordenada donde se hara un click')
print('')
print('<Shift> + s  ---> Empezar/Pausar/reanudar el script')
print('')
print('<shift> + r  ---> Borrar coordenadas previas')
print('')
print('<Alt>        ---> Salir del programa:')
print('')
print('Una vez iniciada la secuencia tu mouse brincará de cordenada en cordenada')
print('por obvias razones se recomienda pausar el programa (Shift + p)')
print('o terminar el programa (Alt) cuando se necesite hacer algo con el mouse')

def playSound(snd):
    path = Path('sounds')
    path = path.absolute() / snd
    print(path)
    playsound(path)

def false_Click():
    global state, pointsInScreen
    for pos in pointsInScreen:
        time.sleep(2)
        if state == 2:
            break
        mouse.position = pos
        mouse.press(Button.left)
        playSound('click.wav')
        mouse.release(Button.left)
        print('click en : {0}'.format(pos))
    if state == 1:
        false_Click()

def record_click():
    global state, pointsInScreen
    if state == 0:
        playSound('confirmation.wav')
        pointsInScreen.append(mouse.position)
        print('cordenada agregada: {}'.format(mouse.position))

def start_click(message='comenzar el script'):
    global state, pointsInScreen
    if state == 0:
        if pointsInScreen:
            print(message)
            playSound('resume.wav')
            state = 1
            thread = threading.Thread(target=false_Click)
            thread.start()
    elif state == 2:
        state = 0
        start_click('reanudar')
    elif state == 1:
        state = 2
        print('pausa')
        playSound('pause.wav')

def reset_click():
    global state, pointsInScreen
    if state != 0:
        state = 0
        pointsInScreen = []
        print('Reset de clicks aplicado')
        playSound('pause.wav')

def end():
    print('adios')
    sys.exit()

with keyboard.GlobalHotKeys({
        '<ctrl>': record_click,
        '<shift>+s': start_click,
        '<shift>+r': reset_click,
        '<alt>': end}) as s:
    s.join()