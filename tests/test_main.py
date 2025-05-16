import unittest
from unittest.mock import patch, MagicMock
from main import get_bot_holidays_with_selenium

class TestHolidayScraper(unittest.TestCase):
    @patch("main.webdriver.Chrome")
    def test_parse_valid_holiday_data(self, mock_webdriver):
        """Test parsing valid holiday data."""
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <div class="holiday-group">
            <div class="month-title"><h3>มกราคม</h3></div>
            <div class="month-holiday-item">
                <div class="item-desc">
                    <h3>วันพุธ 1</h3>
                    <h3>วันขึ้นปีใหม่</h3>
                </div>
            </div>
        </div>
        """
        holidays = get_bot_holidays_with_selenium()
        self.assertEqual(len(holidays), 1)
        self.assertEqual(holidays[0]['name'], "วันขึ้นปีใหม่")
        self.assertEqual(holidays[0]['date'].strftime('%Y-%m-%d'), "2025-01-01")
        self.assertEqual(holidays[0]['location'], "Thailand")

    @patch("main.webdriver.Chrome")
    def test_handle_missing_holiday_data(self, mock_webdriver):
        """Test handling missing holiday data."""
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <div class="holiday-group">
            <div class="month-title"><h3>มกราคม</h3></div>
            <div class="month-holiday-item">
                <div class="item-desc">
                    <h3>วันพุธ 1</h3>
                </div>
            </div>
        </div>
        """
        holidays = get_bot_holidays_with_selenium()
        self.assertEqual(len(holidays), 0)

    @patch("main.webdriver.Chrome")
    def test_handle_empty_page_source(self, mock_webdriver):
        """Test handling empty page source."""
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = ""
        holidays = get_bot_holidays_with_selenium()
        self.assertEqual(len(holidays), 0)

    @patch("main.webdriver.Chrome")
    def test_skip_invalid_month_name(self, mock_webdriver):
        """Test skipping invalid month names."""
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <div class="holiday-group">
            <div class="month-title"><h3>InvalidMonth</h3></div>
            <div class="month-holiday-item">
                <div class="item-desc">
                    <h3>วันพุธ 1</h3>
                    <h3>วันขึ้นปีใหม่</h3>
                </div>
            </div>
        </div>
        """
        holidays = get_bot_holidays_with_selenium()
        self.assertEqual(len(holidays), 0)

    @patch("main.webdriver.Chrome")
    def test_handle_no_holiday_groups(self, mock_webdriver):
        """Test handling no holiday groups."""
        mock_driver = MagicMock()
        mock_webdriver.return_value = mock_driver
        mock_driver.page_source = """
        <div class="no-holidays"></div>
        """
        holidays = get_bot_holidays_with_selenium()
        self.assertEqual(len(holidays), 0)

if __name__ == "__main__":
    unittest.main()