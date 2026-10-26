#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import json, re, subprocess, sys, zipfile

root=Path(__file__).resolve().parent
errors=[]; warnings=[]
expected={
'aware':('Aware','QT3F52623418','single_later_included_on_album','2026-06-18'),
'looks-fine-to-me':('Looks Fine to Me','QT3F42662021','single_later_included_on_album','2026-06-07'),
'dead-end':('Dead End','QT3F72610084','album_track','2026-06-26'),
'merrily':('Merrily','QT3F42661902','single_later_included_on_album','2026-05-31'),
'no-return':('No Return','QT3F52617991','single_later_included_on_album','2026-06-11'),
'after-all':('After All','QT3F72610085','album_track','2026-06-26'),
'movies':('Movies','QT3F72610086','album_track','2026-06-26'),
'bubblegum-tuesday':('Bubblegum Tuesday','QT3F72610087','album_track','2026-06-26'),
'sorry':('Sorry','QT3F72610088','album_track','2026-06-26'),
'on-air':('On Air','QT3F72610089','album_track','2026-06-26'),
'what-have-i-done':('What Have I Done','QT3F72610090','album_track','2026-06-26'),
'blue-light':('Blue Light','QT3F72610091','album_track','2026-06-26'),
'normal':('Normal','QT3F72610092','album_track','2026-06-26'),
'i-was-the-island':('I Was the Island','QT3F72610093','album_track','2026-06-26'),
'seattle':('Seattle','QT3F72610094','album_track','2026-06-26'),
'bad-idea-tourettes':("Bad Idea Tourette's",'QT3FA2635455','standalone_single','2026-06-07'),
'run-it-straight':('Run It Straight','QT6EF2616658','standalone_single','2026-06-28'),
'already-in':('Already In','QT6F62657669','standalone_single','2026-07-14')}
album=['aware','looks-fine-to-me','dead-end','merrily','no-return','after-all','movies','bubblegum-tuesday','sorry','on-air','what-have-i-done','blue-light','normal','i-was-the-island','seattle']
pre={'merrily','looks-fine-to-me','no-return','aware'}
standalone={'bad-idea-tourettes','run-it-straight','already-in'}
internal_docs={'README.md','CHANGELOG.md','AUDIT_REPORT.md','CONTENT_STATUS.md','audit_site.py'}
platforms={'spotify','appleMusic','amazonMusic','youtubeMusic','pandora','deezer','tidal'}

# Configuration integrity.
config_text=(root/'site-config.js').read_text(encoding='utf-8')
m=re.search(r'window\.PARKER_BECKETT_CONFIG\s*=\s*(\{[\s\S]*\})\s*;\s*$',config_text)
if not m:
    errors.append('site-config.js: unable to parse centralized configuration'); config={}
else:
    try: config=json.loads(m.group(1))
    except Exception as exc: errors.append(f'site-config.js: invalid JSON object: {exc}'); config={}
