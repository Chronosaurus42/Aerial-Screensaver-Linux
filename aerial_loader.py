#!/usr/bin/env python

import os
import json
import tarfile
import requests
from os import path
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning

Download_Screensaver = True

apple_resources_source = "https://sylvan.apple.com/Aerials/resources-15.tar"
resource_name = "Aerials.tar"
resource_json = "entries.json"
stream_url_file="Aerials_stream.url"



def update_check():
    if not path.isfile(resource_json):
        get_aerials_info()
    max_age = (datetime.utcnow() + timedelta(days=10))
    file_age = datetime.utcfromtimestamp(path.getmtime(resource_json))
    if file_age > max_age:
        get_aerials_info()

def get_aerials_info():
    r = requests.get(apple_resources_source, verify=False)
    with open(resource_name, 'wb') as infile:
        infile.write(r.content)

    #extract entries.json from archive
    archiv = tarfile.open(resource_name)
    archiv.extract(resource_json)
    archiv.close()

def download_aerials():
    if not Download_Screensaver:
        print('File download disabled')
    #Available quality
    video_quality={0: "url-1080-H264",
                    1: "url-1080-SDR",
                    2: "url-1080-HDR",
                    3: "url-4K-SDR",
                    4: "url-4K-HDR"}
    # used quality for download
    download_video_quality=3
    # used quality for stream
    stream_video_quality=1

    with open('entries.json', 'r') as feed:
        locations = set()
        categories = dict()
        streams = list()

        top = json.load(feed)

        # get locations
        for block in top["assets"]:
            label = block["accessibilityLabel"]
            locations.add(label)

        # get categories
        for block in top["categories"]:
            name = block["localizedNameKey"]
            _id = block["id"]
            categories[_id] = name.replace('AerialCategory','')

        for ort in locations:
            for block in top["assets"]:
                if ort == block["accessibilityLabel"]:
                    categorie = categories.get(block["categories"][0])
                    video_name = block[video_quality[download_video_quality]].split("/")[-1]
                    filename = f"{categorie}_-_{ort.replace(' ','_')}_-_{video_name}"
                    streams.append(block[video_quality[stream_video_quality]])

                    if Download_Screensaver:
                        #check if file already exists
                        if not path.isfile(filename):
                            # download file
                            print(f'Download file: location: {ort} - categorie: {categorie} name: {video_name} - URL: {block[video_quality[download_video_quality]]}')
                            r = requests.get(block[video_quality[download_video_quality]], verify=False)
                            with open(filename, 'wb') as video:
                                video.write(r.content)
                        else:
                            print(f'File already exists: {filename} -[skipping]-')
    # write download urls to file
    with open(stream_url_file, 'w') as video_urls:
        for stream in streams:
            video_urls.write(stream + "\n")

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    update_check()
    download_aerials()
