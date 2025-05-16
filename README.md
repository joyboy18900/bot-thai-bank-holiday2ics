# bot-thai-bank-holiday2ics

Python script for scraping Thai bank holidays from BOT (Bank of Thailand) and exporting them as `.ics` (iCalendar) file for iPhone, Google Calendar, etc.

## Features

- Scrape up-to-date Thai bank holidays directly from BOT website
- Export as standard `.ics` (iCalendar) for easy import to any calendar app
- No manual date entry, always fresh from the source
- Pre-generated `.ics` files available for download in the `output` folder

## Usage

### Option 1: Download Pre-Generated `.ics` File
You can directly download the latest `.ics` file from the `output` folder:
[Download Thai Bank Holidays `.ics`](./output)

### Option 2: Run the Script Locally
1. Clone this repo or download files:
    ```
    git clone <repo-url>
    cd bot-thai-bank-holiday2ics
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the script:
    ```
    python main.py
    ```

4. The generated `.ics` file will be saved in the `output` folder. Import this file into your iPhone, Google Calendar, or any calendar app that supports `.ics`.