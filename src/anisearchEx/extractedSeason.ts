export class ExtractedSeason {
    episodes: number;
    name:string|undefined;

    constructor(episodes:number, name:string|undefined = undefined) {
        this.episodes = episodes;
        this.name = name;
    }
}