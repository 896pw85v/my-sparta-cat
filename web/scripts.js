const releasesDiv = document.getElementById('releases-div');
const burl = 'http://localhost:8000'
document.getElementById('form').addEventListener('submit', (e) => {
    e.preventDefault()
    // formdata pack the form, then put it into json
    const fd = new FormData(e.target)
    const myjson = Object.fromEntries(fd)
    // console.log(typeof myjson)
    // console.log(myjson)
    fetch(burl, {
        method: 'POST', 
        body: JSON.stringify(myjson),
        headers: {
            "Content-Type": "application/json"
        },})
    .then(res => res.json())
    .then(res => loadReleases(res))
    .catch((error) => (console.log(error)))
})
// TODO: return correct release name
let out = {}
function loadReleases(j) {
    console.log(typeof j)

    out = j
    console.log(j[0]['images'])
    releasesDiv.innerHTML = ""
    for (let release of j) {        
        const thumbnails = release['images'][0]['thumbnails'];
        const tn = 'large' in Object.keys(thumbnails) ? thumbnails['large'] : thumbnails['500'];
        const releaseUrl = release['release']
        const title = release['title']
        const card = `
        <div class="release-card">
            <img src="${tn} alt="Album front image" >
            <a href="${releaseUrl}" target="./blank">Link to Music Brainz</a>
            <p>${title}</p>
        </div>`; // <a>
        releasesDiv.innerHTML += card;
    }
}


/*
res : Song1 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song2 >  - images -> [ {...: ...} ] (idk why but only one dict)
              |- releases
      Song3...
                            {'thumbnails: 
                                'size': url, 
                                ...
                            }
*/

const sign = document.getElementById('sign');
sign.addEventListener('submit', (e) => {
    e.preventDefault()
    // console.log(e.target)
    const fd = new FormData(e.target)
    const myjson = Object.fromEntries(fd)
    console.log(myjson)
    fetch(burl + '/log-in', {
        method: "POST", 
        headers: {
            'Content-Type': 'application/json',

        },
        body: JSON.stringify(myjson)
    }).then(res => res.json())
    .then(data => {
        console.log(data)
        console.log(typeof data)
    })
})