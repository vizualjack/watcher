// @ts-nocheck
import { loadHtml } from "./anisearchLoader";
import { LoadResult } from "./loadResult";
import {parse, NodeType} from 'node-html-parser';
import { Relation } from "./relation";
import { ExtractedSeason } from "./extractedSeason";
import { SearchEntry } from "./searchEntry";


const BASE_LINK = "https://www.anisearch.com/anime/";
export class AniSearch {
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
        } catch (error) {
            console.log("Exception on extracting infos from: " + loadResult.link);
            console.log(error);
        }
        return loadResult;
    }

    async search(searchText:string) {
        let searchResult = [];
        let page = await this.#getPage(`${BASE_LINK}index?text=${searchText}`);
        let results_li = this.#entriesAsList(page);
        for(let i = 0; i < results_li.length; i++) {
            let result_li = results_li[i];
            let linkElement = result_li.querySelector("a");
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
        return linkElement.getAttribute("title")?.replace("Anime: ", "");
    }

    #getImageLinkFromLinkElement(linkElement:HTMLElement) {
        return linkElement.getAttribute("data-bg");
    }

    #getLinkFromLinkElement(linkElement:HTMLElement) {
        return linkElement.getAttribute("href")?.replace("anime/", "https://www.anisearch.com/anime/");
    }

    #entriesAsList(page:HTMLElement) {        
        return page.querySelectorAll("ul[class='covers gallery'] > li");
    }

    async #getPage(link) {
        let htmlPage = await loadHtml(link);
        return parse(htmlPage);
    }

    async #loadSeasons(loadResult:LoadResult) {
        let dataGraph = await this.#getDataGraph(`${loadResult.link}/relations`);
        let relations = this.#getSequelRelations(dataGraph);
        // console.log(relations);
        let extractedSeasons = loadResult.extractedSeasons;
        // FIND AND PUSH START SEASON
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
            if (isStart) {
                extractedSeasons.push(startSeason);
                break
            }
        }
        // LOAD REST OF THE SEASONS FROM THE START
        while(true) {
            let lastSeason = extractedSeasons[extractedSeasons.length-1];
            let nextSeason = null;
            for(let i = 0; i < relations.length; i++) {
                let relation = relations[i];
                if (relation.frm.name == lastSeason.name) nextSeason = relation.to;
            }
            if(nextSeason == null) break;
            extractedSeasons.push(nextSeason);
        }
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
        let relations = [];
        let edges = dataGraph["edges"];
        for(let i = 0; i < edges.length; i++) {
            let edge = edges[i];
            if(edge["relation"] != sequelRelationId) continue;
            let frm = this.#extractSeason(animeDict[edge["from"]]["title"]);
            let to = this.#extractSeason(animeDict[edge["to"]]["title"]);
            relations.push(new Relation(frm, to));
        }
        return relations;
    }

    #getSequelRelationId(dataGraph:any) {
        let sequelId = -1;
        let legend = dataGraph["legend"]
        for(let i = 0; i < legend.length; i++) {
            sequelId += 1;
            let name = legend[i];
            if(name == "Sequel") {
                break
            }
        }
        return sequelId;
    }

    #extractSeason(titleString:string) {
        let splitted = titleString.split("<span>");
        let name = splitted[0];
        let episodes = splitted[1].split(", ")[1].split(" ")[0];
        if (episodes == "?") episodes = -1;
        return new ExtractedSeason(episodes, name);
    }
}