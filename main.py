### Comic Downloader ###
### Craig Cuninghame ###
### Takes list of RSS feeds and downloads the first image from each feed ###

import datetime
import os
import sys
import feedparser
from bs4 import BeautifulSoup
import requests


def create_folder(comic_folder_path):
    ### Creates a folder with Today's date ###
    try:
        os.mkdir(comic_folder_path)
    except Exception as e:
        print("Creation of the directory %s failed" % comic_folder_path)
        print(e)
        sys.exit()
    else:
        print("Successfully created the directory %s " % comic_folder_path)
    return


def download_link_from_rss(feed_link):
    feed_obj = feedparser.parse(feed_link)
    try:
        comic_title = feed_obj.feed.title
    except:
        comic_title = "No title found"
    try:
        image_title = feed_obj.entries[0].title
    except:
        image_title = "No image title found"
    soup = BeautifulSoup(str(feed_obj), "html.parser")
    image_link = soup.find("img")
    try:
        alternate_title = image_link['title']
    except:
        alternate_title = "No title found"
    image_link = image_link['src']
    return image_link, image_title, comic_title, alternate_title


def download_picture_from_link(image_link):
    ### Downloads picture from the link provided ###
    try:
        image_request = requests.get(image_link)
        return image_request
    except Exception as e:
        print("This has failed:")
        print(e)



def main():
    current_date = str(datetime.date.today())
    comic_folder_path = "Comics" + "/" + current_date
    create_folder(comic_folder_path)
    with open("rss_feed_list.txt", "r") as feed_list:
        for feed_link in feed_list:
            try:
                print(feed_link)
                image_link, image_title, comic_title, alternate_title = download_link_from_rss(feed_link)
                print(f"Comic Title = {comic_title}")
                print(f"Alternate Title = {alternate_title}")
                print(f"Image Link = {image_link}")
                print(f"Title = {image_title}")
                with open('previously_downloaded.txt', "r+") as previously_downloaded:
                    if image_link in previously_downloaded.read():
                        print("This has already been downloaded")
                    else:
                        image = download_picture_from_link(image_link)
                        with open(f'{comic_folder_path}/{comic_title}.jpg', 'wb') as f:
                            f.write(image.content)
                            previously_downloaded.write(f"{image_link}\n")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()


