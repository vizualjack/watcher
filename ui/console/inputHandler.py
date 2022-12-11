import keyboard
import sys
import os
from ui.console.command import Command

Commands = list[Command]

class InputHandler:
    def __init__(self, cmds: Commands) -> None:
        self.cmds = cmds


    def use(self):
        inputText = ""
        lines = 0
        autoCorrect = None
        while True:
            readedKey = keyboard.read_key()
            if not keyboard.is_pressed(readedKey):
                continue
            if len(readedKey) == 1:
                inputText += readedKey
                autoCorrect = None
                continue
            if readedKey == "enter":
                lines += 1
                inputText = ""
            elif readedKey == "backspace":
                inputText = inputText[0:-1]
            elif readedKey == "esc":
                break
            elif readedKey == "tab":
                pass
            print("\r" + inputText, end='')
        #clean up
        for i in range(lines):
            sys.stdin.readline()
        os.system("cls")