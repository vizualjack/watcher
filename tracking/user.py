from tracking.watchInfo import WatchInfo


WatchInfos = list[WatchInfo]


class User:
    def __init__(self) -> None:
        self.watchInfos = WatchInfos()

    
    def addSeries(self, series):
        self.watchInfos.append(WatchInfo(series))


    def removeSeries(self, series):
        watchInfoWithSeries = None
        for watchInfo in self.watchInfos:
            if watchInfo.series == series:
                watchInfoWithSeries = watchInfo
                break
        if watchInfoWithSeries != None:
            self.watchInfos.remove(watchInfoWithSeries)
