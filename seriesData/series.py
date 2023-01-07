from seriesData.season import Season


SeasonList = list[Season]


class Series:
    def __init__(self, name: str) -> None:
        self.name = name
        self.seasons = SeasonList()
        self.image = ""
        self.desc = ""
        self.link = ""


    def addSeason(self, episodes, name=None):
        self.seasons.append(Season(episodes, name))
        

    def removeSeason(self, season):
        self.seasons.remove(season)
        