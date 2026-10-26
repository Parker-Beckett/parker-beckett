# Parker Beckett Official Website — Version 1.3

Static HTML, CSS, and JavaScript website for **Parker Beckett**, created and written by Corey Winfield and released through Soul Tech Records. It requires no framework, build process, database, server, or Node installation for deployment.

## Project structure

- `site-config.js` — authoritative catalog, release metadata, streaming URLs, video URLs, thumbnail paths, content-status fields, and confirmed credits.
- `song-page.js` — renders streaming controls, validates privacy-enhanced video embeds, and powers Copy Link.
- `videos-page.js` — builds the Videos catalog from the same `site-config.js` data.
- `script.js` — shared mobile navigation behavior.
- `songs/` — static song pages containing lyrics, static SEO, release history, and JSON-LD.
- `assets/images/` — supplied artwork and site imagery.
- `audit_site.py` — project QA audit.
- `CONTENT_STATUS.md` — internal content inventory; not linked publicly.
- `AUDIT_REPORT.md` — latest QA result; not linked publicly.
- `CHANGELOG.md` — version history; not linked publicly.

## Preview locally

From the project folder:

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`.

## Add or change a streaming URL

1. Open `site-config.js`.
2. Find the correct song slug under `songs`.
3. Find the platform inside that song’s `streaming` object.
4. Paste the verified HTTPS **song-specific** URL between the quotation marks.
5. Save and refresh the page.

An empty value keeps only that song/platform unavailable and displays **Link Coming Soon**. The seven supported keys are `spotify`, `appleMusic`, `amazonMusic`, `youtubeMusic`, `pandora`, `deezer`, and `tidal`.

## Add an official YouTube video

1. Use the privacy-enhanced embed form only:

```text
https://www.youtube-nocookie.com/embed/VIDEO_ID
```

2. Paste it into that song’s `youtubeEmbedUrl` value in `site-config.js`.
3. Do not add an autoplay parameter.

The song page and `videos.html` will both update from the same value.

## Add a video thumbnail

1. Export a 16:9 JPG or WebP, ideally 1280 × 720.
2. Add it to `assets/images/` with a lowercase hyphenated filename.
3. Put the relative path in the song’s `videoThumbnail` field, for example:

```text
assets/images/blue-light-video.webp
```

Until a released thumbnail is supplied, the Videos page intentionally uses the song artwork.

## Replace a Story Behind the Song placeholder

Open the song’s HTML file. In `.song-details`, find the article with:

```html
data-content-status="story-placeholder"
```

Replace only its heading and paragraph with Corey’s approved text. Change the status attribute to `story-approved`, then update `storyStatus` in `site-config.js` to `approved`.

## Replace a commentary placeholder

In the same `.song-details` section, find:

```html
data-content-status="commentary-placeholder"
```

Replace only the heading and paragraph with approved commentary. Change the status attribute to `commentary-approved`, then update `commentaryStatus` in `site-config.js` to `approved`.

## Update confirmed credits

Credits appear as static HTML so they remain visible to search engines and visitors without JavaScript. The same confirmed fields also appear in `site-config.js` for catalog maintenance. Update both locations only after the credit is confirmed. Do not add an unverified producer, performer, engineer, studio, publisher, PRO, UPC, or catalog number.

## Add an official lyric sheet

1. Use a web-safe lowercase filename, such as `blue-light-official-lyric-sheet.pdf`.
2. Create `assets/documents/` if it does not exist and place the file there.
3. Add the path to the song’s `lyricSheetPath` field in `site-config.js`.
4. Add a clearly labeled link near the lyric section, such as **Download the official Blue Light lyric sheet**.
5. Run the audit to verify the document is included and the link resolves.

## Update an ISRC or release date

Update the verified values in `site-config.js`, the song page release block, and the song page’s JSON-LD. Album changes may also require updates to `the-forecast.html`. Run the audit after every metadata change.

## Add a journal entry

Open `journal.html` and replace or follow the existing archive pattern with an approved `<article>`. Use only a real title, date, summary, and final text. Add a separate page and sitemap URL only when a permanent shareable entry is needed.

## Run QA

```bash
python3 audit_site.py
```

The audit checks catalog integrity, ISRCs, album membership, song structure, lyrics, placeholders, links, assets, embeds, canonical URLs, sitemap coverage, robots.txt, JavaScript syntax, and internal-document exposure.

## Deploy to Cloudflare Pages

### Direct Upload

1. Open Cloudflare **Workers & Pages**.
2. Create or open the Parker Beckett Pages project.
3. Choose Direct Upload.
4. Upload the contents of the deployment ZIP, with `index.html` at the root.
5. No build command or framework preset is needed.

### Connect `parkerbeckett.com`

In the Pages project, open **Custom domains**, add `parkerbeckett.com`, and follow Cloudflare’s DNS instructions. Add `www.parkerbeckett.com` only when the preferred redirect behavior is configured.

### Future updates

Edit the project copy, preview locally, run `python3 audit_site.py`, create a fresh deployment ZIP, and upload it as a new Cloudflare deployment.

## Internal documentation

`README.md`, `CHANGELOG.md`, `AUDIT_REPORT.md`, `CONTENT_STATUS.md`, and `audit_site.py` are maintenance files. They are included in the complete project archive but omitted from the Cloudflare-ready deployment ZIP.

## Information still needed

- Official song-specific streaming URLs.
- Official YouTube privacy-enhanced embed URLs.
- Released video thumbnails.
- Approved Story Behind the Song text.
- Approved commentary or confirmation of existing topic notes.
- Additional confirmed production, performance, engineering, publishing, or recording credits.
- Official lyric-sheet files intended for public download.


## Catalog expansion (Version 1.4)
Two additional standalone recordings are cataloged in `site-config.js`: Smile Bigger and You'll Have Me. Their original lyric PDFs are retained under `assets/documents/` and linked from the song pages. The album track list remains unchanged at 15. Only verified streaming and video URLs should be populated. Story and commentary entries require Corey's explicit approval before publication.
