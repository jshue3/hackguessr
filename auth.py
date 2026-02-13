from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv("authCred.env")

user = os.getenv("DEVPOSTEMAIL")
password = os.getenv("DEVPOSTPW")

def login(url):
    driver = webdriver.Chrome()
    purl = url.rstrip("/")+"/users/login"
    driver.get(purl)

    driver.find_element("id", "user_email").send_keys(user)
    driver.find_element("id", "user_password").send_keys(password)

    driver.find_element("id", "submit-form").click()


    return driver
