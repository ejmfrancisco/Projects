from __future__ import unicode_literals

import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from browser import Browser
from fetch import fetch_comments, fetch_datetime, fetch_details
from utils import instagram_int, retry


class SecretSetting:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# secret = SecretSetting("dde_1025", "dderocks1!")
secret = SecretSetting("dde_ins", "dderocks1!")
# secret = SecretSetting("dde_igtest", "ddercoks2023!")

class InsCrawler():
    URL = "https://www.instagram.com"
    RETRY_LIMIT = 10

    def __init__(self, has_screen=False):
        super(InsCrawler, self).__init__()
        self.browser = Browser(has_screen)
        self.page_height = 0
        self.login()

    def _dismiss_login_prompt(self):
        ele_login = self.browser.find_one(".Ls00D .Szr5J")
        if ele_login:
            ele_login.click()

    def login(self):
        browser = self.browser
        url = f"{InsCrawler.URL}/accounts/login/"
        browser.get(url)
        u_input = browser.find_one('input[name="username"]')
        u_input.send_keys(secret.username)
        p_input = browser.find_one('input[name="password"]')
        p_input.send_keys(secret.password)
        
        login_btn = browser.find_one('button[class="_acan _acap _acas _aj1-"]')
        login_btn.click()

        @retry()
        def check_login():
            if browser.find_one('input[name="username"]'):
                raise Exception()

        check_login()

    def parse_numeric_string(self, s):
        # Remove any non-numeric characters (e.g., 'K' or ',')
        s = s.replace(',', '').replace('K', '').replace('M','')
        
        try:
            return str(float(s))
        except ValueError:
            return None

    def get_user_profile(self, username):
        browser = self.browser
        print(browser)
        url = "%s/%s/" % (InsCrawler.URL, username)
        browser.get(url)

        wait = WebDriverWait(browser.driver, 30)
    
        name = browser.find_one("div._aa_y div span.x18hxmgj")
        desc = browser.find_one("div._aa_y div h1")
        photo = browser.find_one("div._aa_y header img")  
        statistics = browser.driver.find_elements(By.CSS_SELECTOR, "li span._ac2a span")
        post_num, follower_num, following_num = [self.parse_numeric_string(element.text) for element in statistics]
        
        profile_Desc = {
            "name": name.text,
            "desc": desc.text if desc else None, 
            "photo_url": photo.get_attribute("src") if photo else None,
            "post_num": post_num,
            "follower_num": follower_num,
            "following_num": following_num,
        }
        return profile_Desc
    
    def get_user_posts(self, username, number=None, detail=False):
        user_profile = self.get_user_profile(username)
        if not number:
            number = instagram_int(user_profile["post_num"])

        self._dismiss_login_prompt()

        return self._get_posts(number)

    def _get_posts(self, num):
        """
            To get posts, we have to click on the load more
            button and make the browser call post api.
        """
        TIMEOUT = 600
        browser = self.browser
        key_set = set()
        posts = []
        pre_post_num = 0
        wait_time = 1

        def start_fetching(pre_post_num, wait_time):
            ele_posts = browser.find("._aabd a")
                    
            for ele in ele_posts:
                key = ele.get_attribute("href")
                if key not in key_set:
                    dict_post = { "key": key }
                    ele_img = browser.find_one("div._aagv img", ele)
                    dict_post["caption"] = ele_img.get_attribute("alt")
                    dict_post["img_url"] = ele_img.get_attribute("src")
                
                    main_post = browser.find_one("div._aagu", ele)
                    main_post.click()

                    fetch_details(browser, dict_post)   # description, datetime 포함 ----> fetch_caption, fetch_datetime
                    fetch_comments(browser, dict_post)

                    close_button = browser.find_one('svg[aria-label="Close"]')
                    close_button.click()

                    key_set.add(key)
                    posts.append(dict_post)
                    print(posts)

                    if len(posts) == num:
                        break

                time.sleep(0.3)
            if pre_post_num == len(posts):
                sleep(wait_time)

                wait_time *= 2
                browser.scroll_up(300)
            else:
                wait_time = 1

            pre_post_num = len(posts)
            browser.scroll_down()

            return pre_post_num, wait_time, posts

        while len(posts) < num and wait_time < TIMEOUT:
            post_num, wait_time, posts = start_fetching(pre_post_num, wait_time)
            pre_post_num = post_num

            loading = browser.find_one(".W1Bne")
            if not loading and wait_time > TIMEOUT / 2:
                break
        
        print("Done. Fetched %s posts." % (min(len(posts), num)))
        return posts[:num]
