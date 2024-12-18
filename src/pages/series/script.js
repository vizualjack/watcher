wSeasonNameEle = document.getElementById("wSeasonName");
wSeasonEle = document.getElementById("wSeason");
wEpisodeEle = document.getElementById("wEpisode");
watchInfoEle = document.getElementById("watchInfo");
actionEle = document.getElementById("action");
openWpEle = document.getElementById("openWatchPage");


function back() {
    window.location.href = backLink;
}

async function action() {
    let newBtnText = await window.backend.action();
    actionEle.innerHTML = newBtnText;
    loadWatchInfo();
}

function showWatchInfo(watchInfo) {
    if (!watchInfo) {
        watchInfoEle.style.display = "none";
        return 
    }
    wSeasonNameEle.innerHTML = "Season name: <br>" + watchInfo.seasonName;
    wSeasonEle.innerHTML = "Season " + watchInfo.season + "/" + watchInfo.maxSeason;
    wEpisodeEle.innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
    openWpEle.style.display = watchInfo.watchLocation ? "inherit" : "none";
    watchInfoEle.style.display = "grid";
}

async function loadWatchInfo() {
    let watchInfo = await window.backend.getWatchInfo();
    showWatchInfo(watchInfo);
}

async function init() {
    // LOAD SERIES DATA 
    let seriesData = await window.backend.getSelectedSeries();
    headerEle = document.getElementsByTagName("header").item(0);
    nameEle = document.getElementsByTagName("name").item(0);
    seasonEle = document.getElementsByTagName("seasons").item(0);
    descEle = document.getElementsByTagName("desc").item(0);
    headerEle.style.backgroundImage = "url(" + seriesData.image +")";
    headerEle.style.backgroundColor = "gray"; 
    nameEle.innerHTML = seriesData.name;
    seasonEle.innerHTML = seriesData.seasons.length + " Seasons";
    descEle.innerHTML = seriesData.desc ? seriesData.desc : "No description";
    // LOAD BACK LINK AND ACTION TEXT
    backLink = await window.backend.getBackLink();
    await loadWatchInfo();
    let newBtnText = await window.backend.getActionText();
    actionEle.innerHTML = newBtnText;
    actionEle.style.display = "block";
}

function showSetSeason(event) {
    btn = event.target;
    wSeasonEle.innerHTML = "";
    inputEle = document.createElement("input");
    inputEle.type = "text";
    wSeasonEle.appendChild(inputEle);
    btn.setAttribute("onclick", "setSeason(event)");
    btn.innerHTML = "Set season";
}

async function setSeason(event) {
    newSeason = wSeasonEle.children[0].value;
    let watchInfo = await window.backend.setSeason(newSeason);
    let btn = event.target;
    btn = event.target;
    wSeasonEle.innerHTML = "Season " + watchInfo.season + "/" + watchInfo.maxSeason;
    if (wEpisodeEle.children.length == 0) {
        wEpisodeEle.innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
    }
    btn.setAttribute("onclick","showSetSeason(event)");
    btn.innerHTML = "Edit season";
}

function showSetEpisode(event) {
    btn = event.target;
    wEpisodeEle.innerHTML = "";
    inputEle = document.createElement("input");
    inputEle.type = "text";
    wEpisodeEle.appendChild(inputEle);
    btn.setAttribute("onclick", "setEpisode(event)");
    btn.innerHTML = "Set episode";
}

async function setEpisode(event) {
    newEpisode = wEpisodeEle.children[0].value;
    let watchInfo = await window.backend.setEpisode(newEpisode);
    btn = event.target;
    wEpisodeEle.innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
    btn.setAttribute("onclick","showSetEpisode(event)");
    btn.innerHTML = "Edit episode";
}

function showSetWatchLocation(event) {
    btn = event.target;
    openWpEle.innerHTML = "";
    inputEle = document.createElement("input");
    inputEle.type = "text";
    openWpEle.appendChild(inputEle);
    openWpEle.style.display = "inherit";
    openWpEle.style.backgroundColor = "transparent";
    openWpEle.style.borderColor = "transparent";
    btn.setAttribute("onclick", "setWatchLocation(event)");
    openWpEle.setAttribute("onclick", "");
    btn.innerHTML = "Set watch page";
}

async function setWatchLocation(event) {
    newLink = openWpEle.children[0].value;
    let watchInfo = await window.backend.setWatchLocation(newLink);
    btn = event.target;
    btn.setAttribute("onclick","showSetWatchLocation(event)");
    openWpEle.setAttribute("onclick", "openWatchPage()");
    openWpEle.innerHTML = "Open watch page";
    openWpEle.style.display = watchInfo.watchLocation ? "inherit" : "none";
    openWpEle.style.backgroundColor = "";
    openWpEle.style.borderColor = "";
    btn.innerHTML = "Edit watch page";
}

async function nextEpisode() {
    let watchInfo = await window.backend.nextEpisode();
    showWatchInfo(watchInfo);
}

function openWatchPage() {
    window.backend.openWatchPage();
}

init();