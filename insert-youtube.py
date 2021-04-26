import argparse
import datetime
import math
import os
import random
import sqlite3
import urllib.parse
import uuid
import PIL.Image
import requests

parser = argparse.ArgumentParser()
parser.add_argument("space_id", help="UUID of the space to add to")
parser.add_argument("URL", help="YouTube video URL")
args = parser.parse_args()

if not os.path.exists(os.path.join('.', 'storage', 'my_spacedeck_bucket', 's{}'.format(args.space_id))):
    parser.error('Space UUID doesn\'t exist in local storage')

youtubeurl = urllib.parse.urlparse(args.URL, allow_fragments=True)
if youtubeurl.netloc == 'youtu.be':
    videoid = youtubeurl.path.strip('/')
elif youtubeurl.path == '/watch':
    videoid = urllib.parse.parse_qs(youtubeurl.query)['v'][0]
else:
    parser.error('Don\'t understand the YouTube URL')

artifactid = str(uuid.uuid4())
localstoragedir = os.path.join('.', 'storage', 'my_spacedeck_bucket', 's{}'.format(args.space_id), 'a{}'.format(artifactid))
try:
    os.mkdir(localstoragedir)
except FileExistsError:
    pass

r = requests.get('https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(videoid), stream=True)
if r.status_code != requests.codes.ok:
    r = requests.get('https://i.ytimg.com/vi/{}/hq720.jpg'.format(videoid), stream=True)
    if r.status_code != requests.codes.ok:
        r = requests.get('https://i.ytimg.com/vi/{}/sddefault.jpg'.format(videoid), stream=True)
        if r.status_code != requests.codes.ok:
            r = requests.get('https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(videoid), stream=True)
            if r.status_code != requests.codes.ok:
                parser.error('Don\'t understand the YouTube URL thumbnail')

thumbnailfile = urllib.parse.urlparse(r.url, allow_fragments=True).path.split('/')[-1]

with open(os.path.join(localstoragedir, thumbnailfile), 'wb') as fd:
    for chunk in r.iter_content(chunk_size=128):
        fd.write(chunk)

im = PIL.Image.open(os.path.join(localstoragedir, thumbnailfile))
w, h = im.size

big = None
if w > 1920 or h > 1920:
    if w == h:
        big = im.resize((1920, 1920), resample=3, reducing_gap=2.0)
    elif w > h:
        big = im.resize((1920, int(math.floor((float(h) / float(w)) * 1920))), resample=3, reducing_gap=2.0)
    elif w < h:
        big = im.resize((int(math.floor((float(w) / float(h)) * 1920)), 1920), resample=3, reducing_gap=2.0)

medium = None
if w > 800 or h > 800:
    if w == h:
        medium = im.resize((800, 800), resample=3, reducing_gap=2.0)
    elif w > h:
        medium = im.resize((800, int(math.floor((float(h) / float(w)) * 800))), resample=3, reducing_gap=2.0)
    elif w < h:
        medium = im.resize((int(math.floor((float(w) / float(h)) * 800)), 800), resample=3, reducing_gap=2.0)

small = None
if w > 320 or h > 320:
    if w == h:
        small = im.resize((320, 320), resample=3, reducing_gap=2.0)
    elif w > h:
        small = im.resize((320, int(math.floor((float(h) / float(w)) * 320))), resample=3, reducing_gap=2.0)
    elif w < h:
        small = im.resize((int(math.floor((float(w) / float(h)) * 320)), 320), resample=3, reducing_gap=2.0)

if big:
    big.save(os.path.join(localstoragedir, '1920_{}.jpg'.format(thumbnailfile)))
    big.close()

if medium:
    medium.save(os.path.join(localstoragedir, '800_{}.jpg'.format(thumbnailfile)))
    medium.close()

if small:
    small.save(os.path.join(localstoragedir, '320_{}.jpg'.format(thumbnailfile)))
    small.close()

im.close()

con = sqlite3.connect('database.sqlite')
cur = con.cursor()

dbstoragedir = os.path.join('/storage', 's{}'.format(args.space_id), 'a{}'.format(artifactid))
webthumb = None
if small:
    webthumb = os.path.join(dbstoragedir, '320_{}.jpg'.format(thumbnailfile))
else:
    webthumb = os.path.join(dbstoragedir, thumbnailfile)

medthumb = None
if medium:
    medthumb = os.path.join(dbstoragedir, '800_{}.jpg'.format(thumbnailfile))
else:
    medthumb = os.path.join(dbstoragedir, thumbnailfile)

bigthumb = None
if big:
    bigthumb = os.path.join(dbstoragedir, '1920_{}.jpg'.format(thumbnailfile))
else:
    bigthumb = os.path.join(dbstoragedir, thumbnailfile)

cur.execute("INSERT INTO artifacts(_id, space_id, mime, link_uri, x, y, w, h, payload_thumbnail_web_uri, payload_thumbnail_medium_uri, payload_thumbnail_big_uri, created_at, updated_at, createdAt, updatedAt) VALUES (:id, :space_id, :mime, :link_uri, :x, :y, :w, :h, :payload_thumbnail_web_uri, :payload_thumbnail_medium_uri, :payload_thumbnail_big_uri, :ct, :ut, :ct, :ut)", \
    {"id": artifactid, \
     "space_id": args.space_id, \
     "mime": "x-spacedeck/oembed-youtube", \
     "link_uri": args.URL, \
     "x": 250 + random.randint(0, 2000), \
     "y": 250 + random.randint(0, 2000), \
     "w": 640, \
     "h": 360, \
     "payload_thumbnail_web_uri": webthumb, \
     "payload_thumbnail_medium_uri": medthumb, \
     "payload_thumbnail_big_uri": bigthumb, \
     "ct": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f +00:00"),
     "ut": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f +00:00")})

con.commit()
con.close()
