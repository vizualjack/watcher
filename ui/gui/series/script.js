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
        document.getElementById("wSeason").innerHTML = "Season " + watchInfo.season + "/" + watchInfo.maxSeason;
        document.getElementById("wEpisode").innerHTML = "Episode " + watchInfo.episode + "/" + watchInfo.maxEpisode;
        document.getElementById("watchInfo").style.display = "block";
        
    //   <span id="wSeason">Season 1/2</span>
    //   <span id="wEpisode">Episode 1/2</span>
    });
}
loadSeries();