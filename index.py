
from persister import Persister
# from ui.console.consoleUi import ConsoleUI # pyinstaller index.py --name Watcher --onefile --icon=icon.ico
from ui.gui.graphicalUi import GraphicalUI # python -m eel index.py ui/gui/ --onefile --noconsole


if __name__ == "__main__":
    persister = Persister.load()
    ui = GraphicalUI(persister.user, persister.library)
    # ui = ConsoleUI(persister.user, persister.library)
    ui.onClose = persister.save
    ui.use()
    # persister.save()