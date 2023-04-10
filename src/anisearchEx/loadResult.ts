import { ExtractedSeason } from "./extractedSeason";
import { SearchEntry } from "./searchEntry";

export class LoadResult extends SearchEntry {
    desc:string;
    extractedSeasons: ExtractedSeason[];

    constructor(link:string) {
        super("","",link);
        this.desc = "";
        this.extractedSeasons = [];
    }

    async loadImageByLink(imageLink:string) {
        this.imageLink = imageLink;
        await this.loadImage();
    }
}