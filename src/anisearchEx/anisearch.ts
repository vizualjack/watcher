// @ts-nocheck
import { loadHtml } from "./anisearchLoader";
import { LoadResult } from "./loadResult";
import {parse, NodeType} from 'node-html-parser';
import { Relation } from "./relation";
import { ExtractedSeason } from "./extractedSeason";
import { SearchEntry } from "./searchEntry";
import {logger, logLevel, LogLevel} from '../logger';
import fs from 'fs';

const START_PAGE = "https://www.anisearch.com";
const BASE_LINK = "https://www.anisearch.com/anime/";
const SESSION_KEY = "session_database";
const SET_COOKIE_KEY = "set-cookie";
export class AniSearch {
    sessionKey: string;
    kev: string;

    async init() {
        logger.debug("AniSearch - Initializing...");
        let response = await loadHtml(START_PAGE);
        if(SET_COOKIE_KEY in response.headers) {
            logger.debug("AniSearch - Got cookies");
            for(let cookie of response.headers[SET_COOKIE_KEY]) {
                if(cookie.search(SESSION_KEY) != -1) {
                    this.sessionKey = cookie.split(";")[0].replace(`${SESSION_KEY}=`, "");
                    logger.debug(`AniSearch - Got session key: ${this.sessionKey}`);
                }
            }
        }
        let page = parse(response.message);
        if(logLevel >= LogLevel.DEBUG) fs.writeFileSync("initPage.html", page.outerHTML);
        this.kev = page.querySelector("footer").getAttribute("data-search")?.replace("kev,", "");
        logger.debug(`AniSearch - kev: ${this.kev}`);
    }

    async loadFromLink(link:string) {
        let loadResult = new LoadResult(link);
        let page = await this.#getPage(loadResult.link);
        try {
            // let animeId = link.replace("https://www.anisearch.com/anime/", "").split(",")[0];
            // let subId = animeId.substring(0, animeId.length-3);
            // let imageLink = `https://cdn.anisearch.com/images/anime/cover/${subId}/${animeId}_300.webp`
            // await loadResult.loadImageByLink(imageLink);
            loadResult.name = page.querySelector('#htitle').text;
            loadResult.desc = "";
            let descEle = page.querySelector("div[class='textblock details-text'][lang='en']");
            if (descEle) {
                for(let i = 0; i < descEle.childNodes.length; i++) {
                    let childNode = descEle.childNodes[i];
                    if (childNode.nodeType != NodeType.COMMENT_NODE) {
                        loadResult.desc += childNode.textContent;
                    }
                    // else if(childNode.nodeType == NodeType.ELEMENT_NODE) {
                        // console.log(childNode.innerText);
                        // console.log(childNode.text);
                        // console.log(childNode.textContent);
                        // let element = parse(childNode.rawText);
                        // // console.log(element.tagName);
                        // if ((element.tagName == 'i' && element.classList.contains("hidden")) || element.tagName == 'div') continue;
                        // loadResult.desc += childNode.innerText;
                    // }
                }
            }
            await this.#loadSeasons(loadResult);
            logger.debug(`Anisearch - loadFromLink result: ${JSON.stringify(loadResult)}`);
        } catch (error) {
            logger.error("Exception on extracting infos from: " + loadResult.link);
            logger.error(error);
        }
        return loadResult;
    }

    async search(searchText:string) {
        let searchResult = [];
        let link = `${BASE_LINK}index/?char=all&text=${searchText}&q=true&kev=${this.kev}`;
        let page = await this.#getPage(link);
        if(logLevel >= LogLevel.DEBUG) fs.writeFileSync("searchPageResult.html", page.toString());
        let results_li = this.#entriesAsList(page);
        for(let i = 0; i < results_li.length; i++) {
            let entry = results_li[i];
            let linkElement = entry.querySelector("a");
            let name = this.#getNameFromLinkElement(linkElement);
            let imageLink = this.#getImageLinkFromLinkElement(linkElement);
            let link = this.#getLinkFromLinkElement(linkElement);
            let newEntry = new SearchEntry(name, imageLink, link);
            await newEntry.loadImage();
            searchResult.push(newEntry);
        }
        return searchResult;
    }

