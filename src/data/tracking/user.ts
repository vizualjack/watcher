import { Series } from "../series";
import { WatchInfo } from "./watchInfo";


export class User {
    watchInfos: WatchInfo[];
    constructor() {
        this.watchInfos = [];
    }

    getWatchInfoForSeries(series:Series) {
        for(let i = 0; i < this.watchInfos.length;i++) {
            let watchInfo = this.watchInfos[i];
            if (watchInfo.series == series) return watchInfo;
        }
        return null;
    }

    addSeries(series:Series) {
        let watchInfo = this.getWatchInfoForSeries(series);
        if (watchInfo == null) this.watchInfos.push(new WatchInfo(series));
    }

    removeSeries(series:Series) {
        let watchInfo = this.getWatchInfoForSeries(series);
        if (watchInfo == null) return;
        let index = this.watchInfos.indexOf(watchInfo);
        if(index == -1) return;
        this.watchInfos.splice(index, 1);
    }
}