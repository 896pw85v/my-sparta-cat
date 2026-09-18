import * as tools from "./btools.js"

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
// TODO: put artist works for mult. artists
let out = {}
function loadReleases(ajson) {
    // console.log(ajson)
    const card = tools.mkCard(ajson) // this should be just one of the many cards
        // card = document.createElement('div');
    
    releasesDiv.appendChild(card)
}


/*
one res :   artist: ..., 
        [Song1 >  - images -> [ {...: ...} ] (idk why but only one dict)
                    |- releases
                    |- title -> title
        Song2 >  - images -> [ {...: ...} ] (idk why but only one dict)
                    |- releases
                    |- title -> title
        Song3...
                            {'thumbnails: 
                                'size': url, 
                                ...
                            }]
*/

const sign = document.getElementById('sign');
sign.addEventListener('submit', (e) => {
    e.preventDefault()
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

// create account, log in

// {
//     artist-name, 
//     optional-artist-photo, 
//     list-releases: {
//         {
//             release-name, 
//             release-image
//         }, 
//         ...,
//         ...
//     }
// }