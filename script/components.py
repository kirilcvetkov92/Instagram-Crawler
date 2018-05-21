import os

import settings as config

try:
    from urlparse import urljoin
    from urllib import urlretrieve
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlretrieve
import codecs
import time
from datetime import datetime


class Page(object):

    followers = []
    following = []
    posts = []

    def __init__(self, page_name=config.DEFAULT_PAGE_NAME,
                 followers=0, following=0, post_info=0,
                 directory=config.DEFAULT_SAVE_DIR):
        self.page_name = page_name
        self.followers_info = followers
        self.following_info = following
        self.post_info = 0
        self.directory = directory
        self.thumb = None
        self.date = None
        self.stripped_name = self.get_stripped_name()

    def delete_all_posts_sql(self, conn, page_id):
        c = conn.cursor()
        c.execute("DELETE FROM instagram_post WHERE page_id = ?", (page_id,))

    def export_to_sql(self, conn):
        c = conn.cursor()
        # Create table
        c.execute("SELECT id FROM instagram_page WHERE page_name = ?", (self.stripped_name,))
        data = c.fetchone()

        if not data:
            c.execute(
                "INSERT INTO instagram_page(page_name,followers,following,date_created, posts,thumb_directory, slug) VALUES (?,?,?,?,?,?,?)",
                [self.stripped_name, self.followers_info, self.following_info, datetime.now(), self.post_info, self.thumb, self.stripped_name])
            post_id = c.lastrowid;
        else:
            t = c.execute(
                """UPDATE instagram_page SET page_name = ? ,followers = ?,following = ?,date_created = ?, posts=?,thumb_directory=? WHERE page_name = ? """,
                (self.stripped_name, self.followers_info, self.following_info, datetime.now(), self.post_info,
                 self.thumb, self.stripped_name))
            post_id = data[0]

        self.delete_all_posts_sql(conn, post_id)
        for post in self.posts:
            post.export_to_sql(conn, post_id)

    def save(self):
        def save_thumb(directory):
            print("Downloading profile photo")

            # save thumbnail
            _, ext = os.path.splitext(self.thumbdir)
            filename = str("thumb") + ext
            filepath = os.path.join(directory, filename)
            try:
                urlretrieve(self.thumbdir, filepath)
            except:
                print("Couldn't download image")

            time.sleep(0.1)
            # Send image request
            self.thumb = filename
            return filepath

        # Check if is hashtag
        page_name = self.page_name
        stripped_name = self.get_stripped_name()

        directory = os.path.join(self.directory, stripped_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        print("Saving page to directory: {}".format(directory))

        # Save Photo thumb
        save_thumb(directory)

        for post in self.posts:
            image_file_path = post.save_image_to_disc(directory)
            #post.save_caption_to_disc(directory)

    def get_stripped_name(self):
        stripped_name = self.page_name.lstrip(
            '#') + '.hashtag' if self.is_hash_tag() else self.page_name
        return stripped_name

    def add_posts(self, posts):
        try:
            self.thumbdir = posts[0].image
            start = 0 if self.is_hash_tag() else 1
            self.posts += posts[start:self.post_info + start]
        except Exception:
            pass

    def add_follower(self, follower):
        self.followers.append(follower)

    def add_folling(self, following):
        self.following.append(following)

    def set_followers(self, followers):
        self.followers_info = followers

    def set_following(self, following):
        self.following_info = following

    def set_posts(self, posts):
        self.post_info = posts

    def add_post(self, post):
        self.posts.append(post)

    def get_page(self, id):
        return self.posts[id]

    def is_hash_tag(self):
        """returns whether page is 
            hastag or user profile """
        return self.page_name.startswith('#')


class Post(object):
    def __init__(self, id, caption="", time="", likes=None, image_url=""):
        self.caption = caption
        self.likes = likes
        self.image = image_url
        self.id = id
        self.time = time

    def save_image_to_disc(self, directory):

        print("Downloading image for post {} ".format(self.id))

        # Filename
        _, ext = os.path.splitext(self.image)
        filename = str(self.id) + ext
        filepath = os.path.join(directory, filename)
        try:
            urlretrieve(self.image, filepath)
        except:
            print("Couldn't download image")

        time.sleep(0.1)
        # Send image request
        self.image_dir = filename
        return filepath

    def save_caption_to_disc(self, directory):
        print("Info retrive image for post {} ".format(self.id))
        filename = str(self.id) + '.txt'
        filepath = os.path.join(directory, filename)

        with codecs.open(filepath, 'w', encoding='utf-8') as fout:
            fout.write(self.caption + '\n')

        self.text_dir = filename
        return filepath

    def export_to_sql(self, conn, page_id):
        c = conn.cursor()

        c.execute(
            "INSERT INTO instagram_post(post_id, likes, caption, date_posted, image_directory, page_id) VALUES (?,?,?,?,?,?)",
            [self.get_id(), self.likes, self.caption, self.time, self.image_dir, page_id])

    def get_id(self):
        return self.id
