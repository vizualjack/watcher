from bs4 import BeautifulSoup
from anisearchEx.anisearchLoader import load
from anisearchEx.searchEntry import SearchEntry
from anisearchEx.loadResult import LoadResult
from anisearchEx.extractedSeason import ExtractedSeason
from anisearchEx.relation import Relation
import json


SearchResult = list[SearchEntry]
Relations = list[Relation]


BASE_LINK = "https://www.anisearch.com/anime/"
class AniSearch:
    def loadFromLink(self, link: str) -> LoadResult:
        loadResult = LoadResult(link)
        pageLoader = self.__loadPage(loadResult.link)
        try:
            imageLink = pageLoader.find("img", attrs={"id": "details-cover"}).get("src")
            loadResult.loadImage(imageLink)
            loadResult.name = pageLoader.find("h1", attrs={"id": "htitle"}).text
            loadResult.desc = ""
            descEle = pageLoader.find("div", attrs={"class": "textblock details-text", "lang": "en"})
            if descEle:
                loadResult.desc = ""
                for content in descEle.contents:
                    if not content.name:
                        loadResult.desc += content
                    elif content.name == "a":
                        loadResult.desc += content.text
            infoblock = pageLoader.find("ul", attrs={"class": "xlist row simple infoblock"})
            episodes = infoblock.find("div", attrs={"class": "type"}).text.split(", ")
            episodes = episodes[len(episodes)-1].strip().split(" ")
            episodes = episodes[0]
            loadResult.extractedSeasons.append(ExtractedSeason(episodes, loadResult.name))
            self.__loadSequelSeasons(loadResult)
        except Exception as ex:
            print("Exception on extracting infos from: " + loadResult.link)
            print(ex)
        return loadResult

        
    def search(self, searchText) -> SearchResult:
        searchResult = SearchResult()
        pageLoader = self.__loadPage(f"{BASE_LINK}index?text={searchText}")
        for entry in self.__entriesAsList(pageLoader):
            linkElement = entry.find("a")
            name = self.__getNameFromLinkElement(linkElement)
            imageLink = self.__getImageLinkFromLinkElement(linkElement)
            link = self.__getLinkFromLinkElement(linkElement)
            searchResult.append(SearchEntry(name, imageLink, link))
        return searchResult


    def __loadPage(self, link) -> BeautifulSoup:
        content = load(link)
        return BeautifulSoup(content)

    
    def __entriesAsList(self, pageLoader: BeautifulSoup):
        list = pageLoader.find("ul", attrs={"class", "covers gallery"})
        return list.find_all("li")


    def __getNameFromLinkElement(self, linkElement):
        return linkElement.get("title").replace("Anime: ", "")


    def __getImageLinkFromLinkElement(self, linkElement):
        return linkElement.get("data-bg")
    
    def __getLinkFromLinkElement(self, linkElement):
        return linkElement.get("href").replace("anime/", "https://www.anisearch.com/anime/")


    def __loadSequelSeasons(self, loadResult:LoadResult):
        dataGraph = self.__getDataGraph(f"{loadResult.link}/relations")
        relations = self.__getSequelRelations(dataGraph)
        extractedSeasons = loadResult.extractedSeasons
        while True: 
            lastSeason = extractedSeasons[len(extractedSeasons)-1]
            nextSeason = None
            for relation in relations:
                if relation.frm.name == lastSeason.name:
                    nextSeason = relation.to
            if nextSeason == None:
                break
            extractedSeasons.append(nextSeason)

        
    def __getDataGraph(self, link):
        pageLoader = self.__loadPage(link)
        dataGraph = None
        for div in pageLoader.find_all("div"):
            if div.get("id") == "flowchart":
                dataGraph = json.loads(div.get("data-graph"))
                break
        return dataGraph


    def __getSequelRelations(self, dataGraph):
        sequelRelationId = self.__getSequelRelationId(dataGraph)
        animeDict = dataGraph["nodes"]["anime"]
        relations = Relations()
        for edge in dataGraph["edges"]:
            if edge["relation"] != sequelRelationId:
                continue
            frm = self.__extractSeason(animeDict[edge["from"]]["title"])
            to = self.__extractSeason(animeDict[edge["to"]]["title"])
            relations.append(Relation(frm, to))
        return relations


    def __extractSeason(self, titleString):
        splitted = titleString.split("<span>")
        name = splitted[0]
        episodes = splitted[1].split(", ")[1].split(" ")[0]
        if episodes == "?":
            episodes = -1
        return ExtractedSeason(episodes, name)


    def __getSequelRelationId(self, dataGraph):
        sequelId = -1
        for name in dataGraph["legend"]:
            sequelId += 1
            if name == "Sequel":
                break
        return sequelId


    