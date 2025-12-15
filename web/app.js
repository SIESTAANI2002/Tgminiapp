const tg=window.Telegram.WebApp;tg.expand();
const p=new URLSearchParams(window.location.search);
document.getElementById("animeTitle").innerText=p.get("title")||"Anime Episode";
document.getElementById("ep").innerText="EP "+(p.get("ep")||"?");
document.getElementById("quality").innerText=p.get("q")||"720p";
const fileId=p.get("file");
if(fileId){document.getElementById("player").src=`https://drive.google.com/file/d/${fileId}/preview`;}