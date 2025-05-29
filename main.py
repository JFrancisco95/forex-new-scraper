from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY_PATH = "/usr/bin/chromium"

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    options.binary_location = CHROME_BINARY_PATH
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=options)

def fetch_high_impact_news():
    driver = create_driver()
    driver.get("https://www.forexfactory.com/calendar")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "calendar__table"))
        )
    except Exception as e:
        driver.quit()
        return f"Timeout or error waiting for calendar table: {e}"

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    table = soup.find("table", {"id": "calendar__table"})
    if not table:
        return "Could not find calendar table."

    rows = table.find_all("tr", class_="calendar__row")
    output = []

    for row in rows:
        impact = row.find("td", class_="calendar__impact")
        if not impact:
            continue
        impact_span = impact.find("span")
        if impact_span and "High" in impact_span.get("title", ""):
            date = row.find("td", class_="calendar__time").text.strip()
            currency = row.find("td", class_="calendar__currency").text.strip()
            event = row.find("td", class_="calendar__event").text.strip()
            output.append(f"{date} - {currency} - {event}")

    return "\n".join(output) or "No high-impact events found."

if __name__ == "__main__":
    print("=== High-Impact Forex Events ===")
    news = fetch_high_impact_news()
    print(news)
