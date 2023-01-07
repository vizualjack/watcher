from .anisearchLoader import load
import base64

BASE_LINK = "https://cdn.anisearch.com/images/"
class SearchEntry:
    def __init__(self, name, imageLink, link) -> None:
        self.name = name
        self.image = self.__downloadImage(imageLink)
        self.link = link

    
    def __downloadImage(self, link) -> str:
        bigImageLink = link.replace("full/", "")
        bigImageLink = bigImageLink.replace(".webp", "_300.webp")
        bigImageLink = f"{BASE_LINK}{bigImageLink}"
        base64Image = base64.b64encode(load(bigImageLink)).decode()
        return f"data:image/webp;base64,{base64Image}"