// @ts-nocheck

document.getElementById("sendBtn").addEventListener('click', async () => {
    console.log("sending...");
    console.log(await window.backend.test(document.getElementById("data").value));
});
console.log("loaded");