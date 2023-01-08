import unittest
from anisearchEx.anisearch import AniSearch


class Tests(unittest.TestCase):
    def test_search(self):
        TEST_ANIME = "Sword Art Online"
        saoEntry = None
        for searchEntry in AniSearch().search("sao"):
            if searchEntry.name == TEST_ANIME:
                saoEntry = searchEntry
                break
        self.assertIsNotNone(saoEntry)
        self.assertNotEqual(len(saoEntry.image), 0, "no image")
        self.assertNotEqual(len(saoEntry.link), 0, "no link")

    
    def test_load(self):
        loadResult = AniSearch().loadFromLink("https://www.anisearch.com/anime/7335,sword-art-online")
        self.assertEqual(loadResult.name, "Sword Art Online")
        self.assertNotEqual(len(loadResult.image), 0)
        self.assertNotEqual(len(loadResult.desc), 0)
        self.assertEqual(len(loadResult.extractedSeasons), 7)
        self.assertEqual(loadResult.extractedSeasons[0].name, "Sword Art Online")
        self.assertEqual(loadResult.extractedSeasons[0].episodes, 25)
        self.assertEqual(loadResult.extractedSeasons[6].name, "Sword Art Online: Alicization - War of Underworld Part 2")
        self.assertEqual(loadResult.extractedSeasons[6].episodes, 11)



if __name__ == '__main__':
    unittest.main()