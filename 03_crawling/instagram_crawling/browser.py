import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from utils import randmized_sleep

from selenium.webdriver.chrome.service import Service

class Browser:
    def __init__(self, has_debug):
        '''
        This code is working with conda environment "lambda_insta" python version 3.8 with latest sel.
        No need to pass binary for chrome and executable path for driver.
        1. Uncomment fake_useragent
        2. Add driver path if needed for binary testing if not leave the binary_location commented as well.
        '''
        # chrome_options = webdriver.ChromeOptions()
        # ua = UserAgent()
        # user_agent = ua.random

        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--ignore-ssl-errors=true")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # # chrome_options.add_argument("user-agent="+UserAgent().random)
        # chrome_options.add_argument(f"user-agent={user_agent}")
        # # chrome_options.binary_location = "/Users/emfc/Downloads/chromedriver-setups/chromedriver-86/headless-chromium"

        # self.driver = webdriver.Chrome(options=chrome_options)

        '''
        Testing Phase
        '''
        # chrome_options = Options()
        # # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--window-size=1920x1080')
        # chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        # chrome_options.add_argument('--hide-scrollbars')
        # chrome_options.add_argument('--enable-logging')
        # chrome_options.add_argument('--log-level=0')
        # chrome_options.add_argument('--v=99')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument('--data-path=/tmp/data-path')
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--homedir=/tmp')
        # chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        # chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        # # chrome_options.binary_location = "/Users/emfc/Downloads/chromedriver-setups/chromedriver-237/headless-chromium"
        
        # self.driver = webdriver.Chrome(options=chrome_options)
        ua = UserAgent()
        user_agent = ua.random
        # chrome_options = webdriver.ChromeOptions()
       

        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('--disable-gpu')
        
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument("--ignore-ssl-errors=true")
        # # chrome_options.add_argument("user-agent="+UserAgent().random)
        # chrome_options.add_argument(f"user-agent={user_agent}")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox")
         # chrome_options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(options=chrome_options)
        # chrome_options.binary_location = "/Users/emfc/Downloads/instagram_dep/chromedriver-setups/chromedriver-86/headless-chromium"
        # self.driver = webdriver.Chrome('/Users/emfc/Downloads/instagram_dep/chromedriver-setups/chromedriver-114/chromedriver-mac64',options=chrome_options)

        self.driver.implicitly_wait(5)

    @property
    def page_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def get(self, url):
        self.driver.get(url)

    @property
    def current_url(self):
        return self.driver.current_url

    def implicitly_wait(self, t):
        self.driver.implicitly_wait(t)

    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        try:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def scroll_down(self, wait=0.3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.driver.execute_script("window.scrollTo(0, 0)")
        else:
            self.driver.execute_script("window.scrollBy(0, -%s)" % offset)
        randmized_sleep(wait)

    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def open_new_tab(self, url):
        self.driver.execute_script("window.open('%s');" %url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_current_tab(self):
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
