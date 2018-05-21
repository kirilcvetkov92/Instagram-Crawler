""" Settings that keeps pattners which the crawler will search for, in order to make an action"""
"""Authentication info"""
username = "kiril_cvetkov"
password = "********"

""" MAIN SETTINGS """

#directory where
DEFAULT_SAVE_DIR = "../pages"
DEFAULT_PAGE_NAME = "kiril_cvetkov"
DEFAULT_POST_NUMBER = 15
#the home webpage
HOME_URL = 'http://www.instagram.com'

# CSS template for "Next" button used to navigate through user's pictures
NEXT_PICTURE_BUTTON = "a[class='_3a693 coreSpriteRightPaginationArrow']"

# CSS template for "Load More" button used to load more picture for specified user inside his wall
LOAD_MORE_BUTTON = "a._1cr2e._epyes"

# CSS template used to obtain the link of the user's first post
FIRST_POST_LINK = "//div[@class='_mck9w _gvoze _f2mse']"

# CSS template for "Time-Date" labes used to obtain the upload date of the user's post
TIME_DATE_PATH = "../../../div/ul/li/span"

# CSS template for "Image-url" field used to obtain the image url of specified uer's post
POST_IMAGE_URL = "div[class='_sxolz']"

#url that appears inside each user profile when the crawler-bot is logged in
EXPLORE_URL = "a[href='/explore/']"

# CSS template for "Likes" labes used to obtain the number of likes in specified picture
LIKES_INFO = "a[class='_nzn1h _gu6vm']"

#Javascript command that will scroll at the top of the pages
SCROLL_UP = "window.scrollTo(0, 0);"

#Javascript command that will scroll at the bottom of the pages
SCROLL_BOTTOM = "window.scrollTo(0, document.body.scrollHeight);"

#Instagram images per scroll
IMAGES_PER_SCROLL = 12

#url for user login
LOGIN_URL = "accounts/login/"
#username input field
username_field_name = "username"
#password input field
password_field_name = "password"


"""OTHER TAGS"""

HASH_TAG_URL = "explore/tags/"
USER_POST_COUNT_REGEX = '"count": \d+, "page_info"'
USER_FOLLOWING_REGEX = '"follows": {"count": \d+}'
USER_FOLLOWERS_REGEX = '"followed_by": {"count": \d+}'

"""EXTRA"""
DATE_TIME_ATTR = "datetime"
TIME_ATTR = "time"


"""DATABASE SETTINGS"""
DATABASE_PATH = "../web/db.sqlite3"

