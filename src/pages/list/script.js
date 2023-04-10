WS_ATT_NAME = "data:watchstatus";

async function loadSeries() {
    while(seriesHolder.children.length > 1) {
        seriesHolder.children[1].remove();
    }    
    let seriesData = await window.backend.getSeries(listSelector.value);
    seriesData.forEach((val, index) => {
        seriesEle = seriesTemplate.cloneNode(true);
        seriesEle.id = index;
        seriesEle.setAttribute(WS_ATT_NAME, val.watchStatus);
        seriesEle.children[0].innerHTML = val.name;
        seriesEle.addEventListener('click', async () => {
            await window.backend.selectSeries(index);
            window.location.href = '../series/page.html';
        });
        seriesEle.style.display = "inline-block";
        seriesEle.style.backgroundImage = "url(" + val.image + ")";
        seriesHolder.appendChild(seriesEle);
    });
    adjustSeriesHolderWidth();
}

function newAnime() {
    window.location.href = '../search/page.html';
}

function changeCheckBox() {
    checkBoxLabel.innerHTML = listSelector.value == "watchList" ? "Hide finished" : "Hide already in watch list";
    checkBox.checked = false;
}

function onListChange() {
    loadSeries();
    changeCheckBox();
}

function onCheckBoxClicked() {
    displayValue = checkBox.checked ? "none" : "inline-block";
    for(let i = 1; i < seriesHolder.children.length; i++) {
        seriesEle = seriesHolder.children[i];
        if (listSelector.value == "library" && 
            seriesEle.getAttribute(WS_ATT_NAME) != 0) {
            seriesEle.style.display = displayValue;
        }
        else if (listSelector.value == "watchList" && 
        seriesEle.getAttribute(WS_ATT_NAME) == 2) {
            seriesEle.style.display = displayValue;
        }
    }
}

function adjustSeriesHolderWidth() {
    totalWidth = document.body.clientWidth - seriesHolderPad;
    newSeriesHolderWidth = totalWidth / seriesWidth;
    newSeriesHolderWidth = Math.floor(newSeriesHolderWidth);
    newSeriesHolderWidth = Math.min(seriesHolder.childElementCount-1, newSeriesHolderWidth);
    newSeriesHolderWidth *= seriesWidth;    
    seriesHolder.style.width = newSeriesHolderWidth + "px";
}

seriesTemplate = document.getElementsByTagName("series").item(0);
seriesHolder = document.getElementsByTagName("seriesHolder").item(0);
listSelector = document.getElementById("list");
checkBox = document.getElementById("checkbox");
checkBoxLabel = document.getElementById("checkboxLabel");
totalMargin = parseInt(window.getComputedStyle(seriesTemplate).margin.replace("px","") * 2);
seriesWidth = seriesTemplate.clientWidth + totalMargin;
seriesHolderPad = parseInt(window.getComputedStyle(seriesHolder).padding.replace("px","") * 2);
seriesTemplate.style.display = "none";

loadSeries();