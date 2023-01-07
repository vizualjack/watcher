import customtkinter as ctk
from tracking.user import User
from seriesData.library import Library
from seriesData.series import Series
from seriesData.season import Season
from tracking.watchInfo import WatchInfo
from anisearch.anisearch import AniSearch, SearchResult
import eel


class GraphicalUI:
    def __init__(self, user:User, library:Library) -> None:
        global gui
        gui = self
        self.user = user
        self.library = library
        self.seriesList = list()
        self.searchResult = SearchResult()
        self.selectedSeries: Series = None
        self.loadBase = ""
        eel.init("./ui/gui")

    
    def use(self):
        eel.start('list/page.html')


# gui object for web functions
gui:GraphicalUI = None

# helper functions
def convertSeasonToDict(season: Season):
    seasonDict = dict()
    seasonDict["episodes"] = season.episodes
    seasonDict["name"] = season.name
    return seasonDict


def convertSeriesToDict(series: Series):
    seriesDict = dict()
    seriesDict["name"] = series.name
    try:
        seriesDict["image"] = series.image
        seriesDict["desc"] = series.desc
        seriesDict["link"] = series.link
    except:
        print("old series object")
    seasonsList = list()
    for season in series.seasons:
        seasonsList.append(convertSeasonToDict(season))
    seriesDict["seasons"] = seasonsList
    return seriesDict


def convertWatchInfoToDict(watchInfo: WatchInfo):
    watchInfoDict = dict()
    if watchInfo:
        watchInfoDict["season"] = watchInfo.getSeason()
        watchInfoDict["maxSeason"] = watchInfo.getSeriesSeasons()
        watchInfoDict["episode"] = watchInfo.getEpisode()
        watchInfoDict["maxEpisode"] = watchInfo.getSeasonEpisodes()
        # watchInfoDict["watchLocation"] = watchInfo.getWatchLocation()
    return watchInfoDict


def convertSeriesListToDict(seriesList: list()):
    dictList = list()
    for series in seriesList:
        dictList.append(convertSeriesToDict(series))
    return dictList


# web functions
@eel.expose
def getSeries(listName):
    gui.seriesList.clear()
    if listName == "watchList":
        for watchInfo in gui.user.watchInfos:
            gui.seriesList.append(watchInfo.getSeries())
    else:
        for series in gui.library.series:
            gui.seriesList.append(series)
    return convertSeriesListToDict(gui.seriesList)


@eel.expose
def selectSeries(index):
    gui.selectedSeries = gui.seriesList[index]
    gui.loadBase = "list"


@eel.expose
def getWatchInfo():
    return convertWatchInfoToDict(gui.user.getWatchInfoForSeries(gui.selectedSeries))


@eel.expose
def loadSeries(index):
    searchEntry = gui.searchResult[index]
    addInfo = AniSearch().loadFromSearchEntry(searchEntry)
    newSeries = Series(searchEntry.name)
    newSeries.image = searchEntry.image
    newSeries.desc = addInfo.desc
    for exSeason in addInfo.extractedSeasons:
        newSeries.addSeason(exSeason.episodes, exSeason.name)
    gui.selectedSeries = newSeries
    gui.loadBase = "search"


@eel.expose
def getSelectedSeries():
    return convertSeriesToDict(gui.selectedSeries)


@eel.expose
def searchSeries(searchText):
    gui.searchResult = AniSearch().search(searchText)
    print("Search result:" + str(len(gui.searchResult)))
    return getSearchResult()


@eel.expose
def getSearchResult():
    searchSeriesList = list()
    for searchEntry in gui.searchResult:
        searchSeries = Series(searchEntry.name)
        searchSeries.image = searchEntry.image
        searchSeriesList.append(convertSeriesToDict(searchSeries))
    return searchSeriesList


@eel.expose
def getBackLink():
    return f"/{gui.loadBase}/page.html"