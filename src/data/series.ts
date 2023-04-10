import { Season } from "./season";

export class Series {
    id:number;
    name:string;
    seasons: Season[];
    image:string;
    desc:string;
    link:string

    constructor(id:number, name:string) {
        this.id = id;
        this.name = name;
        this.seasons = [];
        this.image = "";
        this.desc = "";
        this.link = "";
    }

    addSeason(episodes:number, name:string|undefined=undefined) {
        this.seasons.push(new Season(name, episodes));
    }

    removeSeason(season:Season) {
        let index = this.seasons.indexOf(season);
        if(index == -1) return
        this.seasons.splice(index,1);
    }
}