import time
import sys
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from playsound import playsound
import os
import PySimpleGUI as sg

global state, pointsInScreen, sound, mouse
mouse = Controller()
pointsInScreen = []
state = 0
sound = 0


def printInUi(txt=None):
    if txt:
        window['display_text'].update(txt)


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
        if state == 2 or state == 0:
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
        updateCordListUi(pointsInScreen)
        printInUi('Coord added: {}'.format(mouse.position))
        focusUi()


def updateCordListUi(cords):
    format_cord = []
    for i in cords:
        format_cord.append('x: {}, y: {}'.format(i[0], i[1]))

    window["cords_list"].update(format_cord)
    if cords:
        window['btn_erase'].update(disabled=False)
        window['btn_start'].update(disabled=False)
        window['btn_reset'].update(disabled=False)
        window['cords_list'].update(set_to_index=[len(pointsInScreen) - 1], scroll_to_index=len(pointsInScreen) - 1)
    else:
        window['btn_erase'].update(disabled=True)
        window['btn_start'].update(disabled=True)
        window['btn_reset'].update(disabled=True)
        global state
        if state == 2:
            state = 0



def focusUi():
    window.BringToFront()


def eraseCordSelected(list="cords_list"):
    if state == 0 or state == 2:
        index = window[list].get()
        if index:
            index = window["cords_list"].GetIndexes()
            printInUi('Coord deleted: {}'.format(pointsInScreen[index[0]]))
            pointsInScreen.pop(index[0])
            updateCordListUi(pointsInScreen)


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
        focusUi()
        printInUi('Pause')
        playSound('pause.wav')


def reset_click():
    global state, pointsInScreen
    state = 0
    pointsInScreen = []
    updateCordListUi(pointsInScreen)
    printInUi('Coords reset successfully')
    playSound('pause.wav')


def end():
    sys.exit()


# //////////////////////////////////////
# //////////// UI //////////////////////
# //////////////////////////////////////

# Define the window's contents
layout = [[sg.Text('Press Ctrl', key='display_text', font=("Helvetica", "10"))],
          [sg.Button('Start', key='btn_start', disabled=True, tooltip='Start/Stop <SHIFT>'),sg.Button('Erase', key='btn_erase', disabled=True), sg.Button('Reset', key='btn_reset', disabled=True), sg.Button('Quit')],
          [sg.Listbox([], size=(25, 5), enable_events=True, key='cords_list')],
          [[sg.Text('Record click cord <CTRL> Start/Stop script <SHIFT>', key='info_text', font=("Helvetica", "8"),size=(25, 5))]]]
# Create the window
window = sg.Window('Autoclick', layout, size=(220, 200), icon=resource_path('favicon.ico'), return_keyboard_events=True,use_default_focus=True)
# working main window

with keyboard.GlobalHotKeys({
    '<ctrl>': record_click,
    '<shift>': start_click}) as s:
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            end()
        elif event == 'btn_start':
            start_click()
        elif event == 'btn_reset':
            reset_click()
        elif event == 'btn_erase':
            eraseCordSelected()
        window.TKroot.focus_force()
    s.join()
window.close()