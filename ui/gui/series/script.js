wSeasonEle = document.getElementById("wSeason");
wEpisodeEle = document.getElementById("wEpisode");
watchInfoEle = document.getElementById("watchInfo");


function back() {
    window.location.href = backLink;
}

async function loadSeries() {
    eel.getSelectedSeries()(function(seriesData){
        headerEle = document.getElementsByTagName("header").item(0);
        nameEle = document.getElementsByTagName("name").item(0);
        seasonEle = document.getElementsByTagName("seasons").item(0);
        descEle = document.getElementsByTagName("desc").item(0);
        headerEle.style.backgroundImage = "url(" + seriesData.image +")";
        headerEle.style.backgroundColor = "gray"; 
        nameEle.innerHTML = seriesData.name;
        seasonEle.innerHTML = seriesData.seasons.length + " Seasons";
        descEle.innerHTML = seriesData.desc ? seriesData.desc : "No description";        
    });
    eel.getBackLink()(function(bLink){backLink = bLink});
    eel.getWatchInfo()(function(watchInfo){
        if (!watchInfo.episode) {
            return 
        }
        wSeasonEle.innerHTML = "Season " + watchInfo.season + "/" + watchInfo.maxSeason;
        wEpisodeEle.innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
        watchInfoEle.style.display = "block";
    });
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

function setSeason(event) {
    newSeason = wSeasonEle.children[0].value;
    eel.setSeason(newSeason)(function(watchInfo){
        btn = event.target;
        wSeasonEle.innerHTML = "Season " + watchInfo.season + "/" + watchInfo.maxSeason;
        btn.setAttribute("onclick","showSetSeason(event)");
        btn.innerHTML = "Edit season";
    });    
}

function showSetEpisode(event) {
    btn = event.target;
    wEpisodeEle.innerHTML = "";
    inputEle = document.createElement("input");
    inputEle.type = "text";
    wEpisodeEle.appendChild(inputEle);
    btn.setAttribute("onclick", "setEpisode(event)");
    btn.innerHTML = "Set Episode";
}

function setEpisode(event) {
    newEpisode = wEpisodeEle.children[0].value;
    eel.setEpisode(newEpisode)(function(watchInfo){
        btn = event.target;
        wEpisodeEle.innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
        btn.setAttribute("onclick","showSetEpisode(event)");
        btn.innerHTML = "Edit Episode";
    });    
}

loadSeries();