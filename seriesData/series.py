from seriesData.season import Season


class Series:
    def __init__(self, name: str) -> None:
        self.name = name
        self.seasons = list()
        self.image = ""
        self.desc = ""
        self.link = ""


    def addSeason(self, episodes, name=None):
        self.seasons.append(Season(episodes, name))
        

    def removeSeason(self, season):
        self.seasons.remove(season)
        