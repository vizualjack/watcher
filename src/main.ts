// @ts-nocheck
// Modules to control application life and create native browser window
import { BrowserWindow, Menu, MenuItem, app, dialog, ipcMain } from 'electron';
import path from 'path';
import fs from 'fs';
import { Persister } from './data/persister';
import { Library } from './data/library';
import { User } from './data/tracking/user';
import { Series } from './data/series';
import { SearchEntry } from './anisearchEx/searchEntry';
import { AniSearch } from './anisearchEx/anisearch';
import {exec} from 'child_process';
// import {Persister} from 'persiter';


// APP SETTINGS
const windowSizePath = "./lastWindow";
const persPath = "./persPath";
///////////////
// var persister = Persister.getInstance("./");
// console.log("by main");
// let wi = new WatchInfo(new Series("asd"));
// wi.getEpisode();
// console.log("wi");
var mainWindow: BrowserWindow;
var persister: Persister;
var library:Library;
var user:User;
loadData();

function loadData() {
  persister = new Persister(getSaveDir());
  persister.load();
  library = persister.library;
  user = persister.user;
}

function getSaveDir() {  
  if (!fs.existsSync(persPath)) return "";
  return fs.readFileSync(persPath).toString();
}

function setSaveDir(newSaveDir:string) {
  fs.writeFileSync(persPath, newSaveDir);
}

function saveWindowSettings(mainWindow:BrowserWindow) {
  var winSettings = {
    "width": mainWindow.getSize()[0],
    "height": mainWindow.getSize()[1],
    "x": mainWindow.getPosition()[0],
    "y": mainWindow.getPosition()[1],
  };
  fs.writeFileSync(windowSizePath, JSON.stringify(winSettings));
}

function createWindow() {
  var width = 800
  var height = 600
  var x = undefined
  var y = undefined
  if (fs.existsSync(windowSizePath)) {
    var winSettings = JSON.parse(fs.readFileSync(windowSizePath).toString());
    width = winSettings["width"];
    height = winSettings["height"];
    x = winSettings["x"];
    y = winSettings["y"];
  }
  
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: width,
    height: height,
    x: x,
    y: y,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../icon.ico')
  })

  mainWindow.on('close', () => {
      saveWindowSettings(mainWindow);
      persister.save();
  })

  // and load the index.html of the app.
  mainWindow.loadFile('src/pages/list/page.html');
  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

const menu = new Menu();
menu.append(new MenuItem({
  label: 'Change save location',
  click: async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openDirectory']
    })
    if (result.filePaths.length == 0) {
      console.log("No folder seleted");
      return;
    }
    let filePath = path.join(result.filePaths[0], "fileHere").replace("fileHere", "");
    setSaveDir(filePath);
    loadData();
    mainWindow.reload();
  }
}))
Menu.setApplicationMenu(menu);

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(async () => {
  createWindow();
  await anisearch.init();
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
});


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.


/////////////  ACTUAL APP FUNCS
const LB_LIST = "list";
const LB_SEARCH = "search";
var loadBase = "";
var selectedSeries: Series;
var seriesList:Series[] = [];
var searchResult:SearchEntry[] = [];
var anisearch: AniSearch = new AniSearch();

function getActionText() {
  if (loadBase == LB_SEARCH) return "Add to library";
  else if (loadBase == LB_LIST) {
    let watchInfo = user.getWatchInfoForSeries(selectedSeries);
    if (watchInfo != null) return "Remove from watch list";
    else return "Add to watch list";
  }
}

function getSearchResult() {
  let searchSeriesList = [];
  for(let i = 0; i < searchResult.length; i++) {
    let searchEntry = searchResult[i];
    let searchSeries = new Series(-1,searchEntry.name);
    searchSeries.name = searchEntry.name;
    searchSeries.image = searchEntry.image;
    searchSeriesList.push(searchSeries);
  }
  return searchSeriesList;
}

function getFullWatchInfo() {
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if(!watchInfo) return null;
  let fullWatchInfo = {};
  fullWatchInfo["seasonName"] = watchInfo.getSeasonName();
  fullWatchInfo["season"] = watchInfo.getSeason();
  fullWatchInfo["maxSeason"] = watchInfo.getSeriesSeasons();
  fullWatchInfo["episode"] = watchInfo.getEpisode();
  fullWatchInfo["maxEpisode"] = watchInfo.getSeasonEpisodes();
  if (watchInfo.watchLocationIsWebLink()) fullWatchInfo["watchLocation"] = watchInfo.watchLocation;
  return fullWatchInfo;
}

