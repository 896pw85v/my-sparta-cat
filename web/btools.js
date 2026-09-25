// complete dom interaction, too ugly
export function mkCard(pack) {
  const artistName = pack[0];
  console.log(artistName)
  const albums = pack[1];

  // Create the main card container
  const artistCard = document.createElement('div');
  artistCard.classList.add('artist-card');

  // Create the artist info section
  const artistInfo = document.createElement('div');
  artistInfo.classList.add('artist-info');

  const h2 = document.createElement('h2');
  h2.classList.add('artist-name');
  h2.textContent = artistName;

  // const img = document.createElement('img');
  // img.classList.add('artist-photo');
  // img.src = "";
  // img.alt = `${artistName} Portrait`;

  // Assemble artist info
  artistInfo.appendChild(h2);
  // artistInfo.appendChild(img);
  artistCard.appendChild(artistInfo);

  // Create the release tiles container
  const releaseTiles = document.createElement('div');
  releaseTiles.classList.add('release-tiles');

  // Process albums
  for (let album of albums) {
    try {
      const thumbnails = album['images'][0]['thumbnails'];
      const cover = 'small' in thumbnails ? thumbnails['small'] : thumbnails['250'];
      // const releaseUrl = album['release']
      const title = album['title'];

      // Create individual release tile
      const releaseTile = document.createElement('div');
      releaseTile.classList.add('release-tile');

      const albumImg = document.createElement('img');
      albumImg.src = cover;
      albumImg.alt = title + " Cover";

      const span = document.createElement('span');
      span.classList.add('release-label');
      span.textContent = title;

      // Assemble release tile
      releaseTile.appendChild(albumImg);
      releaseTile.appendChild(span);

      // Append to container
      releaseTiles.appendChild(releaseTile);
    } catch {
      console.error('error while making tile')
      console.error(album)
    }
  }

  // Append all tiles to the main card
  artistCard.appendChild(releaseTiles);

  // Return the completed DOM node
  return artistCard;
}

// good alternative to consider, or just try htmx some day
/*
export function mkCard(pack) {
  const artistName = pack['artist'];
  const albums = pack['albums'] || [];

  // 1. Generate the HTML string for all album tiles
  const tilesHTML = albums.map(album => {
    try {
      const thumbnails = album['images'][0]['thumbnails'];
      const cover = 'small' in thumbnails ? thumbnails['small'] : thumbnails['250'];
      
      return `
        <div class="release-tile">
          <img src="${cover}" alt="Album Cover">
          <span class="release-label">${album['title']}</span>
        </div>
      `;
    } catch (err) {
      console.error('Error while making tile', album);
      return ''; // Return empty string for failed items so they don't break the loop
    }
  }).join(''); // Combine the array of strings into a single HTML string

  // 2. Create the main card container and inject the final structure
  const artistCard = document.createElement('div');
  artistCard.classList.add('artist-card');
  artistCard.innerHTML = `
    <div class="artist-info">
      <h2 class="artist-name">${artistName}</h2>
      <img class="artist-photo" src="" alt="${artistName} Portrait">
    </div>
    <div class="release-tiles">
      ${tilesHTML}
    </div>
  `;

  return artistCard;
}
*/

export function mkRow(item) {
  console.log('making card', item['title'])
  console.log(item.images.length);
  const ima = item.images;
  const thumbUrl =
    ima[0].thumbnails?.small ||
    ima[0].thumbnails?.large ||
    "";
  console.log('url', thumbUrl)
  const row = document.createElement("div");
  row.className = "song-row";

  row.innerHTML = `
          <img class="song-thumb" src="${thumbUrl}" alt="${item.title}">
          <div class="song-info">
              <p class="song-title">${item.title}</p>
              <p class="song-artist">${item["artist-credit-phrase"]}</p>
          </div>
      `;

  return row
}
