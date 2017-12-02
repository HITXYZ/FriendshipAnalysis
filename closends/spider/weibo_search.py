"""
    @author: Jiale Xu
    @date: 2017/11/11
    @desc: Search weibo users and get html
"""

import os
from urllib.request import quote
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from closends.spider.base_exceptions import MethodParamError
from closends.spider.base_configs import weibo_search_url

driver = webdriver.PhantomJS(executable_path='phantomjs', service_log_path=os.path.devnull)


def get_user_by_account(user=None, number=1):
    if not isinstance(user, str):
        raise MethodParamError('Parameter \'user\' must be an instance of \'str\'!')
    if not isinstance(number, int):
        raise MethodParamError('Parameter \'number\' must be an instance of \'int\'!')
    if number <= 0:
        number = 1
    wait = WebDriverWait(driver, 3)
    driver.get(weibo_search_url.format(user=quote(user)))
    try:
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'pl_personlist')))
        user_divs = driver.find_elements_by_class_name('list_person')
    except TimeoutException:  # 未找到结果或网速太慢
        return [], []
    except NoSuchElementException:  # 未找到结果
        return [], []
    if len(user_divs) >= number:  # 截取前number个搜索结果
        user_divs = user_divs[:number]
    user_ids = []
    user_htmls = []
    for user_div in user_divs:
        user_id = user_div.find_element_by_class_name('person_name').find_element_by_tag_name('a').get_attribute('uid')
        user_ids.append(int(user_id))
        user_htmls.append(user_div.get_attribute('outerHTML'))
    return user_ids, user_htmls


def get_user_by_homepage(url):
    if not isinstance(url, str):
        raise MethodParamError('Parameter \'url\' must be an instance of \'str\'!')
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'username')))
    except TimeoutException:  # 网速太慢或链接错误
        return [], []
    username = driver.find_element_by_class_name('username').text
    user_ids, user_htmls = get_user_by_account(user=username, number=1)
    if len(user_ids) > 0 and len(user_htmls) > 0:
        return user_ids[0], user_htmls[0]
    return [], []


if __name__ == '__main__':
    # _, html = get_user_by_account("理想三旬XU")
    _, html = get_user_by_homepage("https://weibo.com/u/1749224837?refer_flag=1005055013_&is_all=1")
    print(html)
