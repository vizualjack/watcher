from tracking.user import User
from seriesData.library import Library
from persister import Persister
from ui.consoleUi import ConsoleUI


if __name__ == "__main__":
    persister = Persister.load()
    ui = ConsoleUI(persister.user, persister.library)
    ui.use()
    persister.save()