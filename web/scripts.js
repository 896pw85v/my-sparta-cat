import * as tools from "./btools.js"

const releasesDiv = document.getElementById('releases-div');
const burl = 'http://localhost:8000'
document.getElementById('form').addEventListener('submit', (e) => {
    e.preventDefault()
    // formdata pack the form, then put it into json
    const fd = new FormData(e.target)
    const myjson = Object.fromEntries(fd)
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

function loadReleases(name_covers) {
    releasesDiv.innerHTML = '';
    Object.entries(name_covers).forEach(entry => {
        const card = tools.mkCard(entry); // this should be just one of the many cards
        releasesDiv.appendChild(card);
    });   
}

/*
name_covers: name -> []
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