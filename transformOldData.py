from persister import Persister
from anisearchEx.anisearch import AniSearch
from seriesData.series import Series


if __name__ == "__main__":
    persister = Persister.load()
    newSeriesList = list()
    transformedSeries = 0
    for series in persister.library.series:
        try:
            if series.link != "":
                continue
        except:
            pass
        inputLink = input(f"Link for {series.name}: ")
        if len(inputLink) == 0:
            continue
        loadResult = AniSearch().loadFromLink(inputLink)
        newSeries = Series(loadResult.name)
        newSeries.desc = loadResult.desc
        newSeries.link = loadResult.link
        newSeries.image = loadResult.image
        for extractedSeason in loadResult.extractedSeasons:
            newSeries.addSeason(extractedSeason.episodes, extractedSeason.name)
        watchInfo = persister.user.getWatchInfoForSeries(series)#
        if watchInfo:
            watchInfo.series = newSeries
        newSeriesList.append(newSeries)
        transformedSeries += 1
    persister.library.series = newSeriesList
    # persister.library.series.clear()
    # for series in newSeriesList:
    #     persister.library.series.append(series)
    print(f"Transformed {transformedSeries} series")
    persister.save()