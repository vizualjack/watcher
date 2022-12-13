from seriesData.series import Series

class WatchInfo:
    def __init__(self, series:Series) -> None:
        self.series = series
        self.season = 1
        self.episode = 1
        self.watchLocation = ""


    def getSeries(self) -> Series:
        return self.series


    def getEpisode(self) -> int:
        self.__checkForNewSeason()
        return self.episode


    def getSeason(self) -> int:
        self.__checkForNewSeason()
        return self.season


    def getSeasonEpisodes(self) -> int:
        self.__checkForNewSeason()
        curSeasonIndex = self.season-1
        season = self.series.seasons[curSeasonIndex]
        return season.episodes

    
    def watchLocationIsWebLink(self) -> bool:
        return self.watchLocation.startswith("https://") or self.watchLocation.startswith("http://")


    def nextEpisode(self):
        curSeasonIndex = self.season-1
        if curSeasonIndex >= len(self.series.seasons):
            return
        curSeason = self.series.seasons[curSeasonIndex]
        lastSeasonIndex = len(self.series.seasons)-1
        if curSeasonIndex == lastSeasonIndex and self.episode > curSeason.episodes:
            return
        self.episode += 1
        if lastSeasonIndex > curSeasonIndex and self.episode > curSeason.episodes:
            self.episode = 1
            self.season += 1


    def unseenEpisodes(self):
        curSeasonIndex = self.season-1
        lastSeasonIndex = len(self.series.seasons)-1
        if curSeasonIndex > lastSeasonIndex:
            raise Exception("Current season index is higher than last season index")
        if curSeasonIndex < lastSeasonIndex:
            return True
        lastSeasonEpisodes = self.series.seasons[lastSeasonIndex].episodes
        if self.episode <= lastSeasonEpisodes:
            return True
        return False
        

    def __checkForNewSeason(self):
        curSeasonIndex = self.season-1
        curSeason = self.getSeries().seasons[curSeasonIndex]
        if curSeason.episodes >= self.episode:
            return
        lastSeasonIndex = len(self.getSeries().seasons)-1
        if lastSeasonIndex > curSeasonIndex:
            self.season += 1
            self.episode = 1