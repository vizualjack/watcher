from seriesData.library import Library
from seriesData.series import Series
from tracking.user import User
import time
import keyboard


class ConsoleUI:
    def __init__(self, user:User, library:Library) -> None:
        self.user = user
        self.library = library

    
    def use(self):
        while True:
            self.__printOptions()
            option = input()
            if option == "":
                return
            elif option == "l":
                while option != "":
                    self.__printLibraryOptions()
                    option = input()
                    if option == "c":
                        self.__createSeries()
                    elif option == "l":
                        self.__listSeries()
                    elif option == "e":
                        self.__editSeriesList()
            # elif option == "u":
            #     self.__printUserOptions()
            #     option = input()


    def __printOptions(self):
        # print("User - u")
        print("Library - l")


    # def __printUserOptions(self):
    #     print("Nothing here")

    def __printLibraryOptions(self):
        print("List series - l")
        print("Create series - c")
        print("Edit series - e")


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


    def __editSeriesList(self):
        if len(self.library.series) == 0:
            print("No series")
            return
        series = self.__selectSeries()
        print(series.name + " selected")

    
    def __selectSeries(self):
        seriesList = self.library.series
        selectedIndex = 0
        print("Use arrow and enter key to select series")
        time.sleep(0.1)
        while True:
            selectedSeries = self.library.series[selectedIndex]
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