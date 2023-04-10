export class Season {
    name: string|undefined;
    episodes: number;
    constructor(name:string|undefined = undefined, episodes:number = 0) {
        this.name = name;
        this.episodes = episodes;
    }
}