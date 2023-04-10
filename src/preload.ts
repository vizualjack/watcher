import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld("backend", {
  action: () => ipcRenderer.invoke("action"),
  getSeries: (listName:any) => ipcRenderer.invoke("getSeries", listName),
  selectSeries: (index:any) => ipcRenderer.invoke("selectSeries", index),
  getWatchInfo: () => ipcRenderer.invoke("getWatchInfo"),
  setSeason: (newSeason:any) => ipcRenderer.invoke("setSeason", newSeason),
  setEpisode: (newEpisode:any) => ipcRenderer.invoke("setEpisode", newEpisode),
  setWatchLocation: (newWatchLoc:any) => ipcRenderer.invoke("setWatchLocation", newWatchLoc),
  getActionText: () => ipcRenderer.invoke("getActionText"),
  nextEpisode: () => ipcRenderer.invoke("nextEpisode"),
  openWatchPage: () => ipcRenderer.invoke("openWatchPage"),
  getBackLink: () => ipcRenderer.invoke("getBackLink"),
  searchSeries: (searchText:any) => ipcRenderer.invoke("searchSeries", searchText),
  loadSeries: (index:any) => ipcRenderer.invoke("loadSeries", index),
  getSearchResult: () => ipcRenderer.invoke("getSearchResult"),
  getSelectedSeries: () => ipcRenderer.invoke("getSelectedSeries"),
})


// window.addEventListener('DOMContentLoaded', () => {
//   const replaceText = (selector:any, text:any) => {
//     const element = document.getElementById(selector);
//     if (element) element.innerText = text;
//   }

//   for (const type of ['chrome', 'node', 'electron']) {
//     replaceText(`${type}-version`, process.versions[type])
//   }
// })