import {loadHtml, loadImageAsBase64} from './anisearchEx/anisearchLoader';
import fs from 'fs';
import { read } from 'original-fs';
import {Readable} from 'stream';




async function main() {
    let page = await loadHtml("https://www.anisearch.com/anime/7335,sword-art-online");
    // stream.pipe(fs.createWriteStream("test.webp"));
    // stream.read()
    fs.writeFileSync("test.html", page);
    console.log("done");
}

main();