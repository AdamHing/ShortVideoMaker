from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome  import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def heatmap(url):
    driver.get(url)
    driver.maximize_window()
    # time.sleep(5)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    mydivs = soup.find("path", {"class": "ytp-heat-map-path"}).get('d')
    return mydivs

#//*[@id="21"]/path
#//*[@id="5"]/path
#/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[37]/div[1]/div[1]/div[2]/svg/defs/clipPath/path
#/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[35]/div[1]/div[1]/div[2]/svg/defs/clipPath/path


#https://www.youtube.com/watch?v=J3-m7dAL_cY
url = "https://www.youtube.com/watch?v=J3-m7dAL_cY"
print(heatmap(url))