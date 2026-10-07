const form = document.getElementById('review-form');
window.addEventListener("error", (event) => {
    // console.log(event)
    if (event.message === "Uncaught Error: Can't get id for the song to write review. ") {
        console.log("this is my eorr")
        alert("Status shows that there is no song selected to rate. Maybe you shouldn't be on this page. Redirecting you to the previous page. ")
        window.history.length === 1 ? window.close() : window.history.back() 
    }
})
form.addEventListener('submit', (e) => {
    e.preventDefault()
    // NOTE: formdata is all string
    const fd = new FormData(e.target); // rating and content
    const obj = Object.fromEntries(fd);
    obj.mbid = sessionStorage.getItem('songId');
    obj.rating = Number(obj.rating)
    localStorage.setItem("lastSongRated", JSON.stringify(obj));
    console.log('song review package: ', obj)
    fetch('/write', {
        method: 'POST', 
        body: JSON.stringify(obj), 
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        if (data === true) {
            alert("Submitted. ");
            history.back();
        }
        else {
            alert("Submit failed. Please try again later. ")
        }
    })
})
const content = document.getElementById("content");
content.addEventListener("input", () => {
    content.style.height = "auto";        // reset
    content.style.height = content.scrollHeight + "px"; // grow
  });

//   TODO: this is an duplicate of btool; try to get rid of it
function mkRow(item) {
    console.log('making card', item['title'])
    console.log(item.images.length);
    const id = item.id;
    const ima = item.images;
    const thumbUrl =
        ima[0].thumbnails?.small ||
        ima[0].thumbnails?.large ||
        "";
    console.log('url', thumbUrl)
    const row = document.createElement("div");
    // alternative: make div <a> so it's a link to a new page
    row.id = id;
    row.className = "song-row";

    row.innerHTML = `
            <img class="song-thumb" src="${thumbUrl}" alt="${item.title}">
            <div class="song-info">
                <p class="song-title">${item.title}</p>
                <p class="song-artist">${item["artist-credit-phrase"]}</p>
            </div>
        `;
    // sessionStorage.setItem(id, JSON.stringify(item))
    return row
}

const rowDiv = document.getElementById('reviewSongRow')
window.onload = (event) => {
    // prompt("loaded");
    const id = sessionStorage.getItem('songId')
    if (id === null) {
        // this check would probably never be true since I ensured on 
        // the last page that un-logged-in users cannot access this page
        alert("Status shows that there is no song selected to rate. Maybe you shouldn't be on this page. Redirecting you to the previous page. ")
        window.history.back() 
        throw new Error("Can't get id for the song to write review. ")
    }
    const song = JSON.parse(sessionStorage.getItem(id))
    rowDiv.appendChild(mkRow(song))
};

