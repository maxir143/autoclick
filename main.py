import time
import sys
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
global state,pointsInScreen

mouse = Controller()
pointsInScreen = []
state = 0

print('CONTROLES :')
print('')
print('Ctrl ---> Guarda la cordenada donde se hara un click')
print('')
print('Shift + S ---> Empezas el script')
print('')
print('Shift + p ---> Pausar/reanudar el script ')
print('')
print('Shift + R ---> Borrar coordenadas previas')
print('')
print('Alt  ---> Salir del programa:')
print('')
print('Una vez iniciada la secuencia tu mouse brincará de cordenada en cordenada')
print('por obvias razones se recomienda pausar el programa (Shift + p)')
print('o terminar el programa (Alt) cuando se necesite hacer algo con el mouse')

def false_Click():
    global state, pointsInScreen
    for pos in pointsInScreen:
        time.sleep(2)
        if state == 2:
            break
        mouse.position = pos
        mouse.press(Button.left)
        mouse.release(Button.left)
        print('click en : {0}'.format(pos))
    if state == 1:
        false_Click()

def record_click():
    global state, pointsInScreen
    if state == 0:
        pointsInScreen.append(mouse.position)
        print('cordenada agregada: {}'.format(mouse.position))

def start_click():
    global state, pointsInScreen
    if state == 0:
        if pointsInScreen:
            print('comenzar el script')
            state = 1
            thread = threading.Thread(target=false_Click)
            thread.start()

def reset_click():
    global state, pointsInScreen
    state = 0
    pointsInScreen = []
    print('Reset de clicks aplicado')

def pause_click():
    global state, pointsInScreen
    if state == 2:
        print('no pausita')
        state = 0
        start_click()
    elif state == 1:
        state = 2
        print('pausita')

def end():
    print('adios')
    sys.exit()

with keyboard.GlobalHotKeys({
        '<ctrl>': record_click,
        '<shift>+s': start_click,
        '<shift>+p': pause_click,
        '<shift>+r': reset_click,
        '<alt>': end}) as l:
    l.join()

