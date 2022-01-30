import time
import sys
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
from playsound import playsound
import os
import PySimpleGUI as sg

mouse = Controller()
points_in_screen = []
state = 0
sound = 0

flag = 0
flags_state = []

def printInUi(txt=None):
    if txt:
        window['display_text'].update(txt)


def resourcePath(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def playSound(snd):
    global sound
    if sound:
        playsound(resourcePath(snd))


def falseClick(iter):
    global points_in_screen, flags_state
    for pos in points_in_screen:
        should_continue = flags_state[iter]
        if should_continue is False:
            return
        mouse.position = pos
        mouse.press(Button.left)
        playSound('click.wav')
        mouse.release(Button.left)
        printInUi('Clicked on: {0}'.format(pos))
        time.sleep(1)
    falseClick(iter)


def moveMousePosUi():
    index = window["cords_list"].Widget.curselection()
    if index:
        index = index[0]
        mouse.position = points_in_screen[index]


def recordClick():
    global state, points_in_screen
    if state == 0 or state == 2:
        playSound('confirmation.wav')
        points_in_screen.append(mouse.position)
        updateCordListUi(points_in_screen)
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
        window['cords_list'].update(set_to_index=[len(points_in_screen) - 1], scroll_to_index=len(points_in_screen) - 1)
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
            printInUi('Coord deleted: {}'.format(points_in_screen[index[0]]))
            points_in_screen.pop(index[0])
            updateCordListUi(points_in_screen)


def startClick(message='Starting task'):
    global state, points_in_screen, flag, flags_state
    if state == 0:
        if points_in_screen:
            printInUi(message)
            playSound('resume.wav')
            state = 1
            flags_state.append(True)
            flag = len(flags_state) - 1
            thread = threading.Thread(target=lambda :falseClick(flag))
            thread.start()
    elif state == 2:
        state = 0
        startClick('Resume')
    elif state == 1:
        state = 2
        focusUi()
        flags_state[flag] = False
        printInUi('Pause')
        playSound('pause.wav')


def resetClick():
    global state, points_in_screen
    if state != 1:
        state = 0
        points_in_screen = []
        flags_state[flag] = False
        updateCordListUi(points_in_screen)
        printInUi('Coords reset successfully')
        playSound('pause.wav')


def end():
    sys.exit()


# //////////////////////////////////////
# //////////// UI //////////////////////
# //////////////////////////////////////

# Define the window's contents
layout = [[sg.Text('<Ctrl> to record coordinate', key='display_text', font=("Helvetica", "10"))],
          [sg.Button('Start', key='btn_start', disabled=True, tooltip='Start/Stop <SHIFT>'),sg.Button('Erase', key='btn_erase', disabled=True), sg.Button('Reset', key='btn_reset', disabled=True), sg.Button('Quit')],
          [sg.Listbox([], size=(25, 5), enable_events=True, key='cords_list')],
          [[sg.Text('Record coordinate <CTRL> \rStart / Stop script <SHIFT>', key='info_text', font=("Helvetica", "8"),size=(25, 5))]]]
# Create the window
window = sg.Window('Auto Click', layout, size=(220, 200),disable_minimize = True, icon=resourcePath('favicon.ico'), return_keyboard_events=True, use_default_focus=True)
# working main window

with keyboard.GlobalHotKeys({
    '<ctrl>': recordClick,
    '<shift>': startClick}) as s:
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            end()
        elif event == 'btn_start':
            startClick()
        elif event == 'btn_reset':
            resetClick()
        elif event == 'btn_erase':
            eraseCordSelected()
        elif event == 'cords_list':
            moveMousePosUi()
        window.TKroot.focus_force()
    s.join()
window.close()