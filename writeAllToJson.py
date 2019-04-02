from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from SapiHelper import Sapi
import os
import re
from multiprocessing import Process, current_process


def getAllChapterLinks(link, browser):
    browser.get(link)
    try:
        chapterContainers = browser.find_elements_by_class_name('chapter-chs')
        
        chapterElems = []
        for chapterContainer in chapterContainers:
            for chapterElem in chapterContainer.find_elements_by_tag_name('a'):
                chapterElems.append(chapterElem)

        chapterLinks = [chapterElem.get_attribute("href") for chapterElem in chapterElems]
        
        novelInfo = {
            "Name": browser.find_element_by_class_name('block-title').text,
            "Link": link,
            "Rating": browser.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div/div[6]/div[2]").text,
            "Chapters":[]
        }
        i = 0
        for chapterLink in chapterLinks:
            i+=1
            # print('{}/{} Chapters for this Novel Completed'.format(i, len(chapterLinks)))
            novelInfo["Chapters"].append({
                "chapterNumber": i,
                "chapterLink": chapterLink
                # "chapterText": getChapterTexts(chapterLink, browser)
            })
            # novelInfo["Chapters"]["chapterLink"] = chapterLink
            # novelInfo["Chapters"]["chapterText"] = getChapterTexts(chapterLink, browser)
    except:
        novelInfo = {}


    return novelInfo


def getChapterTexts(link, browser):
    browser.get(link)
    try:
        chapterText = browser.find_element_by_class_name("desc").text
        return chapterText
    except:
        chapterText = "Didnt work bro"
        return chapterText

def getNovelLinks():
    with open("theLinks.txt", "r", encoding="utf8") as f:
        links = [line[:-2] for line in f.readlines()]
    return links

def readNovelJson():
    with open('novels.json', 'r') as f:
        novelJson = json.load(f)
    return novelJson


def writeNewJson(browser):

    links = getNovelLinks()

    novelJson = {
        "Novels": []
    }
    i = 0
    for link in links:
        i+=1
        print('{}/{} Novels Completed!'.format(i, len(links)))
        try:
            novelJson["Novels"].append(getAllChapterLinks(link, browser))
            with open("novels.json", "w") as f:
                json.dump(novelJson, f)
        except:
            pass
        
        # print(novelJson)

def getChapterLinksforCompare():
    chapterList = []
    for novel in readNovelJson()["Novels"]:
        for chapter in novel["Chapters"]:
            chapterList.append(chapter["chapterLink"])
    return chapterList

def updateJson():
    links = getNovelLinks()
    novelJson = readNovelJson()
    chapterList = getChapterLinksforCompare()

    for link in links:
        for chapter in chapterList:
            if link in chapter:
                links.remove(link)
                break
    return links

    





if __name__ == '__main__':
    searchTerm = input("Enter Novel Name: ")
    novelJson = readNovelJson()



    chrome_options = Options()
    chrome_options.add_extension('./Driver/extension_0_9_5_12.crx')
    browser = webdriver.Chrome(executable_path='./Driver/chromedriver.exe', chrome_options=chrome_options)
    # writeNewJson(browser)
    speaker = Sapi()
    speaker.set_rate(2)
    voices = speaker.get_voices()
    speaker.set_voice(voices[1])


    for novel in novelJson["Novels"]:
        if 'Name' in novel:
            if novel["Name"] == searchTerm:
                newPath = r"Novels\{}".format(novel["Name"].replace("?", ''))
                if not os.path.exists(newPath):
                    os.makedirs(newPath)
                for chapter in novel["Chapters"]:
                    if not os.path.isfile(newPath + f"\{chapter['chapterNumber']:05d}.mp3"):
                        chapterText = getChapterTexts(chapter['chapterLink'], browser)
                        speaker.create_recording(newPath + f"\{chapter['chapterNumber']:05d}.mp3", re.sub(r'Chapter \w+', r'', chapterText))
                        print(f"Chapter {chapter['chapterNumber']}/{len(novel['Chapters'])} finished")


    browser.quit()






    # chapterContainers = chain.from_iterable(chapterContainers)
    # chapters = [chapter for chapter in chapterContainers]
    