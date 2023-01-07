seriesTemplate = document.getElementsByTagName("series").item(0);
seriesHolder = document.getElementsByTagName("seriesHolder").item(0);
async function loadSeries() {
    eel.getSeries()(function(seriesData){
        seriesData.forEach((val, index) => {
            seriesEle = seriesTemplate.cloneNode(true);
            seriesEle.id = index;
            seriesEle.children[0].innerHTML = val.name;
            seriesEle.addEventListener('click', async () => {
                eel.selectSeries(index);
                window.location.href = '/series/page.html';
            });
            seriesEle.style.display = "block";
            seriesEle.style.backgroundImage = "URL('../data/" + index + ".webp')";
            seriesHolder.appendChild(seriesEle);
        });
    });    
}

function newAnime() {
    window.location.href = '/search/page.html';
}

loadSeries();