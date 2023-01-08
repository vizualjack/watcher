from anisearchEx.extractedSeason import ExtractedSeason


class Relation:
    def __init__(self, frm:ExtractedSeason, to:ExtractedSeason):
        self.frm = frm
        self.to = to