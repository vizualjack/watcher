import unittest
import requests

from anisearchLoader import load
from .anisearch import AniSearch
from .searchEntry import SearchEntry


class Tests(unittest.TestCase):
    def test_search(self):
        TEST_ANIME = "Sword Art Online"
        anisearch = AniSearch()
        saoEntry = None
        for searchEntry in anisearch.search("sao"):
            if searchEntry.name == TEST_ANIME:
                saoEntry = searchEntry
                break
        self.assertIsNotNone(saoEntry)
        self.assertNotEqual(len(saoEntry.image), 0, "no image")
        self.assertNotEqual(len(saoEntry.link), 0, "no link")
        with open("image.webp", "wb") as file:
            file.write(saoEntry.image)
            file.close()
            

if __name__ == '__main__':
    unittest.main()