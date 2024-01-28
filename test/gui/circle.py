#!/usr/bin/env python3
# run on pi with: xinit /pi/touchpi/venv/bin/python circle.py to check display offset
import PySimpleGUI as sg

layout = [[sg.Canvas(size=(480, 480), background_color='red', key='canvas')]]

window = sg.Window('Canvas test', layout,
                   location=(0, 0),
                   no_titlebar=True,
                   margins=(0, 0),
                   finalize=True)


def submit1():
    window.write_event_value(sg.WIN_CLOSED, ())
    print("Write event WIN_CLOSED")


quit_button = sg.ttk.Button(window['canvas'].TKCanvas, text='Quit', command=submit1)
cir1 = window['canvas'].TKCanvas.create_oval(0, 0, 480, 480, fill='blue')
cir2 = window['canvas'].TKCanvas.create_oval(10, 10, 470, 470, fill='green')
but1 = window['canvas'].TKCanvas.create_window(200, 230, anchor='nw', window=quit_button)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