if config.get('version')!='1.3': errors.append('site-config.js: version is not 1.3')
songs=config.get('songs',{})
if set(songs)!=set(expected): errors.append(f'site-config.js: expected 18 songs, found {len(songs)}')
isrcs=[]
for slug,(title,isrc,rtype,date) in expected.items():
    item=songs.get(slug,{})
    required=('title','slug','isrc','releaseType','originalReleaseDate','artworkPath','songPagePath','streaming','youtubeEmbedUrl','videoThumbnail','lyricsStatus','storyStatus','commentaryStatus','confirmedCredits')
    for key in required:
        if key not in item: errors.append(f'site-config.js: {slug} missing {key}')
    if item.get('title')!=title: errors.append(f'site-config.js: {slug} title mismatch')
    if item.get('isrc')!=isrc: errors.append(f'site-config.js: {slug} ISRC mismatch')
    if item.get('releaseType')!=rtype: errors.append(f'site-config.js: {slug} release type mismatch')
    if item.get('originalReleaseDate')!=date: errors.append(f'site-config.js: {slug} release date mismatch')
    if item.get('lyricsStatus')!='complete': errors.append(f'site-config.js: {slug} lyrics not marked complete')
    if not re.fullmatch(r'[A-Z]{2}[A-Z0-9]{3}\d{7}',item.get('isrc','')): errors.append(f'site-config.js: malformed ISRC for {slug}')
    isrcs.append(item.get('isrc'))
    if set(item.get('streaming',{}))!=platforms: errors.append(f'site-config.js: {slug} streaming platform set mismatch')
    for platform,url in item.get('streaming',{}).items():
        if url and not re.match(r'^https://',url): errors.append(f'site-config.js: {slug}/{platform} populated URL is not HTTPS')
    video=item.get('youtubeEmbedUrl','')
    if video:
        if not re.match(r'^https://www\.youtube-nocookie\.com/embed/[A-Za-z0-9_-]+(?:\?[^#]*)?$',video): errors.append(f'site-config.js: {slug} invalid YouTube privacy embed')
        if re.search(r'[?&]autoplay=1(?:&|$)',video): errors.append(f'site-config.js: {slug} autoplay enabled')
    if slug in album:
        if item.get('albumName')!='The Forecast' or item.get('albumReleaseDate')!='2026-06-26': errors.append(f'site-config.js: {slug} album association mismatch')
    else:
        if item.get('albumName') or item.get('albumReleaseDate'): errors.append(f'site-config.js: standalone {slug} associated with album')
if len(isrcs)!=len(set(isrcs)): errors.append('site-config.js: duplicate ISRC values')
if config.get('album',{}).get('trackSlugs')!=album: errors.append('site-config.js: album track order mismatch')
if config.get('album',{}).get('trackCount')!=15: errors.append('site-config.js: The Forecast track count is not 15')

# General HTML, assets, IDs, SEO, public/internal separation.
html_files=sorted(root.rglob('*.html'))
for file in html_files:
    raw=file.read_text(encoding='utf-8')
    rel=file.relative_to(root)
    if len(re.findall(r'<!DOCTYPE html>',raw,re.I))!=1: errors.append(f'{rel}: expected exactly one doctype')
    soup=BeautifulSoup(raw,'html.parser')
    if not soup.title or not soup.title.get_text(strip=True): errors.append(f'{rel}: missing title')
    for attrs,label in [({'name':'description'},'description'),({'property':'og:title'},'OG title'),({'property':'og:description'},'OG description'),({'property':'og:image'},'OG image'),({'name':'twitter:card'},'Twitter card')]:
        if not soup.find('meta',attrs=attrs): errors.append(f'{rel}: missing {label}')
    canonical=soup.find('link',rel='canonical')
    expected_url='https://parkerbeckett.com/' + ('' if rel.as_posix()=='index.html' else rel.as_posix())
    if not canonical: errors.append(f'{rel}: missing canonical')
    elif canonical.get('href')!=expected_url: errors.append(f'{rel}: canonical mismatch ({canonical.get("href")})')
    ids=[x.get('id') for x in soup.find_all(id=True)]
    dup={x for x in ids if ids.count(x)>1}
    if dup: errors.append(f'{rel}: duplicate IDs {sorted(dup)}')
    for img in soup.find_all('img'):
        if not img.get('alt','').strip(): errors.append(f'{rel}: image missing alt ({img.get("src")})')
        if not img.get('width') or not img.get('height'): warnings.append(f'{rel}: image has no explicit dimensions ({img.get("src")})')
    for frame in soup.find_all('iframe'):
        if not frame.get('title','').strip(): errors.append(f'{rel}: iframe missing title')
        if frame.get('src'):
            if 'youtube-nocookie.com' not in frame['src']: errors.append(f'{rel}: iframe is not privacy-enhanced YouTube')
            if 'autoplay=1' in frame['src']: errors.append(f'{rel}: autoplay enabled')
    for tag,attr in [('a','href'),('img','src'),('script','src'),('link','href')]:
        for el in soup.find_all(tag):
            value=el.get(attr)
            if not value or value.startswith(('#','mailto:','tel:','data:','javascript:')): continue
            parsed=urlparse(value)
            if parsed.scheme or value.startswith('//'): continue
            path=unquote(parsed.path)
            if not path: continue
            target=(file.parent/path).resolve()
            try: target.relative_to(root.resolve())
            except ValueError: errors.append(f'{rel}: path escapes project ({value})'); continue
            if path.endswith('/'): target=target/'index.html'
            if not target.exists(): errors.append(f'{rel}: broken local reference ({value})')
            if target.name in internal_docs: errors.append(f'{rel}: publicly links internal documentation ({target.name})')

