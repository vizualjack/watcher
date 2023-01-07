from .extractedSeason import ExtractedSeason


ExtractedSeasons = list[ExtractedSeason]


class LoadResult:
    def __init__(self, name, link, image) -> None:
        self.name = name
        self.link = link
        self.image = image
        self.desc = ""
        self.extractedSeasons = ExtractedSeasons()