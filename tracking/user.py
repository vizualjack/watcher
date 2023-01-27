from tracking.watchInfo import WatchInfo


class User:
    def __init__(self) -> None:
        self.watchInfos = list()


    def getWatchInfoForSeries(self, series):
        for watchInfo in self.watchInfos:
            if watchInfo.series == series:
                return watchInfo
        return None

    
    def addSeries(self, series):
        if self.getWatchInfoForSeries(series) == None:
            watchInfo = WatchInfo(series)
            self.watchInfos.append(watchInfo)
            return watchInfo
        return None


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
