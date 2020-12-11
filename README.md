# Cruel Bot's Thesis-00 Prototype
This is the source code of https://www.facebook.com/cruelbotsthesis/

This is a hobby project from 2019, stemming from a personal interest in automated Facebook Bots and Neon Genesis Evangelion.
I have abandoned this project, because I got tired of getting copystriked about twenty times a day by SME and WB.


The way this bot works is the following:

- users can submit YouTube links to a database (initially, I used Google Forms)
- the bot takes a link at random from the database
- it downloads the YouTube video, extracts the audio (with the help of the wonderful youtube-dl https://github.com/ytdl-org/youtube-dl )
- takes a 45-second clip at random from the audio, and combines it with a 45-second clip of the Evangelion opening
- mixes them, and posts the resulting video to Facebook

As you can see, this bot is not very complex, but it was fun while it lasted.

The JSON files necessary for configuration only contain placeholder data, if you plan to use this silly project for whatever reason, modify them to your liking.
