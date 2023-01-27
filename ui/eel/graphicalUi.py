from tracking.user import User
from seriesData.library import Library
from seriesData.series import Series
from seriesData.season import Season
from tracking.watchInfo import WatchInfo
from anisearchEx.anisearch import AniSearch, SearchResult
import eel
import sys
import gevent as gvt
import webbrowser as wb
import sys
import whichcraft as wch


LB_LIST = "list"
LB_SEARCH = "search"

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
        eel.init("./ui/eel")

    
    def use(self):
        eel.start('list/page.html', close_callback=self._close_callback)
        # eel.start('list/page.html', close_callback=self._close_callback, mode="custom", cmdline_args=[wch.which('electron'), "http://localhost:8000/list/page.html"])


    def doAction(self):
        if self.loadBase == LB_SEARCH:
            self.library.addSeries(self.selectedSeries)
            self.loadBase = LB_LIST
        elif self.loadBase == LB_LIST:
            watchInfo = self.user.getWatchInfoForSeries(self.selectedSeries)
            if watchInfo:
                self.user.removeSeries(self.selectedSeries)
            else:
                self.user.addSeries(self.selectedSeries)
        return self.getActionText()


    def getActionText(self):
        if self.loadBase == LB_SEARCH:
            return "Add to library"
        elif self.loadBase == LB_LIST:
            watchInfo = self.user.getWatchInfoForSeries(self.selectedSeries)
            if watchInfo:
                return "Remove from watch list"
            else:
                return "Add to watch list"

    
    def _detect_shutdown(self):
        if len(eel._websockets) == 0:
            self.onClose()
            sys.exit()


    def _close_callback(self, p1, p2):
        gvt.spawn_later(1, self._detect_shutdown)


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
    watchStatus = 0
    watchInfo = gui.user.getWatchInfoForSeries(series)
    if watchInfo:
        watchStatus = 1
        if not watchInfo.unseenEpisodes():
            watchStatus = 2
    seriesDict["watchStatus"] = watchStatus
    return seriesDict


def convertWatchInfoToDict(watchInfo: WatchInfo):
    watchInfoDict = dict()
    if watchInfo:
        watchInfoDict["season"] = watchInfo.getSeason()
        watchInfoDict["maxSeason"] = watchInfo.getSeriesSeasons()
        watchInfoDict["episode"] = watchInfo.getEpisode()
        watchInfoDict["maxEpisode"] = watchInfo.getSeasonEpisodes()
        if watchInfo.watchLocationIsWebLink():
            watchInfoDict["watchLocation"] = watchInfo.getWatchLocation()
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
    gui.loadBase = LB_LIST


@eel.expose
def getWatchInfo():
    return convertWatchInfoToDict(gui.user.getWatchInfoForSeries(gui.selectedSeries))


@eel.expose
def loadSeries(index):
    searchEntry = gui.searchResult[index]
    addInfo = AniSearch().loadFromLink(searchEntry.link)
    newSeries = Series(addInfo.name)
    newSeries.image = addInfo.image
    newSeries.desc = addInfo.desc
    newSeries.link = searchEntry.link
    for exSeason in addInfo.extractedSeasons:
        newSeries.addSeason(exSeason.episodes, exSeason.name)
    gui.selectedSeries = newSeries
    gui.loadBase = LB_SEARCH


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


@eel.expose
def setSeason(newSeason):
    watchInfo = gui.user.getWatchInfoForSeries(gui.selectedSeries)
    try: 
        newSeason = int(newSeason)
        watchInfo.season = newSeason
        watchInfo.episode = 1
    except:
        print("Can't set season")
    return convertWatchInfoToDict(watchInfo)


@eel.expose
def setEpisode(newEpisode):
    watchInfo = gui.user.getWatchInfoForSeries(gui.selectedSeries)
    try: 
        newEpisode = int(newEpisode)
        watchInfo.episode = newEpisode
    except:
        print("Can't set episode")
    return convertWatchInfoToDict(watchInfo)


@eel.expose
def setWatchLocation(newWatchLoc):
    watchInfo = gui.user.getWatchInfoForSeries(gui.selectedSeries)
    watchInfo.watchLocation = newWatchLoc
    return convertWatchInfoToDict(watchInfo)


@eel.expose
def action():
    return gui.doAction()


@eel.expose
def getActionText():
    return gui.getActionText()


@eel.expose
def nextEpisode():
    watchInfo = gui.user.getWatchInfoForSeries(gui.selectedSeries)
    watchInfo.nextEpisode()
    return convertWatchInfoToDict(watchInfo)

@eel.expose
def openWatchPage():
    watchInfo = gui.user.getWatchInfoForSeries(gui.selectedSeries)
    wb.open(watchInfo.watchLocation)