import auth
import scraper.scrape_devpost_ as scrape
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as soup
import re


url = input("Enter hackathon URL: ")


driver = auth.login(url)
profiles = scrape.scrapeParticipants(driver, url)
scrape.scrapeData(profiles)


