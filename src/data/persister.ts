// @ts-nocheck
import fs from 'fs';
import { Library } from './library';
import { User } from './tracking/user';
import { WatchInfoPers } from './tracking/watchInfo';
import { Series } from './series';

const FILE_NAME = "data.json";
const KEY_SERIES = "librarySeries";
const KEY_WATCHINFOS = "userWatchInfos";


export class Persister {
    savePath:string;
    library:Library;
    user:User;

    constructor(saveDir:string) {
        this.savePath = saveDir + FILE_NAME;
        this.library = new Library();
        this.user = new User();
    }

    load() {
        if (!fs.existsSync(this.savePath)) return;
        let data = JSON.parse(fs.readFileSync(this.savePath).toString());
        this.library.series = data[KEY_SERIES] as Series[];
        let watchInfosPer = this.#loadWatchInfosPers(data[KEY_WATCHINFOS]);
        for (let i = 0; i < watchInfosPer.length; i++) {
            let watchInfoPer = watchInfosPer[i];
            let seriesForId = this.library.getSeriesById(watchInfoPer.seriesId);
            if (seriesForId == null) {
                console.log("No series for id: " + watchInfoPer.seriesId);
                continue
            }
            this.user.watchInfos.push(watchInfoPer.toWatchInfo(seriesForId));
        }
        console.log("Loaded data");
    }

    save() {
        let watchInfosPer = [];
        for (let i = 0; i < this.user.watchInfos.length; i++) {
            let watchInfo = this.user.watchInfos[i];
            watchInfosPer.push(watchInfo.toPersVersion());
        }
        let data = {};
        data[KEY_SERIES] = this.library.series;
        data[KEY_WATCHINFOS] = watchInfosPer;
        fs.writeFileSync(this.savePath, JSON.stringify(data));
        console.log("Data saved");
    }

    #loadWatchInfosPers(onlyDataWatchInfos:WatchInfoPers[]) {
        let loadedWatchInfos = [];
        for (let i = 0; i < onlyDataWatchInfos.length; i++) {
            let onlyDataWatchInfo = onlyDataWatchInfos[i];
            let newWatchInfoPers = new WatchInfoPers();
            newWatchInfoPers.episode = onlyDataWatchInfo.episode;
            newWatchInfoPers.season = onlyDataWatchInfo.season;
            newWatchInfoPers.seriesId = onlyDataWatchInfo.seriesId;
            newWatchInfoPers.watchLocation = onlyDataWatchInfo.watchLocation;
            loadedWatchInfos.push(newWatchInfoPers);
        }
        return loadedWatchInfos;
    }
}