    #getNameFromLinkElement(linkElement:HTMLElement) {
        return linkElement.getAttribute("data-title")?.replace("Anime: ", "");
    }

    #getImageLinkFromLinkElement(linkElement:HTMLElement) {
        return linkElement.getAttribute("data-bg");
    }

    #getLinkFromLinkElement(linkElement:HTMLElement) {
        return linkElement.getAttribute("href")?.replace("anime/", "https://www.anisearch.com/anime/");
    }

    #entriesAsList(page:HTMLElement) {        
        return page.querySelectorAll("ul[class*='covers'] > li");
    }

    async #getPage(link) {
        let cookies = {};
        cookies[SESSION_KEY] = this.sessionKey;
        cookies["kev"] = this.kev;
        let response = await loadHtml(link, cookies);
        return parse(response.message);
    }

    #getAllSeasonPaths(relations: Relation[]) {
        let listOfSeasonLists = this.#getAllStarters(relations);
        if(relations.length <= 1) return listOfSeasonLists;
        this.#fillAllLists(listOfSeasonLists, relations);
        return listOfSeasonLists;
    }

    #fillAllLists(listOfSeasonLists: [ExtractedSeason[]], relations: Relation[]) {
        for(let seasonLists of listOfSeasonLists) {
            while(true) {
                let currentSeason = seasonLists[seasonLists.length - 1];
                let foundSeason = false;
                for(let relation of relations) {
                    if(currentSeason.name == relation.frm.name) {
                        seasonLists.push(relation.to);
                        foundSeason = true;
                        break;
                    }
                }
                if(!foundSeason) break;
            }
        }
        logger.debug(`Anisearch - fillAllLists: ${JSON.stringify(listOfSeasonLists)}`);
    }

    #getAllStarters(relations: Relation[]): [ExtractedSeason[]] {
        let list = [];
         for(let i = 0; i < relations.length; i++) {
            let startRelation = relations[i];
            let isStart = true;
            let startSeason = startRelation.frm;
            for(let i = 0; i < relations.length; i++) {
                let relation = relations[i];
                if(startRelation == relation) continue;
                if(startSeason.name == relation.to.name) {
                    isStart = false;
                    break;
                }
            }
            if (isStart) list.push([startSeason]);
        }
        logger.debug(`Anisearch - getAllStarters: ${JSON.stringify(list)}`);
        return list;
    }

    #getLongestSeasonPath(seasonLists: [ExtractedSeason[]]) {
        let longestPath;
        for(let seasonList of seasonLists) {
            if(longestPath == undefined || seasonList.length > longestPath.length) longestPath = seasonList;
        }
        return longestPath;
    }

    #trimSeasonPaths(seasonPaths:[ExtractedSeason[]]) {
        for(let seasonPath of seasonPaths) {
            for(let i = seasonPath.length-1; i >= 0; i--) {
                let currentSeason = seasonPath[i];
                if(currentSeason.episodes == -1) {
                    seasonPath.splice(i,1);
                    logger.debug(`Spliced season path: ${JSON.stringify(seasonPath)}`);
                }
            }
        }
    }

    async #loadSeasons(loadResult:LoadResult) {
        let dataGraph = await this.#getDataGraph(`${loadResult.link}/relations`);
        logger.debug(`Datagraph: ${JSON.stringify(dataGraph)}`);
        let relations = this.#getSequelRelations(dataGraph);
        logger.debug(`Relations: ${JSON.stringify(relations)}`);
        let allSeasonPaths = this.#getAllSeasonPaths(relations);
        logger.debug(`All relation paths: ${allSeasonPaths.length}`);
        this.#trimSeasonPaths(allSeasonPaths);
        loadResult.extractedSeasons = this.#getLongestSeasonPath(allSeasonPaths);
    }

    async #getDataGraph(link:string) {
        let page = await this.#getPage(link);
        let flowChart = page.getElementById("flowchart");
        if (!flowChart) return null;
        let dataGraphStr = flowChart.attributes["data-graph"];
        return JSON.parse(dataGraphStr);
    }

    #getSequelRelations(dataGraph:any) {
        let sequelRelationId = this.#getSequelRelationId(dataGraph);
        let animeDict = dataGraph["nodes"]["anime"];
        logger.debug(`animeDict: ${JSON.stringify(animeDict)}`);
        let relations = [];
        let edges = dataGraph["edges"];
        logger.debug(`edges: ${JSON.stringify(edges)}`);
        if (edges.length == 0) {
            relations.push(new Relation(this.#extractSeason(animeDict[dataGraph["id"]]["title"])));
        }
        for(let i = 0; i < edges.length; i++) {
            let edge = edges[i];
            if(edge["relation"] != sequelRelationId) continue;
            let frm = this.#extractSeason(animeDict[edge["from"]]["title"]);
            let to = this.#extractSeason(animeDict[edge["to"]]["title"]);
            relations.push(new Relation(frm, to));
        }
        if (relations.length == 0) {
            relations.push(new Relation(this.#extractSeason(animeDict[dataGraph["id"]]["title"])));
        }
        return relations;
    }

    #getSequelRelationId(dataGraph:any) {
        let legend = dataGraph["legend"]
        for(let i = 0; i < legend.length; i++) {
            let name = legend[i];
            if(name == "Sequel") {
                return i;
            }
        }
        return -1;
    }

    #extractSeason(titleString:string) {
        let splitted = titleString.split("<span>");
        let name = splitted[0];
        let episodesAndGenre = splitted[1];
        let episodes = episodesAndGenre.split(", ")[1].split(" ")[0].trim();
        let genre = episodesAndGenre.split(")")[1].replace("<\/span>","").replace(",", "").trim();
        if (episodes == "?" || genre == "?") episodes = -1;
        return new ExtractedSeason(episodes, name);
    }
}