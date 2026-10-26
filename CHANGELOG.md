## Version 1.4 — October 26, 2026
- Added standalone singles Smile Bigger (August 22, 2026; QT6HR2604313) and You'll Have Me (September 29, 2026; QTA2U2647621).
- Added two complete song pages, original cover artwork, official lyric PDF sources and transcriptions, static SEO and JSON-LD, verified UPC identifiers, release chronology, lyrics navigation, and sitemap.
- Kept The Forecast at 15 tracks and preserved all 18 existing songs unchanged.
- Added neutral unpublished story/commentary states rather than the unapproved narratives.
- Expanded audit coverage to 20 songs and five standalone singles.

# Changelog

## Version 1.3 — Content readiness and pre-launch QA

- Preserved the verified 18-recording catalog, all ISRCs, dates, album relationships, page URLs, artwork, and official lyrics.
- Removed the incorrect Blue Light pending-transcription statement from the Lyrics page while preserving the complete official lyrics on the song page.
- Removed duplicate Story Behind the Song and Commentary presentations from all 18 song pages.
- Restored the standardized public order: lyrics, story, commentary, credits, share controls, and related songs.
- Replaced internal drafting instructions with restrained public archive states without inventing stories or commentary.
- Removed the unconfirmed “Additional credits” list item from public credit blocks; only confirmed credits remain.
- Added semantic, nonfunctional streaming states and HTTPS validation while keeping all seven platforms centralized in `site-config.js`.
- Enforced privacy-enhanced YouTube embeds, no autoplay, lazy loading, iframe titles, and safe referrer behavior.
- Rebuilt the existing Videos destination from the centralized catalog, grouping The Forecast and standalone singles and using supplied artwork until official thumbnails arrive.
- Added `videos-page.js`; no framework or build process was introduced.
- Refined the Journal empty state without inventing posts or dates.
- Added image dimensions, lazy loading, async decoding, and high-priority loading for primary artwork to reduce layout shift.
- Improved mobile navigation with Escape-key and outside-click closing plus accurate menu labels.
- Added targeted responsive refinements for streaming controls, editorial cards, video cards, and share controls.
- Added `CONTENT_STATUS.md`, a private page-by-page and song-by-song editorial inventory.
- Expanded `audit_site.py` for content-readiness, privacy embeds, internal-document exposure, lyric preservation, and catalog checks.
- Updated README maintenance and deployment instructions.
- No missing story, commentary, credit, streaming link, thumbnail, or video URL was invented.

## Version 1.2 — Verified catalog and release history

- Expanded `site-config.js` into the authoritative metadata source for all 18 recordings while retaining centralized streaming and video fields.
- Added the verified ISRC and original release date for every recording.
- Classified Merrily, Looks Fine to Me, No Return, and Aware as pre-album singles later included on The Forecast.
- Classified eleven recordings as first released with The Forecast on June 26, 2026.
- Classified Bad Idea Tourette's, Run It Straight, and Already In as standalone singles outside the album.
- Updated all 18 song-page release blocks with the correct classification, dates, album association, and ISRC.
- Updated MusicRecording JSON-LD to include verified `datePublished`, `isrcCode`, `url`, `image`, and `inAlbum` where applicable.
- Updated The Forecast MusicAlbum JSON-LD and its complete 15-track structured track list.
- Added subtle release-history labels to every album track on The Forecast page.
- Reworked the Music page into the verified eight-entry release chronology without treating album-debut tracks as separate singles.
- Updated related-release navigation while preserving all established song URLs.
- Corrected title capitalization to “Looks Fine to Me” and “I Was the Island” while retaining their established slugs.
- Preserved the complete official Blue Light lyrics and all existing supplied lyrics and artwork.
- Expanded `audit_site.py` to validate catalog metadata, release classifications, album membership, ISRC format and uniqueness, song-page metadata, structured data, links, assets, IDs, scripts, and sitemap coverage.
- Updated README maintenance instructions and removed the outdated Blue Light/release-metadata request.
