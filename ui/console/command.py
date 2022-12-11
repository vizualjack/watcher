class Command:
    def __init__(self, cmd) -> None:
        self.cmd = cmd
        self.subCmds = [Command]
        self.search = None
        self.exec = None


    def addSubCmd(self, subCmd):
        self.subCmds.append(subCmd)