import re
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_parsed_mentions(raw_text):
    regex = re.compile(r"@([\w\.]+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)


def get_parsed_hashtags(raw_text):
    regex = re.compile(r"#(\w+)")
    regex.findall(raw_text)
    return regex.findall(raw_text)


def fetch_datetime(browser, dict_post):
    time_ele = browser.driver.find_element(By.CSS_SELECTOR, "time[class='_aaqe']")
    datetime = time_ele.get_attribute("datetime")

    dict_post["datetime"] = datetime

def fetch_comments(browser, dict_post):
    # click comment plus button
    while True:
        try:
            comment_plus_btns = browser.find_one(
                'ul._a9z6._a9za > li > div > button')
            comment_plus_btns.send_keys(Keys.ENTER)
            sleep(1)
        except:
            break

    '''
    View all replies inside a comments
    '''
    buttons = browser.find('ul._a9yo > li > div > button')
    print(f"[INFO] Number of Hidden Replies Found and Accessed: {len(buttons)}")

    for button in buttons:
        try:
            button_stat = browser.find_one("span._a9yi", button)
            if button_stat.text != "Hide replies" or button_stat.text != "View replies":
                button.send_keys(Keys.ENTER)
                sleep(0.3)
        except:
            pass
    

    sleep(0.3)
    ele_comments = browser.find("._a9zm")

    comments = []
    hashtags = []
    for els_comment in ele_comments[1:] :

        author = browser.find_one("h3._a9zc a", els_comment).text

        try:
            comment = browser.find_one("._a9zs > span", els_comment).text
        except:
            '''
            UNCOMMENT IF WANTED TO GET THE COMMENT MEDIA SOURCE
            
            comment = browser.find_one("div._a9zo div._a9zr img", els_comment)
            comment = comment.get_attribute("src")
            '''
            comment = "[GIF | Image]"


        comment_dtele = browser.find_one("div.x9f619 > span > a > time", els_comment)
        comment_dt = comment_dtele.get_attribute("datetime")


        comment_obj = {"author": author, "comment": comment, "date_time": comment_dt}
        
        pattern = '#([0-9a-zA-Z가-힣 u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"  u"\U0001F680-\U0001F6FF"  u"\U0001F1E0-\U0001F1FF"]*)'
        hash_w = re.compile(pattern)
        hashtag = hash_w.findall(comment)

        comments.append(comment_obj)
        hashtags += hashtag

    if comments:
        dict_post["comments"] = comments

    if ("hashtags" not in dict_post):
        dict_post["hashtags"] = hashtags
    elif ("hashtags" in dict_post):
        dict_post["hashtags"] = dict_post["hashtags"] + hashtags

def fetch_initial_comment(browser, dict_post):
    try:
        description = browser.driver.find_element(By.CSS_SELECTOR, 'div._a9zs h1._aacl')
        # first_post_elem = browser.find_one("div._a9zr > div._a9zs")
        # description = browser.find("h1", first_post_elem)#._aacl._aaco._aacu._aacx._aad7._aade", first_post_elem)
    except: 
        description = None

    if description is not None:
        dict_post["description"] = description.text
    else:
        pass

def fetch_details(browser, dict_post):
    username = browser.find_one('h2._a9zc a') 

    if username:
        dict_post["username"] = username.text
    fetch_initial_comment(browser, dict_post)
    fetch_datetime(browser, dict_post)
 
