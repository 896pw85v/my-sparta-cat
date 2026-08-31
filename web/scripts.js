const releasesDiv = document.getElementById('releases-div');

document.getElementById('form').addEventListener('submit', (e) => {
    e.preventDefault()
    // formdata pack the form, then put it into json
    const fd = new FormData(e.target)
    const myjson = Object.fromEntries(fd)
    // console.log(typeof myjson)
    // console.log(myjson)
    fetch('http://localhost:8000', {
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
        const id = release['release'].match(/release\/([0-9a-fA-F-]{36})/)[1];
        console.log(id)
        const card = `
        <div class="release-card">
            <img src="${tn} alt="Album front image" >
            <p>${id}</p>
        </div>`;
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