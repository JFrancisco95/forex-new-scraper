import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0 Safari/537.36")
    driver = uc.Chrome(version_main=136, options=options)  # force driver for Chrome 136
    return driver

def fetch_high_impact_news():
    driver = create_driver()
    driver.get("https://www.forexfactory.com/calendar")

    try:
        # Wait up to 15 seconds for the calendar table to appear
        WebDriverWait(driver, 15).until(
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
        impact_td = row.find("td", class_="calendar__impact")
        if not impact_td:
            continue
        impact_span = impact_td.find("span")
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
