#!/usr/bin/env bash


key=$1
value=$2
yt_url="https://www.youtube.com"

cd ./downloads

if [[ $key == "video_id" ]]; then
  youtube-dl -f mp4 --download-archive ids.txt "$yt_url/watch?v=$value"
elif [[ $key == "playlist_id" ]]; then
  youtube-dl -f mp4 --download-archive ids.txt "$yt_url/playlist?list=$value"
elif [[ $key == "video_title" ]]; then
  youtube-dl -f mp4 --download-archive ids.txt "ytsearch:$value"
fi