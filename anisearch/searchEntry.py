from anisearchLoader import load

BASE_LINK = "https://cdn.anisearch.com/images/"
class SearchEntry:
    def __init__(self, name, imageLink, link) -> None:
        self.name = name
        self.image = self.__downloadImage(imageLink)
        self.link = link

    
    def __downloadImage(self, link) -> bytes:
        bigImageLink = link.replace("full/", "")
        bigImageLink = bigImageLink.replace(".webp", "_300.webp")
        bigImageLink = f"{BASE_LINK}{bigImageLink}"
        return load(bigImageLink)