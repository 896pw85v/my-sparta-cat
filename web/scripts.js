import * as tools from "./btools.js"

const artistsDiv = document.getElementById('artists-div');
const songsDiv = document.getElementById('songs-div');
const blankPh = document.getElementById('blank-ph').cloneNode(true);
console.log(blankPh);
const burl = ''; // same origin

document.getElementById('form').addEventListener('submit', (e) => {
    e.preventDefault()
    // formdata pack the form, then put it into json
    const fd = new FormData(e.target)
    const myjson = Object.fromEntries(fd)
    // artistsDiv.parentElement.style.display = 'block';
    songsDiv.replaceChildren(blankPh);
    blankPh.style.display = 'block';
    songsDiv.parentElement.style.display = 'block';
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
        .catch((error) => {
            console.log(error);
            songsDiv.parentElement.style.display = 'none';
            alert("Search didn't complete. Please try again. ");
        })
})

function putArtists(name_covers) {
    // artistsDiv.parentElement.style.display = 'block';
    artistsDiv.innerHTML = '';
    Object.entries(name_covers).forEach(entry => {
        localStorage.setItem(entry.id, JSON.stringify(entry))
        const card = tools.mkCard(entry); // one of the many cards
        card.addEventListener('click', jumpAlbum);
        artistsDiv.appendChild(card);
    });
}

function putSongs(songs) {
    songsDiv.parentElement.style.display = 'block';
    blankPh.style.display = 'none';
    songs.forEach(song => {
        localStorage.setItem(song.id, JSON.stringify(song));
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
                updateUserProfile(data.name, '');
                loadMyReviews(data.name, null, 10, 0)
                sign.parentElement.style.display = "none"
                createForm.parentElement.style.display = 'none'
            }
        })
        .catch((reason) => {
            console.error("During log-in: ", reason)
        })
})
sign.requestSubmit()
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


const createForm = document.getElementById('create-account');
createForm.addEventListener('submit', createAccount);
function createAccount(e) {
    e.preventDefault();
    const form = e.target;
    const fd = new FormData(form);
    const myjson = Object.fromEntries(fd);
    if (myjson['password'] != myjson['confirm-password']) {
        alert('Password is not confirmed. '); // this can be real time detecting
        return;
    }
    delete myjson['confirm-password'];
    console.log(myjson)
    fetch(burl + '/sign-up', {
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
                updateUserProfile(data.name, '');
                loadMyReviews(data.name, null, 10, 0)
                sign.parentElement.style.display = "none"
                createForm.parentElement.style.display = 'none'
            }
        })
        .catch((reason) => {
            console.error("During log-in: ", reason)
        })
}
function loadMyReviews(name, mbid, limit, offset) {
    offset = 0; limit = 10;
    fetch(burl + '/reviews', {
        body: JSON.stringify({
            'offset': offset, 
            'limit': limit, 
            'name': name, 
            'mbid': mbid
        }), 
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(res => res.json())
    .then(reviews => {
        console.log(reviews);
        const cont = document.getElementById('my-reviews');
        for (let each of reviews) {
            const reviewCard = tools.makeReviewCard(each)
            cont.appendChild(reviewCard)
        }
    })
}