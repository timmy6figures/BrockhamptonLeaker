from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import os
from selenium.webdriver.common.keys import Keys


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def download_file_list(filepath):
    print("Downloading list of files to " + filepath)


def download_file(link):
    linkArray = str(link).split("/")

    if (linkArray[0] != "https:"):
        print("This may not be a link")
        return 0
    if (linkArray[2] != "onlyfiles.io"):
        print("This is not an onlyfiles link.")
        return 0

    page_content = requests.get(link).content
    pagesoup = BeautifulSoup(page_content, "html.parser")

    siblings_of_play_button = pagesoup.find("div", id="playpause").fetchNextSiblings()

    for sibling_of_play_button in siblings_of_play_button:
        # The second element of this split will be class="____"
        sibling_text_array = str(sibling_of_play_button).split(" ")
        # print(sibling_text_array)
        if sibling_text_array[1].split("=")[1] == "\"download\"":
            text_to_match = sibling_text_array[2]
            # print(text_to_match)
            regex = "(?<=downloadURI\()(.*)(?=,)"
            download_link = re.search(regex, text_to_match).group(0).lstrip("'").rstrip("'")
            print(download_link)
            downloaded_filename = download_link.split('/')[-1]
            file = requests.get("https://onlyfiles.io" + download_link)
            open("DownloadedFiles/" + downloaded_filename, "wb").write(file.content)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # download_file_list("files_to_download.txt")
    file_of_links = "links_to_download.txt"
    filestring = open(file_of_links, 'r').read()
    print(filestring)
    filestring_array = filestring.split("\n")
    for file in filestring_array:
        download_file(file)