# Song structure, lyrics, metadata, placeholders, streaming/video architecture.
for slug,(title,isrc,rtype,date) in expected.items():
    file=root/'songs'/f'{slug}.html'
    if not file.exists(): errors.append(f'missing song page: {slug}'); continue
    soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    main=soup.select_one(f'main.song-page[data-song-slug="{slug}"]')
    if not main: errors.append(f'{slug}: missing song-page slug'); continue
    sections=['song-hero','song-streaming','song-video','song-body','song-details','share-row','song-next']
    children=[c for c in main.children if getattr(c,'name',None)]
    positions=[]
    for cls in sections:
        nodes=soup.select('.'+cls)
        if len(nodes)!=1: errors.append(f'{slug}: expected one .{cls}, found {len(nodes)}')
        elif nodes[0].parent==main: positions.append(children.index(nodes[0]))
        else: errors.append(f'{slug}: .{cls} is not a direct main child')
    if positions!=sorted(positions): errors.append(f'{slug}: standardized section order is incorrect')
    details=soup.select('.song-details .detail-card')
    headings=[x.select_one('.eyebrow').get_text(' ',strip=True) for x in details if x.select_one('.eyebrow')]
    if headings!=['Story Behind the Song','Commentary','Credits']: errors.append(f'{slug}: editorial/credits order mismatch ({headings})')
    if soup.select('.song-body aside'): errors.append(f'{slug}: duplicate editorial aside remains in lyrics section')
    lyrics=soup.select_one('.lyrics-text')
    if not lyrics or len(lyrics.get_text(' ',strip=True))<150: errors.append(f'{slug}: lyrics missing or replaced by placeholder')
    release=' '.join(soup.select_one('.song-hero').stripped_strings)
    if isrc not in release: errors.append(f'{slug}: ISRC missing from release block')
    if rtype=='single_later_included_on_album' and not all(x in release for x in ('Original single release','Later included on','The Forecast','June 26, 2026')): errors.append(f'{slug}: incomplete pre-album release history')
    if rtype=='album_track' and not all(x in release for x in ('Original release','Release','The Forecast','June 26, 2026')): errors.append(f'{slug}: incorrect album-debut release block')
    if rtype=='standalone_single' and ('Standalone single' not in release or 'Release date' not in release or 'The Forecast' in release): errors.append(f'{slug}: incorrect standalone release block')
    ld=soup.find('script',attrs={'type':'application/ld+json'})
    try: data=json.loads(ld.string)
    except Exception: errors.append(f'{slug}: invalid JSON-LD'); data={}
    if data.get('isrcCode')!=isrc or data.get('datePublished')!=date: errors.append(f'{slug}: JSON-LD mismatch')
    if slug in album and data.get('inAlbum',{}).get('name')!='The Forecast': errors.append(f'{slug}: JSON-LD missing inAlbum')
    if slug in standalone and 'inAlbum' in data: errors.append(f'{slug}: standalone JSON-LD has inAlbum')
    stream=soup.select_one('[data-streaming-links]')
    if not stream: errors.append(f'{slug}: streaming mount missing')
    frame=soup.select_one('[data-video-frame]')
    if not frame or not frame.get('title'): errors.append(f'{slug}: video frame/title missing')
    if frame and frame.get('src'): errors.append(f'{slug}: static iframe src should come only from site-config.js')
    if len(soup.select('.song-next'))!=1 or len(soup.select('.song-next a'))<1: errors.append(f'{slug}: related songs missing')

