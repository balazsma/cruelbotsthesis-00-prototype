from __future__ import unicode_literals
from pathlib import Path
import gspread
import facebook
from oauth2client.service_account import ServiceAccountCredentials
from mutagen.mp3 import MP3
import moviepy.editor as mpe
import random as rng
import glob, os, requests, json, datetime, time, youtube_dl, db_access

# os.chdir(/path/to/your/script)

def download(link, rng):
    # this is a somewhat lousy implementation, but YoutubeDL does not always manage to download certain videos
    # for several reasons
    ytError = True
    # setting the parameters of YoutubeDL
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors':
        [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
        }

    while ytError:
        try:
            # so if everything goes according to plan, ytError is set to False, therefore the loop is broken, and the URL is returned
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(link)
            ytError = False
            return link
            # if an exception occurst, another download is attempted with another URL
        except:
            link = db_access.get_url(rng.randint(0, db_access.get_max()))



date = datetime.datetime.now()
weekday = date.strftime("%a")
# configuration of your Facebook page, and whatnot
fb_config = json.loads(Path("fb_config.json").read_text())
page_access_token = fb_config["access_token"]
facebook_page_id = fb_config["page_id"]
graph = facebook.GraphAPI(page_access_token)


# a random URL from the database is returned, and is passed to YoutubeDL for downloading and audio extraction
# the URL is also stored in a variable, so that it can be used as the video's description

title = download(db_access.get_url(rng.randint(0, db_access.get_max())), rng)
# renames every .mp3 file in the directory to audio.mp3, just to make sure that a valid file is passed
for files in glob.glob("*.mp3"):
    os.rename(files, "audio.mp3")

opDuration = rng.randint(45, 90)
lgth = MP3("audio.mp3").info.length
bgmusic = mpe.AudioFileClip("audio.mp3")

# the Bot would post the Evangelion ending on Sundays, and the opening on other days
if weekday=="Sun":
    # of course you change the file structure and relative paths however it suits you
    # although remember that if you plan to automate it (i.e. with cron), you should
    # uncomment line 11 and change it to the absolute path of this script
    originalOp = mpe.VideoFileClip("./FLYME/ED.mp4")
else:
    originalOp = mpe.VideoFileClip("./CRUAT/OP.mp4")

if lgth<45:
    # if the length of the audio source is shorter than the source video (i.e. 45 seconds), the audio plays from start to finish
    musicEnd=int(lgth)
    musicStart=0

elif lgth>45:
    # if it's longer than 45 seconds, it chooses a random endpoint after the 45 mark and sets the starting point as endpoint-45 seconds
    # this ensures "true" randomisation, since even if the same source audio is chosen, a different subclip of the audio is taken as the new audio
    musicEnd = rng.randint(45, int(lgth))
    musicStart=musicEnd-45
# this is pretty much the same thing, the Evangelion opening is around 1:20 long, and it takes a random 45 second subclip out of it
# you can play around with the number, if you desire shorter videos, whatsoever
originalOp.subclip(opDuration-45, opDuration).set_audio(bgmusic.subclip(musicStart, musicEnd)).write_videofile("output.mp4")

# the description is set to the URL of the source audio
desc = title
title = 'EVA'
vidfbpath = 'output.mp4'
source = open(vidfbpath, 'rb')
# these parameters will be used in a POST request to Facebook
meta = {'description': desc,
    'title': title,
    'source': vidfbpath,}
files = {'source': ('output.mp4', open('output.mp4', 'rb'), 'video/mp4')}
fburl = 'https://graph-video.facebook.com/v2.0/102083981342358/videos?access_token={0}'.format(page_access_token)
# and finally the request is sent, your video is uploaded
r = requests.post(fburl, data=meta, files=files)
