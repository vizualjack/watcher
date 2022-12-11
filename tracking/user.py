from tracking.watchInfo import WatchInfo


WatchInfos = list[WatchInfo]


class User:
    def __init__(self) -> None:
        self.watchInfos = WatchInfos()


    def getWatchInfoForSeries(self, series):
        for watchInfo in self.watchInfos:
            if watchInfo.series == series:
                return watchInfo
        return None

    
    def addSeries(self, series):
        if self.getWatchInfoForSeries(series) == None:
            self.watchInfos.append(WatchInfo(series))
            return True
        return False


    def removeSeries(self, series):
        watchInfoWithSeries = None
        for watchInfo in self.watchInfos:
            if watchInfo.series == series:
                watchInfoWithSeries = watchInfo
                break
        if watchInfoWithSeries != None:
            self.watchInfos.remove(watchInfoWithSeries)
            return True
        return False
