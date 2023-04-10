// import base64 from 'base-64';
import {loadImageAsBase64} from './anisearchLoader';

const BASE_LINK = "https://cdn.anisearch.com/images/";

export class SearchEntry {
    name:string;
    imageLink:string;
    link:string;
    image:string;

    constructor(name:string, imageLink:string, link:string) {
        this.name = name;
        this.imageLink = imageLink;
        this.link = link;
        this.image = "";
    }

    #convertToImageLink(link:string) {
        let bigImageLink = link.replace("full/", "");
        bigImageLink = bigImageLink.replace(".webp", "_300.webp");
        return `${BASE_LINK}${bigImageLink}`;
    }

    async loadImage() {
        let base64Image = await loadImageAsBase64(this.#convertToImageLink(this.imageLink));
        this.image = `data:image/webp;base64,${base64Image}`;
    }
}