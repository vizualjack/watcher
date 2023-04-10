import { Series } from './series';


export class Library {
    series: Series[];
    constructor() {
        this.series = [];
    }

    getSeriesById(seriesId: number) {
        for(let i = 0; i < this.series.length; i++) {
            let cSeries = this.series[i];
            if (cSeries.id == seriesId) return cSeries;
        }
        return null;
    }
    
    addSeries(series:Series) {
        if (series != null) {
            series.id = this.#getIdForNewSeries();
            this.series.push(series);
        }
    }

    removeSeries(series:Series) {
        let index = this.series.indexOf(series);
        if (index == -1) return;
        this.series.splice(index,1);
    }

    #getIdForNewSeries() {
        if(this.series.length == 0) return 0;
        let lastSeries = this.series[this.series.length-1];
        return lastSeries.id + 1;
    }
}