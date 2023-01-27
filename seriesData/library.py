from seriesData.series import Series


# SeriesList = list[Series]


class Library:
    def __init__(self, series:list=None) -> None:
        # self.series = SeriesList()
        self.series = list()
        if series != None:
            self.series = series

    
    def addSeries(self, series:Series):
        self.series.append(series)


    def removeSeries(self, series:Series):
        self.series.remove(series)