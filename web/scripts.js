import * as tools from "./btools.js"

const artistsDiv = document.getElementById('artists-div');
const songsDiv = document.getElementById('songs-div');
const burl = ''; // same origin

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
        },
    })
        .then(res => res.json())
        .then(res => {
            if (!Array.isArray(res)) {
                // logic here is artists are {name: images}
                // songs are arr of [song1, song2, ...]
                putArtists(res)
            } else {
                putSongs(res)
            }
        })
        .catch((error) => (console.log(error)))
})

function putArtists(name_covers) {
    artistsDiv.parentElement.style.display = 'block';
    artistsDiv.innerHTML = '';
    Object.entries(name_covers).forEach(entry => {
        const card = tools.mkCard(entry); // this should be just one of the many cards
        card.addEventListener('click', jumpAlbum);
        artistsDiv.appendChild(card);
    });
}

function putSongs(songs) {
    songsDiv.parentElement.style.display = 'block';
    songsDiv.innerHTML = '';
    songs.forEach(song => {
        const row = tools.mkRow(song);
        row.addEventListener('click', jumpSong);
        songsDiv.appendChild(row);
    })
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
sign.submit
const create = document.getElementById('create-account')
sign.addEventListener('submit', (e) => {
    e.preventDefault()
    const fd = new FormData(e.target)
    console.log(typeof fd)
    console.log(fd)
    const myjson = Object.fromEntries(fd)
    console.log(myjson)
    fetch(burl + '/log-in', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(myjson)
    }).then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.success) {
                // sessionStorage.setItem('sid', data)
                updateUserProfile(data.name, '')
                sign.parentElement.style.display = "none"
                create.parentElement.style.display = 'none'
            }
        })
        .catch((reason) => {
            console.error("During log-in: ", reason)
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

/** maybe this should be a tool */
function updateUserProfile(username, photoUrl) {
    console.log(username)
    const profileBox = document.getElementById("profile-box");
    const profilePhoto = document.getElementById("profile-photo");
    const profileName = document.getElementById("profile-name");

    // If no username → logged out
    if (!username) {
        profileBox.classList.add("hidden");
        return;
    }
    console.log('update')
    // Logged-in state
    profileBox.classList.remove("hidden");

    // Update profile info
    profileName.textContent = username;
    profilePhoto.src = photoUrl || "https://tse1.mm.bing.net/th/id/OIP.KAFZkVR_hmUcavc7Dot5QAAAAA?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"; // fallback image
    // hard-coded profile photo. anyway. 
}

function jumpAlbum(e) {
    e.preventDefault()
    // implement for viewing songs from albums
}

function jumpSong(e) {
    e.preventDefault()
    fetch(burl + '/log-in', {
        credentials: 'include',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                console.log(e)
                const mbid = e.target.id 
                console.log(mbid)
                sessionStorage.setItem('songId', mbid)
                window.location.href = '/write-review'

            } else {
                confirm("Please log in before rating. ")
                return
            }
        })

}
