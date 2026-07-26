(() => {
  const config = window.PARKER_BECKETT_CONFIG || { album: { trackSlugs: [] }, songs: {} };
  const songs = config.songs || {};
  const albumSet = new Set(config.album?.trackSlugs || []);
  const validEmbed = value => /^https:\/\/www\.youtube-nocookie\.com\/embed\/[A-Za-z0-9_-]+(?:\?[^#]*)?$/.test(value || '') && !/[?&]autoplay=1(?:&|$)/.test(value);

  const buildCard = song => {
    const article = document.createElement('article');
    article.className = 'video-card';
    const media = document.createElement('div');
    media.className = 'video-card-media';
    const videoUrl = (song.youtubeEmbedUrl || '').trim();
    const thumb = (song.videoThumbnail || '').trim();
    if (validEmbed(videoUrl)) {
      const iframe = document.createElement('iframe');
      iframe.src = videoUrl;
      iframe.title = `${song.title} official video`;
      iframe.loading = 'lazy';
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      iframe.allow = 'encrypted-media; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      media.appendChild(iframe);
    } else {
      const img = document.createElement('img');
      img.src = thumb || song.artworkPath;
      img.alt = thumb ? `Official video thumbnail for ${song.title}` : `Artwork for ${song.title}`;
      img.loading = 'lazy';
      img.decoding = 'async';
      media.appendChild(img);
      const state = document.createElement('span');
      state.className = 'video-card-state';
      state.textContent = 'Visual archive pending';
      media.appendChild(state);
    }
    const content = document.createElement('div');
    content.className = 'video-card-content';
    content.innerHTML = `<p class="eyebrow">${song.albumName || 'Standalone single'}</p><h3>${song.title}</h3><p>${validEmbed(videoUrl) ? 'Official video' : 'No official video published yet.'}</p><a class="text-link" href="${song.songPagePath}">View recording →</a>`;
    article.append(media, content);
    return article;
  };

  const albumGrid = document.querySelector('[data-video-group="album"]');
  (config.album?.trackSlugs || []).forEach(slug => songs[slug] && albumGrid?.appendChild(buildCard(songs[slug])));
  const standaloneGrid = document.querySelector('[data-video-group="standalone"]');
  Object.values(songs).filter(song => song.standaloneSingle).sort((a,b) => a.originalReleaseDate.localeCompare(b.originalReleaseDate)).forEach(song => standaloneGrid?.appendChild(buildCard(song)));

  const featured = Object.values(songs).find(song => validEmbed((song.youtubeEmbedUrl || '').trim()));
  if (featured) {
    const shell = document.querySelector('[data-featured-video]');
    const frame = shell?.querySelector('iframe');
    const placeholder = shell?.querySelector('.video-placeholder');
    if (frame) { frame.src = featured.youtubeEmbedUrl; frame.title = `${featured.title} official video`; frame.hidden = false; }
    if (placeholder) placeholder.hidden = true;
    const title = document.querySelector('[data-featured-title]');
    const description = document.querySelector('[data-featured-description]');
    if (title) title.textContent = featured.title;
    if (description) description.textContent = 'Official video';
  }
})();
