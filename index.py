## for compiling ui.eel.graphicalUi
class FakeOut:
    def write(p1,p2):
        pass
import sys
sys.stdout = FakeOut()
sys.stderr = FakeOut()
#####

from persister import Persister
# from ui.console.consoleUi import ConsoleUI # pyinstaller index.py --name Watcher --onefile --icon=icon.ico
from ui.eel.graphicalUi import GraphicalUI # pyinstaller index.py --name Watcher --icon=icon.ico --add-data "ui/eel/;ui/eel/" --onefile --noconsole
                                           # on linux   ~/.local/bin/pyinstaller index.py --name Watcher --icon=icon.ico --add-data ui/eel/:ui/eel/ --onefile --noconsole


if __name__ == "__main__":
    persister = Persister.load()
    ui = GraphicalUI(persister.user, persister.library)
    # ui = ConsoleUI(persister.user, persister.library)
    ui.onClose = persister.save
    ui.use()
    persister.save()