from anisearchEx.anisearchLoader import load
import base64

BASE_LINK = "https://cdn.anisearch.com/images/"
class SearchEntry:
    def __init__(self, name, imageLink, link) -> None:
        self.name = name
        self.image = self._downloadImage(self.__convertToImageLink(imageLink))
        self.link = link


    def __convertToImageLink(self, link):
        bigImageLink = link.replace("full/", "")
        bigImageLink = bigImageLink.replace(".webp", "_300.webp")
        return f"{BASE_LINK}{bigImageLink}"

    
    def _downloadImage(self, link) -> str:        
        base64Image = base64.b64encode(load(link)).decode()
        return f"data:image/webp;base64,{base64Image}"