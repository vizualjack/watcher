function back() {
    window.location.href = '/list/page.html';
}

seriesTemplate = document.getElementsByTagName("series").item(0);
seriesHolder = document.getElementsByTagName("seriesHolder").item(0);
searchText = document.getElementById("searchText");
loadAnim = document.getElementById("loadAnim");
totalMargin = parseInt(window.getComputedStyle(seriesTemplate).margin.replace("px","") * 2);
seriesWidth = seriesTemplate.clientWidth + totalMargin;
seriesHolderPad = parseInt(window.getComputedStyle(seriesHolder).padding.replace("px","") * 2);
seriesTemplate.style.display = "none";

function clearResult() {
    while(seriesHolder.children.length > 1) {
        seriesHolder.children[1].remove();
    }
}

function showResult(seriesData) {
    seriesData.forEach((val, index) => {
        seriesEle = seriesTemplate.cloneNode(true);
        seriesEle.id = index;
        seriesEle.children[0].innerHTML = val.name;
        seriesEle.addEventListener('click', async () => {
            eel.loadSeries(index)(function(){
                window.location.href = '/series/page.html';
            });                
        });
        seriesEle.style.display = "inline-block";
        seriesEle.style.backgroundImage = "url(" + val.image + ")";
        seriesHolder.appendChild(seriesEle);
    });
    adjustSeriesHolderWidth();
}

function adjustSeriesHolderWidth() {
    totalWidth = document.body.clientWidth - seriesHolderPad;
    newSeriesHolderWidth = totalWidth / seriesWidth;
    newSeriesHolderWidth = Math.floor(newSeriesHolderWidth);
    newSeriesHolderWidth = Math.min(seriesHolder.childElementCount-1, newSeriesHolderWidth);
    newSeriesHolderWidth *= seriesWidth;    
    seriesHolder.style.width = newSeriesHolderWidth + "px";
}

async function search() {
    clearResult()
    showLoadAnimation();
    eel.searchSeries(searchText.value)(function(seriesData){
        showResult(seriesData);
        hideLoadAnimation();
    });
}

function showLoadAnimation() {
    loadAnim.style.display = "block";
}

function hideLoadAnimation() {
    loadAnim.style.display = "none";
}

function checkForSearchTrigger(event) {
    if(event.keyCode == 13) {
        search();
    }
}

eel.getSearchResult()(function(seriesData){
    showResult(seriesData);
});