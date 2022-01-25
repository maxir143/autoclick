import time
import sys
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from playsound import playsound
import os
import PySimpleGUI as sg

global state,pointsInScreen,sound,mouse
mouse = Controller()
pointsInScreen = []
state = 0
sound = 0

def printInUi(txt=None):
    if txt:
        window['displayText'].update(txt)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
def playSound(snd):
    if sound:
        playsound(resource_path(snd))
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
        printInUi('Clicked on: {0}'.format(pos))
    if state == 1:
        false_Click()
def record_click():
    global state, pointsInScreen
    if state == 0:
        playSound('confirmation.wav')
        pointsInScreen.append(mouse.position)
        printInUi('Coord added: {}'.format(mouse.position))
def start_click(message='Starting task'):
    global state, pointsInScreen
    if state == 0:
        if pointsInScreen:
            printInUi(message)
            playSound('resume.wav')
            state = 1
            thread = threading.Thread(target=false_Click)
            thread.start()
    elif state == 2:
        state = 0
        start_click('Resume')
    elif state == 1:
        state = 2
        printInUi('Pause')
        playSound('pause.wav')
def reset_click():
    global state, pointsInScreen
    if state != 0:
        state = 0
        pointsInScreen = []
        printInUi('Coords reset successfully')
        playSound('pause.wav')
def end():
    sys.exit()

#//////////////////////////////////////
#//////////// UI //////////////////////
#//////////////////////////////////////

# Define the window's contents
layout = [[sg.Text('Press Ctrl',key='displayText')],[sg.Button('Start'),sg.Button('Reset'),sg.Button('Quit')] ]
# Create the window
window = sg.Window('Autoclick', layout,icon=resource_path('favicon.ico'), return_keyboard_events=True,use_default_focus=True)
# working main window
with keyboard.GlobalHotKeys({
    '<ctrl>': record_click,
    '<shift>': start_click}) as s:
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            end()
        elif event == 'Start':
            start_click()
        elif event == 'Reset':
            reset_click()
    s.join()
window.close()