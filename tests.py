import unittest
from seriesData.library import Library
from seriesData.series import Series
from tracking.user import User
from persister import Persister

class Tests(unittest.TestCase):
    def test_1(self):
        seriesName = "testSeries"
        firstSeasonEpisodes = 3
        secondSeasonEpisodes = 5
        secondSeasonName = "fiveEpisodes"

        library = Library()
        series = Series(seriesName)
        series.addSeason(firstSeasonEpisodes)
        series.addSeason(secondSeasonEpisodes, secondSeasonName)
        library.addSeries(series)
        saver = Persister()
        saver.library = library
        saver.save()

        loader = Persister.load()
        loadedLibrary = loader.library
        self.assertEqual(1, len(loadedLibrary.series), "no series in loaded library")
        loadedSeries = loadedLibrary.series[0]
        self.assertEqual(seriesName, loadedSeries.name)
        self.assertEqual(2, len(loadedSeries.seasons))
        self.assertEqual(firstSeasonEpisodes, loadedSeries.seasons[0].episodes)
        self.assertIsNone(loadedSeries.seasons[0].name)
        self.assertEqual(secondSeasonEpisodes, loadedSeries.seasons[1].episodes)
        self.assertEqual(secondSeasonName, loadedSeries.seasons[1].name)

    
    def test_2(self):
        seriesName = "testSeries"
        firstSeasonEpisodes = 3
        secondSeasonEpisodes = 5
        secondSeasonName = "fiveEpisodes"

        library = Library()
        series = Series(seriesName)
        series.addSeason(firstSeasonEpisodes)
        series.addSeason(secondSeasonEpisodes, secondSeasonName)
        library.addSeries(series)
        user = User()
        user.addSeries(series)
        saver = Persister()
        saver.library = library
        saver.user = user
        saver.save()
        
        loader = Persister.load()
        loadedUser = loader.user
        loadedLibrary = loader.library
        loadedLibrary.series[0].name = "changed"
        self.assertEqual(loadedLibrary.series[0].name, loadedUser.watchInfos[0].getSeries().name)


    def test_3(self):
        series = Series("test")
        series.addSeason(2)
        series.addSeason(1)
        series.addSeason(1)
        series.addSeason(4)
        user = User()
        user.addSeries(series)
        watchInfo = user.watchInfos[0]
        self.assertEqual(1, watchInfo.getSeason())
        self.assertEqual(1, watchInfo.getEpisode())
        watchInfo.nextEpisode() # 1 2
        watchInfo.nextEpisode() # 2 1
        watchInfo.nextEpisode() # 3 1
        self.assertEqual(3, watchInfo.getSeason())
        self.assertEqual(1, watchInfo.getEpisode())
        self.assertTrue(watchInfo.unseenEpisodes())
        watchInfo.nextEpisode() # 4 1
        watchInfo.nextEpisode() # 4 2
        watchInfo.nextEpisode() # 4 3
        watchInfo.nextEpisode() # 4 4
        watchInfo.nextEpisode() # 4 5
        self.assertEqual(4, watchInfo.getSeason())
        self.assertEqual(5, watchInfo.getEpisode())
        self.assertFalse(watchInfo.unseenEpisodes())
        watchInfo.nextEpisode() # 4 5
        watchInfo.nextEpisode() # 4 5
        watchInfo.nextEpisode() # 4 5
        self.assertEqual(4, watchInfo.getSeason())
        self.assertEqual(5, watchInfo.getEpisode())
        self.assertFalse(watchInfo.unseenEpisodes())
        series.seasons[3].episodes = 5
        self.assertTrue(watchInfo.unseenEpisodes())
        watchInfo.nextEpisode() # 4 6
        self.assertFalse(watchInfo.unseenEpisodes())
        self.assertEqual(4, watchInfo.getSeason())
        self.assertEqual(6, watchInfo.getEpisode())
        series.addSeason(7)
        self.assertTrue(watchInfo.unseenEpisodes())
        self.assertEqual(5, watchInfo.getSeason())
        self.assertEqual(1, watchInfo.getEpisode())
        self.assertTrue(watchInfo.unseenEpisodes())


    # def test_XXX(self):


if __name__ == '__main__':
    unittest.main()