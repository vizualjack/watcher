from tracking.watchInfo import WatchInfo


WatchInfos = list[WatchInfo]


class User:
    def __init__(self) -> None:
        self.watchInfos = WatchInfos()

    
    def addSeries(self, series):
        self.watchInfos.append(WatchInfo(series))