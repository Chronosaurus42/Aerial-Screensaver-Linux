# Aerials Screensaver for Linux

Download or stream Aerials on selectable quality with xscreensaver. 

## Dependency
- mplayer
- python
- xscreensaver

## Download all Screensavers
Create a new folder to which you want to download the files and put the file `aerial_loader.py` there.

You can choose in which quality you want to download in `aerial_loader.py`
```sh
    video_quality={0: "url-1080-H264",
                    1: "url-1080-SDR",
                    2: "url-1080-HDR",
                    3: "url-4K-SDR",
                    4: "url-4K-HDR"}
    # used quality for download
    download_video_quality=3
    # used quality for stream
    stream_video_quality=1
```


## Configure xscreensaver
Copy files `aerials_screensaver_local` & `aerials_screensaver_streaming` into
`/usr/lib/xscreensaver` and make them executable (chmod +x). 


Set the path to directory in which you have executed `aerial_loader.py` in the files `aerials_screensaver_local` & `aerials_screensaver_streaming`.


Now you need to announce the new screensavers in `.xscreensaver` under `programs`
```sh
programs:                                     \
"AerialsScreensaver"  aerials_screensaver_local      \n\
"AerialsStream"       aerials_screensaver_streaming  \n\
```


You can also disable downloading video files in `aerial_loader.py` by setting `Download_Screensaver` to `False`.


## KDE
You need to start `ksmserver` with `--no-lockscreen`
it will else conflict with xscreensaver.

`mv /usr/bin/ksmserver /usr/bin/ksmserver-orig`

Create a new file `vim /usr/bin/ksmserver`
```sh
#!/bin/sh
ksmserver-orig --no-lockscreen
```

`chmod +x /usr/bin/ksmserver`

This 'fix' has to be repeated when ksmserver is updated.


## Knonw issues
- It is theoretically possible that in a multi monitor setup the screensavers become asynchronous, should be fixed the next time you run it.
- Xscreensaver seems to have a problem terminating mediaplayers other than mplayer. What leads to the situation that the playback processes remain active after closing the screensaver.
- When downloading, each video is first written fully to RAM before being written to disk. Note this in low RAM scenarios. 
