(() => {
  const config = window.PARKER_BECKETT_CONFIG || { songs: {} };
  const page = document.querySelector('[data-song-slug]');
  if (!page) return;
  const slug = page.dataset.songSlug;
  const song = config.songs?.[slug] || {};
  const labels = { spotify: 'Spotify', appleMusic: 'Apple Music', amazonMusic: 'Amazon Music', youtubeMusic: 'YouTube Music', pandora: 'Pandora', deezer: 'Deezer', tidal: 'Tidal' };
  const validHttps = value => { try { return new URL(value).protocol === 'https:'; } catch { return false; } };
  const validEmbed = value => /^https:\/\/www\.youtube-nocookie\.com\/embed\/[A-Za-z0-9_-]+(?:\?[^#]*)?$/.test(value || '') && !/[?&]autoplay=1(?:&|$)/.test(value);

  const streamGrid = document.querySelector('[data-streaming-links]');
  if (streamGrid) Object.entries(labels).forEach(([key, label]) => {
    const url = (song.streaming?.[key] || '').trim();
    const active = validHttps(url);
    const el = document.createElement(active ? 'a' : 'span');
    el.className = `stream-button${active ? '' : ' disabled'}`;
    if (active) {
      el.textContent = label;
      el.href = url;
      el.target = '_blank';
      el.rel = 'noopener noreferrer';
      el.setAttribute('aria-label', `Listen to ${song.title || 'this song'} on ${label} (opens in a new tab)`);
    } else {
      el.textContent = `${label} · Link Coming Soon`;
      el.setAttribute('role', 'link');
      el.setAttribute('aria-disabled', 'true');
      el.setAttribute('title', `${label} link coming soon`);
    }
    streamGrid.appendChild(el);
  });

  const videoFrame = document.querySelector('[data-video-frame]');
  const videoPlaceholder = document.querySelector('[data-video-placeholder]');
  const videoUrl = (song.youtubeEmbedUrl || '').trim();
  if (videoFrame && validEmbed(videoUrl)) {
    videoFrame.src = videoUrl;
    videoFrame.title = `${song.title || 'Song'} official video`;
    videoFrame.hidden = false;
    if (videoPlaceholder) videoPlaceholder.hidden = true;
  }

  const copyButton = document.querySelector('[data-copy-link]');
  if (copyButton) copyButton.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(window.location.href); }
    catch {
      const input = document.createElement('textarea'); input.value = window.location.href;
      document.body.appendChild(input); input.select(); document.execCommand('copy'); input.remove();
    }
    copyButton.textContent = 'Link Copied';
    setTimeout(() => { copyButton.textContent = 'Copy Link'; }, 1800);
  });
})();
