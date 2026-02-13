import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

def scrapeParticipants(driver, url):
    purl = url.rstrip("/")+"/participants"

    page = 1
    all_profiles = set()

    while True:
        driver.get(f"{purl}?page={page}")
        time.sleep(3)

        profiles = driver.find_elements(By.CLASS_NAME, "user-profile-link")

        if not profiles:
            break


        for p in profiles:
            all_profiles.add(p.get_attribute("href"))

        page += 1

        return all_profiles
    

