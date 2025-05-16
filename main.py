import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from ics import Calendar, Event
from ics.grammar.parse import ContentLine

# Helper function to map Thai months to English
def map_thai_month_to_english():
    return {
        'มกราคม': 'January', 'กุมภาพันธ์': 'February', 'มีนาคม': 'March', 'เมษายน': 'April',
        'พฤษภาคม': 'May', 'มิถุนายน': 'June', 'กรกฎาคม': 'July', 'สิงหาคม': 'August',
        'กันยายน': 'September', 'ตุลาคม': 'October', 'พฤศจิกายน': 'November', 'ธันวาคม': 'December'
    }

# Scrape holiday data from the Bank of Thailand website
def get_bot_holidays_with_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.bot.or.th/th/financial-institutions-holiday.html")

        # Handle cookie pop-up
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recommended-cookies-button"))
            ).click()
        except Exception:
            pass  # Ignore if no cookie pop-up

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        holidays = []
        month_mapping = map_thai_month_to_english()

        for month_group in soup.select(".holiday-group"):
            month_name = month_group.select_one(".month-title h3")
            if not month_name:
                continue

            month_english = month_mapping.get(month_name.text.strip(), None)
            if not month_english:
                continue

            for item in month_group.select(".month-holiday-item"):
                try:
                    date_text = item.select_one(".item-desc h3:nth-child(1)")
                    holiday_name = item.select_one(".item-desc h3:nth-child(2)")

                    if not date_text or not holiday_name:
                        continue

                    day = int(date_text.text.split()[1])
                    current_year = datetime.now().year
                    holiday_date = datetime(current_year, list(month_mapping.values()).index(month_english) + 1, day)

                    holidays.append({
                        'date': holiday_date,
                        'name': holiday_name.text.strip(),
                        'description': f"Holiday observed on {holiday_date.strftime('%d %B %Y')}.",
                        'location': "Thailand"
                    })
                except Exception:
                    continue

        return holidays

    finally:
        driver.quit()

# Create an .ics file from the holiday data
def create_ics_file(holidays, project_name="thai_bank_holidays"):
    valid_holidays = [h for h in holidays if h['date'] is not None]
    if not valid_holidays:
        print("No valid holidays to write.")
        return

    year = valid_holidays[0]['date'].year
    filename = f"{project_name}_{year}.ics"
    output_dir = "output"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    calendar = Calendar()
    calendar.extra.append(ContentLine(name="X-WR-CALNAME", value=f"Thailand Holidays {year}"))
    calendar.extra.append(ContentLine(name="X-WR-CALDESC", value="Official holidays in Thailand."))
    calendar.extra.append(ContentLine(name="X-WR-TIMEZONE", value="Asia/Bangkok"))

    for holiday in valid_holidays:
        event = Event()
        event.name = holiday['name']
        event.begin = holiday['date'].strftime('%Y-%m-%d')
        event.make_all_day()
        event.description = holiday['description']
        event.location = holiday['location']
        event.uid = f"{holiday['date'].strftime('%Y%m%d')}-{holiday['name']}"
        calendar.events.add(event)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(calendar)
    print(f"File {filepath} created successfully.")

# Main function to scrape holidays and generate .ics file
def main():
    holidays = get_bot_holidays_with_selenium()
    if holidays:
        create_ics_file(holidays)
    else:
        print("No holidays found.")

if __name__ == "__main__":
    main()