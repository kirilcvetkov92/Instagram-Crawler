import re as regex

from selenium.common.exceptions import StaleElementReferenceException

import settings as config


class next_button_url_change(object):
    """
        Scheduler, Ticks till the page next button url is changed
    """
    def __init__(self, prev_url, right_arrow):
        self.prev_url = prev_url
        self.right_arrow = right_arrow


    def __call__(self, driver):

        try:
            new_link = self.right_arrow.get_attribute("href")
            if new_link!=self.prev_url: #and driver.current_url == self.prev_url:
                return True
            else :
                return False
        except StaleElementReferenceException as ex:
            return True


class num_of_pictures(object):
    """
        Scheduler, Ticks till page contains amount of pictures equal or greater than specified number
    """
    def __init__(self,number):
      self.number=number

    def __call__(self, driver):

        field = 'src="'
        custom_regex = field + '[ \w+-_/#]*.jpg'
        current_number = len(regex.findall(r'' + custom_regex, driver.page_source))

        if (current_number-1>=self.number):
            return True
        else :
            driver.execute_script(config.SCROLL_BOTTOM)
            return False

