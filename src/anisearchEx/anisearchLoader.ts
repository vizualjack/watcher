import {Readable} from 'stream';

const get = require("simple-get");


async function readableToString(readableStream:Readable) {
    let result = '';
    for await(const chunk of readableStream) {
        result += chunk;
    }
    return result;
}

function load(link:string) {
    return new Promise<Readable>((resolve, reject) => {
        get(link, function(err:any,res:Readable) {
            if (err) reject(err);
            resolve(res)
        })
    })
}


export async function loadImageAsBase64(link:string) {
    let stream = await load(link);
    stream.setEncoding("base64");
    return await readableToString(stream);
}

export async function loadHtml(link:string) {
    let stream = await load(link);
    return await readableToString(stream);
}