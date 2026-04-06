from flask import Blueprint, render_template, request
from main import analyzeData
import scraper.scrape_devpost_ as scrape
import auth
import json

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():
    results = None
    error = None

    if request.method == "POST":
        url = request.form.get("hackathon_url")
        try:
            driver = auth.login(url)
            profiles = scrape.scrapeParticipants(driver, url)
            all_data = scrape.scrapeData(profiles)
            driver.quit()

            print(f"all_data: {all_data}")  # ← check scraper output
            raw = analyzeData(all_data)
            print(f"raw from analyzeData: {raw}")  # ← check Groq output

            if raw is None:
                error = "Could not get a response from Groq, please try again"
            else:
                cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
                print(f"cleaned: {cleaned}")  # ← check cleaned output
                results = json.loads(cleaned)

        except Exception as e:
            print(f"Exception: {e}")
            error = str(e)

    return render_template("index.html", results=results, error=error)