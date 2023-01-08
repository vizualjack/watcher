from anisearchEx.extractedSeason import ExtractedSeason
from anisearchEx.searchEntry import SearchEntry


ExtractedSeasons = list[ExtractedSeason]


class LoadResult(SearchEntry):
    def __init__(self,link) -> None:
        self.link = link
        self.name = ""
        self.image = ""
        self.desc = ""
        self.extractedSeasons = ExtractedSeasons()

    
    def loadImage(self, imageLink):
        self.image = self._downloadImage(imageLink)