import {Readable} from 'stream';
import {IncomingMessage} from 'http';
import {logger} from '../logger';

const get = require("simple-get");


async function readMessage(incomingMessage:IncomingMessage) {
    let result = '';
    for await(const chunk of incomingMessage) {
        result += chunk;
    }
    return {headers: incomingMessage.headers, message: result};
}

function load(link:string, cookies:any|undefined) {
    let headers:any = {};
    if(cookies) {
        let cookieText = "";
        for (let key in cookies) {
            cookieText += `${key}=${cookies[key]}; `;
        }
        headers["Cookie"] = cookieText;
    }
    logger.debug(`Loading ${link} with headers ${Object.entries(headers)}`);
    return new Promise<IncomingMessage>((resolve, reject) => {
        get({url: link, headers: headers}, function(err:any,res:IncomingMessage) {
            if (err) reject(err);
            resolve(res);
        })
    })
}


export async function loadImageAsBase64(link:string, cookies:object|undefined=undefined) {
    let stream = await load(link, cookies);
    stream.setEncoding("base64");
    return await readMessage(stream);
}

export async function loadHtml(link:string, cookies:object|undefined=undefined) {
    let stream = await load(link, cookies);
    return await readMessage(stream);
}