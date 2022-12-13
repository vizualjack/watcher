from seriesData.library import Library
from seriesData.series import Series
from tracking.user import User
from tracking.watchInfo import WatchInfo
import time
import keyboard
import os


WatchInfos = list[WatchInfo]


class ConsoleUI:
    def __init__(self, user:User, library:Library) -> None:
        self.user = user
        self.library = library

    
    def use(self):
        while True:
            self.__printOptions()
            option = input()
            if option == "e":
                return
            elif option == "l":
                while option != "b":
                    self.__printLibraryOptions()
                    option = input()
                    if option == "c":
                        self.__createSeries()
                    elif option == "l":
                        self.__listSeries()
                    elif option == "lnw":
                        self.__listNonWatchedSeries()
                    elif option == "e":
                        self.__editSeriesList()
            elif option == "u":
                while option != "b":
                    self.__printUserOptions()
                    option = input()
                    if option == "as":
                        series = self.__selectNonWatchedSeries()
                        input(series.name + " selected")
                        confirm = input("Wanna add? y/n: ")
                        if confirm == "y":
                            if self.user.addSeries(series):
                                print("Added series to user")
                            else:
                                print("Series already in list")
                    elif option == "rs":
                        watchInfo = self.__selectWatchInfo()
                        input()
                        option = input("Type 'yes' for remove " + watchInfo.series.name + " from your list: ")
                        if option == "yes":
                            self.user.removeSeries(watchInfo.series)
                            print("Removed series!")
                    elif option == "ls":
                        self.__printWatchInfos(self.user.watchInfos)
                    elif option == "wm":
                        watchInfo = self.__selectWatchInfo()
                        while option != "e":
                            os.system("cls")
                            print("Watch mode")
                            self.__printWatchInfo(watchInfo)
                            self.__printWatchModeOptions()
                            option = input()
                            if option == "n":
                                watchInfo.nextEpisode()
                            elif option == "se":
                                print("Episodes in season 1-" + str(watchInfo.getSeasonEpisodes()))
                                newEpisode = int(input())
                                if newEpisode > 0 and newEpisode <= watchInfo.getSeasonEpisodes():
                                    watchInfo.episode = newEpisode
                            elif option == "sb":
                                numOfSeasons = len(watchInfo.series.seasons)
                                watchInfo.season = 1
                                if numOfSeasons > 1:
                                    print("Seasons 1-" + str(numOfSeasons))
                                    newSeason = int(input())
                                    if newSeason > 0 and newSeason <= numOfSeasons:
                                        watchInfo.season = newEpisode
                                print("Episodes in season 1-" + str(watchInfo.getSeasonEpisodes()))
                                newEpisode = int(input())
                                if newEpisode > 0 and newEpisode <= watchInfo.getSeasonEpisodes():
                                    watchInfo.episode = newEpisode
                        

    def __printWatchModeOptions(self):
        print("Next episode - n")
        print("Set episode - se")
        print("Set season and episode - sb")
        print("End - e")


    def __printWatchInfo(self, watchInfo:WatchInfo):
        print(watchInfo.getSeries().name)
        print("Season " + str(watchInfo.getSeason()))
        print("Episode " + str(watchInfo.getEpisode()) + "/" + str(watchInfo.getSeasonEpisodes()))


    def __printWatchInfos(self, watchInfos:WatchInfos):
        if len(watchInfos) == 0:
            print("No series in your list")
        for watchInfo in watchInfos:
            print(watchInfo.series.name + " Season " + str(watchInfo.season) + " Episode " + str(watchInfo.episode))


    def __printUserOptions(self):
        print("Add series - as")
        print("Remove series - rs")
        print("List series - ls")
        print("Watch mode - wm")
        print("Back - b")


    def __printOptions(self):
        print("User - u")
        print("Library - l")
        print("Save and end - e")


    def __printLibraryOptions(self):
        print("List series - l")
        print("List non watched series - lnw")
        print("Create series - c")
        print("Edit series - e")
        print("Back - b")


    def __createSeries(self):
        name = input("Name: ")
        if name == "":
            return
        newSeries = Series(name)
        print("Create seasons (no input = no more seasons)")
        while True:
            season = len(newSeries.seasons)+1
            season = str(season)
            episodeText = input("Episode of season " + season + ":")
            if episodeText == "":
                break
            episodes = int(episodeText)
            if episodes <= 0:
                break
            newSeries.addSeason(episodes)
        if len(newSeries.seasons) == 0:
            return
        self.library.addSeries(newSeries)
        print("New series added")
        
    
    def __listSeries(self):
        if len(self.library.series) == 0:
            print("No series")
            return
        for series in self.library.series:
            print(series.name)

    
    def __listNonWatchedSeries(self):
        if len(self.library.series) == 0:
            print("No series")
            return
        for series in self.library.series:
            if self.user.getWatchInfoForSeries(series) == None:
                print(series.name)


    def __editSeriesList(self):
        if len(self.library.series) == 0:
            print("No series")
            return
        series = self.__selectSeries()
        print("Edit " + series.name)
        self.__printEditOptions()
        option = ""
        while option == "":
            option = input("")
        if option == "b":
            return
        elif option == "r":
            newName = input("New name: ")
            if newName == "":
                return
            series.name = newName
            print("Renamed!")
        elif option == "cs":
            self.__printSeasons(series)
            while True:
                season = input("Which season you wanna edit? ")
                if season == "":
                    break
                seasonIndex = int(season)-1
                if seasonIndex < 0 or seasonIndex >= len(series.seasons):
                    continue
                season = series.seasons[seasonIndex]
                print("Edit season " + season)
                self.__printSeasonInfo(season)
                self.__printSeasonEditOptions()
                option = input("")
                if option == "n":
                    newName = input("New name: ")
                    if newName == "":
                        return
                    season.name = newName
                    print("Name changed!")
                elif option == "e":
                    newEpisodes = input("New episodes: ")
                    if newEpisodes == "":
                        return
                    newEpisodes = int(newEpisodes)
                    season.episodes = newEpisodes
                elif option == "delete":
                    series.removeSeason(season)
                    print("Season deleted!")
        elif option == "as":
            episodes = input("Episodes: ")
            if episodes == "":
                return
            episodes = int(episodes)
            if episodes <= 0:
                return
            seasonName = input("Season name(optional): ")
            series.addSeason(episodes, seasonName)
            print("Season added!")
        elif option == "delete":
            option = input("Type 'yes' for delete: ")
            if option == "yes":
                self.user.removeSeries(series)
                self.library.removeSeries(series)
                print("Series deleted!")

    
    def __printSeasonEditOptions(self):
        print("Change name - n")
        print("Change episodes - e")
        print("Delete season - delete")


    def __printSeasonInfo(self, season):
        print("Name: " + season.name)
        print("Episodes: " + season.episodes)

    
    def __printEditOptions(self):
        print("Rename - r")
        print("Change season - cs")
        print("Add season - as")
        print("Delete season - delete")
        print("Back - b")


    def __printSeasons(self, series:Series):
        for seasonIndex in range(len(series.seasons)):
            season = series.seasons[seasonIndex]
            seasonNum = seasonIndex+1
            print(str(seasonNum) + ". " + season.name + " | " + str(season.episodes) + " episodes")


    def __selectSeriesInList(self, seriesList):
        selectedIndex = 0
        print("Use arrow and enter key to select series")
        time.sleep(0.1)
        while True:
            selectedSeries = seriesList[selectedIndex]
            name = selectedSeries.name
            name += " "*100
            print(name, end='\r')
            pressedKey = keyboard.read_key()
            time.sleep(0.1)
            if pressedKey == "enter":
                return selectedSeries
            elif pressedKey == "nach-oben":
                selectedIndex -= 1
            elif pressedKey == "nach-unten":
                selectedIndex += 1
            if selectedIndex >= len(seriesList):
                selectedIndex = 0
            elif selectedIndex < 0:
                selectedIndex = len(seriesList)-1

    
    def __selectSeries(self):
        return self.__selectSeriesInList(self.library.series)


    def __selectNonWatchedSeries(self):
        return self.__selectSeriesInList(self.__getNonWatchedSeries())


    def __getNonWatchedSeries(self):
        seriesList = [Series]
        for series in self.library.series:
            if self.user.getWatchInfoForSeries(series) == None:
                seriesList.append(series)
        return seriesList


    def __selectWatchInfo(self):
        watchInfos = self.user.watchInfos
        selectedIndex = 0
        print("Use arrow and enter key to select series")
        time.sleep(0.1)
        while True:
            selectedWatchInfo = self.user.watchInfos[selectedIndex]
            name = selectedWatchInfo.series.name
            name += " "*100
            print(name, end='\r')
            pressedKey = keyboard.read_key()
            time.sleep(0.1)
            if pressedKey == "enter":
                return selectedWatchInfo
            elif pressedKey == "nach-oben":
                selectedIndex -= 1
            elif pressedKey == "nach-unten":
                selectedIndex += 1
            if selectedIndex >= len(watchInfos):
                selectedIndex = 0
            elif selectedIndex < 0:
                selectedIndex = len(watchInfos)-1