function getFullSeriesInfos(seriesList:Series[]) {
  let fullSeriesInfos = [];
  for(let i = 0; i < seriesList.length; i++) {
    let fullSeriesInfo = {};
    let series = seriesList[i];
    fullSeriesInfo["name"] = series.name;
    fullSeriesInfo["image"] = series.image;
    fullSeriesInfo["desc"] = series.desc;
    fullSeriesInfo["link"] = series.link;
    fullSeriesInfo["seasons"] = series.seasons;
    let watchStatus = 0;
    let watchInfo = user.getWatchInfoForSeries(series);
    if(watchInfo) {
      watchStatus = 1;
      if(!watchInfo.unseenEpisodes()) watchStatus = 2;
    }
    fullSeriesInfo["watchStatus"] = watchStatus;
    fullSeriesInfos.push(fullSeriesInfo);
  }
  return fullSeriesInfos;
}

// API Methods
ipcMain.handle("action", () => {
  if (loadBase == LB_SEARCH) {
    library.addSeries(selectedSeries);
    loadBase = LB_LIST;
  }
  else if (loadBase == LB_LIST) {
    let watchInfo = user.getWatchInfoForSeries(selectedSeries);
    if (watchInfo != null) {
      user.removeSeries(selectedSeries);
    }
    else {
      user.addSeries(selectedSeries);
    }
  }
  return getActionText();
});

ipcMain.handle("getSeries", (event, listName) => {
  seriesList = [];
  if (listName == "watchList") {
    for (let i = 0; i < user.watchInfos.length; i++) {
      seriesList.push(user.watchInfos[i].series);
    }
  }
  else {
    for (let i = 0; i < library.series.length; i++) {
      seriesList.push(library.series[i]);
    }
  }
  return getFullSeriesInfos(seriesList);
});

ipcMain.handle("getSelectedSeries", (event) => {
  return selectedSeries;
});

ipcMain.handle("selectSeries", (event, index) => {
  selectedSeries = seriesList[index]
  loadBase = LB_LIST
});

ipcMain.handle("getWatchInfo", () => {
  return getFullWatchInfo();
});

ipcMain.handle("setSeason", (event, newSeason) => {
  newSeason = parseInt(newSeason);
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if (watchInfo == null) return;
  watchInfo.season = newSeason;
  watchInfo.episode = 1;
  return getFullWatchInfo();
});

ipcMain.handle("setEpisode", (event, newEpisode) => {
  newEpisode = parseInt(newEpisode);
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if (watchInfo == null) return;
  watchInfo.episode = newEpisode;
  return getFullWatchInfo();
});

ipcMain.handle("setWatchLocation", (event, newWatchLoc) => {
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if (watchInfo == null) return;
  watchInfo.watchLocation = newWatchLoc;
  return getFullWatchInfo();
});

ipcMain.handle("getActionText", () => {
  return getActionText();
});

ipcMain.handle("nextEpisode", () => {
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if (watchInfo == null) return;
  watchInfo.nextEpisode();
  return getFullWatchInfo();
});

ipcMain.handle("openWatchPage", async () => {
  let watchInfo = user.getWatchInfoForSeries(selectedSeries);
  if (watchInfo == null) return;
  let link = watchInfo.watchLocation;
  if(process.platform == "linux") exec(`firefox ${link}`);  // if firefox is used (standard browser on ubuntu)
  else exec(`start ${link}`);   // as far as i tested only worked for windows
});

ipcMain.handle("getBackLink", () => {
  return "../" + loadBase + "/page.html";
});

ipcMain.handle("searchSeries", async (event, searchText) => {
  searchResult = await anisearch.search(searchText);
  console.log("Num of results: " + searchResult.length);
  return getSearchResult();
});

ipcMain.handle("loadSeries", async (event, index) => {
  let searchEntry = searchResult[index];
  let addInfo = await anisearch.loadFromLink(searchEntry.link);
  let newSeries = new Series(-1,searchEntry.name);
  newSeries.image = searchEntry.image;
  newSeries.desc = addInfo.desc;
  newSeries.link = searchEntry.link;
  for (let i = 0; i < addInfo.extractedSeasons.length; i++) {
    let exSeason = addInfo.extractedSeasons[i];
    newSeries.addSeason(exSeason.episodes, exSeason.name);
  }
  selectedSeries = newSeries;
  loadBase = LB_SEARCH
});

ipcMain.handle("getSearchResult", () => {
  return getSearchResult();
});