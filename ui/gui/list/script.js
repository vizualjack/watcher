async function loadSeries() {
    while(seriesHolder.children.length > 1) {
        seriesHolder.children[1].remove();
    }
    eel.getSeries(listSelector.value)(function(seriesData){
        seriesData.forEach((val, index) => {
            seriesEle = seriesTemplate.cloneNode(true);
            seriesEle.id = index;
            seriesEle.children[0].innerHTML = val.name;
            seriesEle.addEventListener('click', async () => {
                eel.selectSeries(index)(function(){
                    window.location.href = '/series/page.html';
                });                
            });
            seriesEle.style.display = "block";
            seriesEle.style.backgroundImage = "url(" + val.image + ")";
            seriesHolder.appendChild(seriesEle);
        });
    });
}

function newAnime() {
    window.location.href = '/search/page.html';
}

seriesTemplate = document.getElementsByTagName("series").item(0);
seriesHolder = document.getElementsByTagName("seriesHolder").item(0);
listSelector = document.getElementById("list");
loadSeries();