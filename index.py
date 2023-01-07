# pyinstaller --onefile index.py --name Watcher
from persister import Persister
# from ui.console.consoleUi import ConsoleUI
from ui.gui.graphicalUi import GraphicalUI


if __name__ == "__main__":
    persister = Persister.load()
    ui = GraphicalUI(persister.user, persister.library)
    ui.onClose = persister.save
    ui.use()
    # persister.save()