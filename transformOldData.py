from persister import Persister
from anisearchEx.anisearch import AniSearch
from seriesData.series import Series


if __name__ == "__main__":    
    persister = Persister.load()
    newSeriesList = list()
    transformedSeries = 0
    for series in persister.library.series:
        inputLink = input(f"Link for {series.name}: ")
        if len(inputLink) == 0:
            newSeriesList.append(series)
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
    if len(newSeriesList) > 0:
        persister.library.series = newSeriesList
    print(f"Transformed {transformedSeries} series")
    persister.save()