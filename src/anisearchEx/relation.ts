import { ExtractedSeason } from "./extractedSeason";

export class Relation {
    frm: ExtractedSeason;
    to: ExtractedSeason;

    constructor(frm:ExtractedSeason, to:ExtractedSeason) {
        this.frm = frm;
        this.to = to;
    }
}