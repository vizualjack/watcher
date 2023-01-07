import customtkinter as ctk
from tracking.user import User
from seriesData.library import Library
from seriesData.series import Series
from seriesData.season import Season
from anisearch.anisearch import AniSearch, SearchResult
import eel


class GraphicalUI:
    def __init__(self, user:User, library:Library) -> None:
        global gui
        gui = self
        self.user = user
        self.library = library
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


# web functions
@eel.expose
def getSeries():
    seriesList = list()
    for series in gui.library.series:
        seriesList.append(convertSeriesToDict(series))
    return seriesList


@eel.expose
def selectSeries(index):
    gui.selectedSeries = gui.library.series[index]
    gui.loadBase = "list"


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