"""Example of selenium"""
import traceback

import selenium
from selenium.webdriver.common.keys import Keys

driver = None
try:
    chrome_options = selenium.webdriver.chrome.options.Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    # chrome_options.add_argument("--enable-precise-memory-info")
    chrome_options.add_argument("--dump-histograms-on-exit")
    driver = selenium.webdriver.chrome.webdriver.WebDriver(
        executable_path="chromedriver",
        options=chrome_options,
        service_log_path="./selenium-server.log",
    )
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("getting started with python")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source

except Exception as exc:
    print(type(exc))
    print(traceback.format_exc())

finally:
    if driver:
        driver.close()
        driver.quit()
