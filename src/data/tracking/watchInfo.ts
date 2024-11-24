import { Series } from "../series";
import { logger } from '../../logger';

export class WatchInfo {
    series:Series;
    season:number;
    episode:number;
    watchLocation:string;

    constructor(series:Series) {
        this.series = series;
        this.season = 1;
        this.episode = 1;
        this.watchLocation = "";
    }

    getEpisode() {
        this.#checkForNewSeason()
        return this.episode
    }

    getSeason() {
        this.#checkForNewSeason()
        return this.season
    }

    getSeriesSeasons() {
        return this.series.seasons.length;
    }

    getSeasonEpisodes() {
        return this.#getCurrentSeason().episodes;
    }

    getSeasonName() {
        return this.#getCurrentSeason().name;
    }

    watchLocationIsWebLink() {
        return this.watchLocation.startsWith("https://") || this.watchLocation.startsWith("http://")
    }

    nextEpisode() {
        let curSeasonIndex = this.season-1;
        if (curSeasonIndex >= this.series.seasons.length) return;
        let curSeason = this.series.seasons[curSeasonIndex];
        let lastSeasonIndex = this.series.seasons.length - 1;
        if (curSeasonIndex == lastSeasonIndex && this.episode > curSeason.episodes) return;
        this.episode += 1;
        if (lastSeasonIndex > curSeasonIndex && this.episode > curSeason.episodes) {
            this.episode = 1;
            this.season += 1;
        }
    }

    unseenEpisodes() {
        let curSeasonIndex = this.season - 1;
        let lastSeasonIndex = this.series.seasons.length - 1;
        if (curSeasonIndex > lastSeasonIndex) {
            logger.info("Current season index is higher than last season index");
            return false;
        }
        if (curSeasonIndex < lastSeasonIndex) return true;
        let lastSeasonEpisodes = this.series.seasons[lastSeasonIndex].episodes;
        if (this.episode <= lastSeasonEpisodes) return true;
        return false;
    }

    toPersVersion() {
        let persVer = new WatchInfoPers();
        persVer.seriesId = this.series.id;
        persVer.season = this.season;
        persVer.episode = this.episode;
        persVer.watchLocation = this.watchLocation;
        return persVer;
    }

    #checkForNewSeason() {
        let curSeasonIndex = this.season-1;
        let curSeason = this.series.seasons[curSeasonIndex];
        if (curSeason.episodes >= this.episode) return;
        let lastSeasonIndex = this.series.seasons.length-1;
        if (lastSeasonIndex > curSeasonIndex) {
            this.season += 1;
            this.episode = 1;
        }
    }

    #getCurrentSeason() {
        this.#checkForNewSeason();
        let curSeasonIndex = this.season-1;
        return this.series.seasons[curSeasonIndex];
    }
}

export class WatchInfoPers {
    seriesId:number;
    season:number;
    episode:number;
    watchLocation:string;

    constructor() {
        this.seriesId = -1;
        this.season = 1;
        this.episode = 1;
        this.watchLocation = "";
    }

    toWatchInfo(seriesForId:Series) {
        let watchInfo = new WatchInfo(seriesForId);
        watchInfo.season = this.season;
        watchInfo.episode = this.episode;
        watchInfo.watchLocation = this.watchLocation;        
        return watchInfo;
    }
}