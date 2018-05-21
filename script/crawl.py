import logging as log

import re as regex
from urllib.parse import urljoin

import schedulers as scheduler
from components import Page as PageComponent
from components import Post as PostComponent

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Page
from selenium.webdriver.support.ui import WebDriverWait as BrowserWait

import settings as config

log.basicConfig(filename='error.log')


class Crawler(object):
    """
        Class that will represent our crawler
    """

    def __init__(self, page_name=config.DEFAULT_PAGE_NAME, directory=config.DEFAULT_SAVE_DIR,
                 more_details=True, posts_number=config.DEFAULT_POST_NUMBER, export_db=True):
        # defailt data
        self.page_name = page_name
        self.directory = directory
        self.more_details = more_details
        self.posts_number = posts_number

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(0.1)
        self.export_db = export_db

    def run(self):
        """
            Main commands and methods
        """
        try:
            authenticated = False
            if (self.more_details):
                authenticated = self.authentication()

            self.crawl_general_page_info()

            self.basic_crawl()

            if authenticated:
                self.detailed_crawl()

            self.page.save()

            if self.export_db:
                print('Exporting to SQL....')
                conn = self.create_db_connection()
                self.page.export_to_sql(conn)
                self.close_db_connection(conn)
                print('Finished Exporting to SQL')

            self.terminate_browser()
        except Exception as ex:
            log.error("Unhandled Exception \n Closing browser.. \n Terminating process")
            log.error("{0} : {1}".format(type(ex), ex))
            print("Unhandled Exception \n Closing browser.. \n Terminating process")
            print("{0} : {1}".format(type(ex), ex))
            self.terminate_browser()

    def create_db_connection(self):
        import sqlite3
        try:
            conn = sqlite3.connect(config.DATABASE_PATH)
        except Exception as ex:
            print(ex)

        return conn

    def close_db_connection(self, conn):
        conn.commit()
        conn.close()

    def authentication(self):
        """
            Login : To see more details our crawler must have authentication
        """
        log.info("Attempting to login..")
        login_success = False

        try:
            authentication_url = urljoin(config.HOME_URL, config.LOGIN_URL)
            self.browser.get(authentication_url)

            has_auth_info = config.username and config.password

            if has_auth_info:

                # username field
                username_input_field = BrowserWait(self.browser, 5).until(
                    Page.presence_of_element_located((By.NAME, config.username_field_name))
                )
                # fill username
                username_input_field.send_keys(config.username)

                # fill password
                password_input_field = BrowserWait(self.browser, 5).until(
                    Page.presence_of_element_located((By.NAME, config.password_field_name))
                )
                password_input_field.send_keys(config.password)
                # Submit
                password_input_field.submit()
            else:
                raise IOError("There is no username and password provided")

            BrowserWait(self.browser, 60).until(
                Page.presence_of_element_located((By.CSS_SELECTOR, config.EXPLORE_URL))
            )

            log.info("Login successful")

            login_success = True

        except TimeoutException as ex:
            log.error("{0} : {1}".format(type(ex), ex))
            log.info("Login unsuccessful, switching to more details = False")
        except NoSuchElementException as ex:
            log.error("{0} : {1}".format(type(ex), ex))
            log.info("Login unsuccessful, switching to basic details mode")
        finally:
            return login_success

    def go_to_page(self, page):
        """Go to desired query page"""
        target_url = page.page_name
        if page.is_hash_tag():
            target_url = urljoin(config.HASH_TAG_URL, page.page_name.strip('#'))

        # get page url
        page_url = urljoin(config.HOME_URL, target_url)
        self.browser.get(page_url)

    def crawl_general_page_info(self):
        print("Get general page info for", self.page_name)
        log.info("Get general page info for", self.page_name)

        def get_instagram_field_number(expression):
            # Get instagram field from regular expression
            num_info = regex.search(expression,
                                    self.browser.page_source).group()
            field_number = int(regex.findall(r'\d+', num_info)[0])
            return field_number

        # create new page
        new_page = PageComponent(
            page_name=self.page_name,
            directory=self.directory
        )

        # go to page
        self.go_to_page(new_page)

        if not new_page.is_hash_tag():
            following = get_instagram_field_number(config.USER_FOLLOWING_REGEX)
            followers = get_instagram_field_number(config.USER_FOLLOWERS_REGEX)
            # update page info
            new_page.set_followers(followers)
            new_page.set_following(following)

        # Get total number of posts in page
        num_of_posts = get_instagram_field_number(config.USER_POST_COUNT_REGEX)
        # validate post number
        self.posts_number = min(self.posts_number, num_of_posts)
        new_page.set_posts(self.posts_number)

        # set current page attribute
        self.page = new_page
        print("Obtained general page info for", self.page_name)
        log.info("Obtained general page info for", self.page_name)

    def basic_crawl(self):

        def get_number_of_scrolls():
            """get the number of scroll-down in order to achieve desired number of picture"""
            images_per_scroll = config.IMAGES_PER_SCROLL
            times_to_scroll = (self.posts_number - images_per_scroll) // images_per_scroll + 1
            return times_to_scroll

        print("Get Basic crawl info for", self.page_name)
        log.info("Get Basic crawl info for", self.page_name)

        if (self.posts_number > config.IMAGES_PER_SCROLL):
            try:
                loadmore = BrowserWait(self.browser, 1)
                element = loadmore.until(
                    Page.presence_of_element_located(
                        (By.CSS_SELECTOR, config.LOAD_MORE_BUTTON))
                )
                element.click()
            except TimeoutException as ex:
                log.error("{0} : {1}".format(type(ex), ex.__traceback__))
                log.error("Couldn't find 'Load More' button")
                print("{0} : {1}".format(type(ex), ex.__traceback__))
                print("Couldn't find 'Load More' button")
                pass

            times_to_scroll = get_number_of_scrolls()

            BrowserWait(self.browser, times_to_scroll * 5).until(
                scheduler.num_of_pictures(self.posts_number)
            )

        field = 'src="'
        custom_regex = field + '[ \w+-_/#]*.jpg'
        image_links = regex.findall(r'' + custom_regex, self.browser.page_source)

        posts = [PostComponent(image_url=m[len(field):], id=inx)
                 for inx, m in enumerate(image_links, 0)]

        self.page.add_posts(posts)
        print("Obtained Basic crawl info for", self.page_name)
        log.info("Obtained Basic crawl info for", self.page_name)

    def detailed_crawl(self):
        log.info("Downloading more info")
        print("Downloading more info")

        post_num = 0
        while (post_num < self.posts_number):

            log.info("Download Page info for page ", post_num + 1, "/", self.posts_number)
            print("Download Page info for page ", post_num + 1, "/", self.posts_number)

            if post_num == 0:
                self.browser.find_element_by_xpath(
                    config.FIRST_POST_LINK).click()

                if self.posts_number>1:
                    BrowserWait(self.browser, 5).until(
                        Page.presence_of_element_located(
                            (By.CSS_SELECTOR, config.NEXT_PICTURE_BUTTON)
                        )
                    )
                    right_arrow = self.browser.find_element_by_css_selector(config.NEXT_PICTURE_BUTTON)
                    self.url_before = right_arrow.get_attribute("href")

            else:
                try:
                    right_arrow = self.browser.find_element_by_css_selector(config.NEXT_PICTURE_BUTTON)
                    right_arrow.click()
                    BrowserWait(self.browser, 10).until(
                        scheduler.next_button_url_change(self.url_before, right_arrow))
                    if post_num < self.posts_number - 1:
                        self.url_before = right_arrow.get_attribute("href")
                except TimeoutException:
                    log.error("Time out in post number {}".format(post_num + 1))
                    print("Time out in post number {}".format(post_num + 1))
                    continue
                except NoSuchElementException:
                    log.error("CSS selector no such element : url_before")
                    print("CSS selector no such element : url_before")
                    continue
                except StaleElementReferenceException:
                    print("Element reference exception")
                    continue

            # Parse caption
            post = self.page.get_page(post_num)

            try:
                time_element = BrowserWait(self.browser, 10).until(
                    Page.presence_of_element_located((By.TAG_NAME, config.TIME_ATTR))
                )

                try:
                    like_element = BrowserWait(self.browser, 0.1).until(
                        Page.presence_of_element_located((By.CSS_SELECTOR, config.LIKES_INFO))
                    )

                    post.likes = int(like_element.text[:-5].replace(',', ''))

                except TimeoutException as ex:
                    print("Unable to locate like tag")
                    log.error(ex)

                post.time = time_element.get_attribute(config.DATE_TIME_ATTR)

                caption = time_element.find_element_by_xpath(
                    config.TIME_DATE_PATH).text
                post.caption = caption

            except NoSuchElementException as ex:  # Forbidden
                print("Unable to locate caption")
                log.error(ex)

            except TimeoutException as ex:
                print("Timeout-" + ex)
                log.error(ex)
            except Exception as ex:
                print(ex)
                log.error(ex)
            post_num += 1

        log.info("Finished post crawling")

    def terminate_browser(self):
        """Quit browser"""
        self.browser.quit()
        log.info("Final Message : Browser is terminated")
        print("Final Message : Browser is terminated")


def main():
    import argparse as parser
    try:
        args = parser.ArgumentParser(description='Crawler arguments')

        args.add_argument('-db', '--export_db', action='store_true',
                          help='Export to db')

        args.add_argument('-dir', '--directory', type=str,
                          default=config.DEFAULT_SAVE_DIR, help='directory to save users')
        args.add_argument('-page', '--page_name', type=str, default=config.DEFAULT_PAGE_NAME,
                          help="# for hashtag")
        args.add_argument('-more', '--more_details', action='store_true',
                          help='Login required, Add this flag to download followers, follows, number of photo likes, photo date')
        args.add_argument('-num', '--photo_number', type=int, default=config.DEFAULT_POST_NUMBER,
                          help='Number of photos to download')

        parsed_arg = args.parse_args()

        export_db = parsed_arg.export_db

        crawler = Crawler(directory=parsed_arg.directory,
                          page_name=parsed_arg.page_name,
                          more_details=parsed_arg.more_details,
                          posts_number=parsed_arg.photo_number,
                          export_db=export_db)

    except AttributeError:
        crawler = Crawler()

    crawler.run()


if __name__ == "__main__":
    main()