# Blue Light exact preservation markers and false missing claims.
blue_soup=BeautifulSoup((root/'songs/blue-light.html').read_text(encoding='utf-8'),'html.parser')
blue=blue_soup.select_one('.lyrics-text').get_text('\n',strip=True)
for line in ["Moonlight's been testing patience","Blue light dancing through the hall","Than everything else ever did"]:
    if line not in blue: errors.append(f'blue-light: official lyric line missing ({line})')
site_text=' '.join(p.read_text(encoding='utf-8',errors='ignore').lower() for p in root.rglob('*.html'))
for phrase in ('blue light lyrics were not provided','approved blue light lyric transcription is not included','official lyric transcription will be added'):
    if phrase in site_text: errors.append(f'public site contains false Blue Light missing claim ({phrase})')

# Forecast and chronology.
forecast=BeautifulSoup((root/'the-forecast.html').read_text(encoding='utf-8'),'html.parser')
track_hrefs=[a.get('href') for a in forecast.select('a.track-row')]
if track_hrefs!=[f'songs/{s}.html' for s in album]: errors.append(f'the-forecast.html: track list mismatch ({len(track_hrefs)})')
for slug in standalone:
    if f'songs/{slug}.html' in track_hrefs: errors.append(f'the-forecast.html: standalone included ({slug})')
if len(forecast.select('.release-note'))!=15: errors.append('the-forecast.html: release labels not present for all 15 tracks')
music=BeautifulSoup((root/'music.html').read_text(encoding='utf-8'),'html.parser')
chron=[a.get('href') for a in music.select('.chronology-row')]
expected_chron=['songs/merrily.html','songs/bad-idea-tourettes.html','songs/looks-fine-to-me.html','songs/no-return.html','songs/aware.html','the-forecast.html','songs/run-it-straight.html','songs/already-in.html']
if chron!=expected_chron: errors.append('music.html: eight-entry chronology mismatch')

# Videos page uses central config and has no hardcoded external embed.
video=BeautifulSoup((root/'videos.html').read_text(encoding='utf-8'),'html.parser')
scripts=[x.get('src') for x in video.find_all('script',src=True)]
if 'site-config.js' not in scripts or 'videos-page.js' not in scripts: errors.append('videos.html: centralized video scripts missing')
if video.select('iframe[src]'): errors.append('videos.html: hardcoded video URL present')

# Source lyric document links, when any are added.
for file in html_files:
    soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    for a in soup.find_all('a',href=True):
        if re.search(r'\.(pdf|docx?)$',a['href'],re.I):
            if 'official lyric sheet' not in a.get_text(' ',strip=True).lower(): warnings.append(f'{file.relative_to(root)}: document link wording should identify an official lyric sheet')

# Sitemap, robots, JS syntax.
sitemap=(root/'sitemap.xml').read_text(encoding='utf-8')
for file in html_files:
    rel=file.relative_to(root).as_posix()
    if rel=='404.html': continue
    url='https://parkerbeckett.com/' + ('' if rel=='index.html' else rel)
    if url not in sitemap: errors.append(f'sitemap.xml: missing {url}')
robots=(root/'robots.txt').read_text(encoding='utf-8')
if 'User-agent:' not in robots or 'Sitemap: https://parkerbeckett.com/sitemap.xml' not in robots: errors.append('robots.txt: invalid or sitemap missing')
for js in ['site-config.js','script.js','song-page.js','videos-page.js']:
    result=subprocess.run(['node','--check',str(root/js)],capture_output=True,text=True)
    if result.returncode: errors.append(f'{js}: JavaScript syntax error ({result.stderr.strip()})')

print(f'Audited {len(html_files)} HTML pages, {len(expected)} recordings, 4 JavaScript files, sitemap, robots, assets, and content states.')
print('Verified 4 pre-album singles, 11 album-debut tracks, 3 standalone singles, and exactly 15 The Forecast tracks.')
if warnings:
    print('\nWarnings:')
    for item in sorted(set(warnings)): print(' -',item)
if errors:
    print('\nBlocking errors:')
    for item in errors: print(' -',item)
    sys.exit(1)
print('PASS: no blocking catalog, lyric, structure, placeholder, link, asset, privacy, SEO, sitemap, robots, or JavaScript errors found.')
