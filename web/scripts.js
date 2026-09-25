import * as tools from "./btools.js"

const artistsDiv = document.getElementById('artists-div');
const songsDiv = document.getElementById('songs-div');
const burl = 'http://localhost:8000';
const userProfile = {}

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
    .then(res => {
        if (!Array.isArray(res)) { 
            putArtists(res)
        } else {
            putSongs(res)
        }
    })
    .catch((error) => (console.log(error)))
})

function putArtists(name_covers) {
    artistsDiv.innerHTML = '';
    Object.entries(name_covers).forEach(entry => {
        const card = tools.mkCard(entry); // this should be just one of the many cards
        card.addEventListener('click', jumpAlbum);
        artistsDiv.appendChild(card);
    });   
}

function putSongs(songs) {
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
        if (data) {
            sessionStorage.setItem('sid', data)
            updateUserProfile(fd.get('u-name'), '')
            sign.parentElement.style.display = "none"
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
    // const loginBtn = document.getElementById("login-btn");
    const profileBox = document.getElementById("profile-box");
    const profilePhoto = document.getElementById("profile-photo");
    const profileName = document.getElementById("profile-name");
  
    // If no username → logged out
    if (!username) {
    //   loginBtn.classList.remove("hidden");
      profileBox.classList.add("hidden");
      return;
    }
  console.log('update')
    // Logged-in state
    // loginBtn.classList.add("hidden");
    profileBox.classList.remove("hidden");
  
    // Update profile info
    profileName.textContent = username;
    profilePhoto.src = photoUrl || "https://tse1.mm.bing.net/th/id/OIP.KAFZkVR_hmUcavc7Dot5QAAAAA?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"; // fallback image
  }

  function jumpAlbum() {

  }

  function jumpSong() {
    
  }