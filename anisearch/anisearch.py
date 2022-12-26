from bs4 import BeautifulSoup
from anisearchLoader import load
from searchEntry import SearchEntry


SearchResult = list[SearchEntry]


BASE_LINK = "https://www.anisearch.com/anime/"
class AniSearch:
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
        return linkElement.get("href").replace("anime/", "")