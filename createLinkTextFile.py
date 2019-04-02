from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_extension('./Driver/extension_0_9_5_12.crx')
browser = webdriver.Chrome(executable_path='./Driver/chromedriver.exe', chrome_options=chrome_options)

browser.get("https://www.readlightnovel.org/novel-list")

elemContainer = browser.find_element_by_class_name('content')

links = elemContainer.find_elements_by_xpath('//a[contains(@href,"readlightnovel")]')

# print(links)

with open("theLinks.txt", "w", encoding="utf8") as f:
    for link in links:
        f.writelines('{} \n'.format(link.get_attribute("href")))
            
browser.quit()
