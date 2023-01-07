function back() {
    window.location.href = '/list/page.html';
}

seriesTemplate = document.getElementsByTagName("series").item(0);
seriesHolder = document.getElementsByTagName("seriesHolder").item(0);
searchText = document.getElementById("searchText");


function showResult(seriesData) {
    while(seriesHolder.children.length > 1) {
        seriesHolder.children[1].remove();
    }
    seriesData.forEach((val, index) => {
        seriesEle = seriesTemplate.cloneNode(true);
        seriesEle.id = index;
        seriesEle.children[0].innerHTML = val.name;
        seriesEle.addEventListener('click', async () => {
            eel.loadSeries(index)(function(){
                window.location.href = '/series/page.html';
            });                
        });
        seriesEle.style.display = "block";
        seriesEle.style.backgroundImage = "url(" + val.image + ")";
        seriesHolder.appendChild(seriesEle);
    });
}


async function search() {
    eel.searchSeries(searchText.value)(function(seriesData){
        showResult(seriesData);
    });    
}

eel.getSearchResult()(function(seriesData){
    showResult(seriesData);
});