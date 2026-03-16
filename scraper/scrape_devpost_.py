import requests
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import time
import json
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}  # defined once, reused everywhere

def scrapeParticipantCount(url):
    response = requests.get(url, headers=HEADERS)
    page = soup(response.text, "html.parser")

    # Find the link back to the hackathon page
    hackathon_link = page.find("a", href=re.compile(r"https://(?!help\.|www\.|api\.)[^/]+\.devpost\.com/$"))

    if hackathon_link:
        hackathon_url = hackathon_link.get("href")
        response2 = requests.get(hackathon_url, headers=HEADERS)
        page2 = soup(response2.text, "html.parser")
        tag = page2.find(string=re.compile(r"Participants \(\d+\)"))

        if tag:
            count = re.search(r"\d+", tag)
            return int(count.group()) if count else None

    print(f"Could not find hackathon link on {url}")
    return None

def scrapeParticipants(driver, url):
    purl = url.rstrip("/") + "/participants"

    page = 1
    all_profiles = set()

    while True:
        driver.get(f"{purl}?page={page}")
        time.sleep(3)

        profiles = driver.find_elements(By.CLASS_NAME, "user-profile-link")

        new_profiles = set()
        for p in profiles:
            new_profiles.add(p.get_attribute("href"))

        if new_profiles.issubset(all_profiles):
            break

        all_profiles.update(new_profiles)
        print(f"Page {page} — {len(all_profiles)} profiles so far")
        page += 1

    return all_profiles


def scrapeData(profiles):
    all_data = []

    for p in profiles:
        response = requests.get(p, headers=HEADERS)  # added headers
        page = soup(response.text, "html.parser")

        hackathon_entries = page.select("a.block-wrapper-link.fade.link-to-software")
        projects = 0
        wins = []

        for entry in hackathon_entries:
            projects += 1
            winner_img = entry.select_one("img.winner")

            if winner_img:
                wins.append({
                    "hackathon_url": entry.get("href"),
                })

        for win in wins:
            count = scrapeParticipantCount(win["hackathon_url"])
            win["participants"] = count
            time.sleep(1)

        profile = {
            "url": p,
            "projects": projects,
            "is_winner": len(wins) > 0,
            "win_count": len(wins),
            "wins": wins
        }

        print(profile)
        all_data.append(profile)
        time.sleep(1)

    return all_data