import unittest
import requests
from bs4 import BeautifulSoup

from anisearchLoader import load
from anisearch import AniSearch
from searchEntry import SearchEntry
import json


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

    
    def test_load(self):
        anisearch = AniSearch()
        loadResult = anisearch.loadFromSearchEntry(SearchEntry("Sword Art Online", "anime/cover/full/7/7335.webp", "https://www.anisearch.com/anime/7335,sword-art-online"))
        self.assertNotEqual(len(loadResult.desc), 0)
        self.assertEqual(len(loadResult.extractedSeasons), 7)
        self.assertEqual(loadResult.extractedSeasons[0].name, "Sword Art Online")
        self.assertEqual(loadResult.extractedSeasons[0].episodes, 25)
        self.assertEqual(loadResult.extractedSeasons[6].name, "Sword Art Online: Alicization - War of Underworld Part 2")
        self.assertEqual(loadResult.extractedSeasons[6].episodes, 11)



if __name__ == '__main__':
    unittest.main()