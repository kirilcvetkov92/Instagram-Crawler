from django.db import models

# Create your models here.
from datetime import datetime
from django.template.defaultfilters import slugify


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    followers = models.IntegerField()
    following = models.IntegerField()
    posts = models.IntegerField(default=0)
    page_name = models.TextField(blank=False, null=False, unique=True)
    date_created = models.DateTimeField(default=datetime.now, blank=False)
    thumb_directory = models.TextField(blank=False, null=False)
    slug = models.SlugField(default = page_name)

    def __unicode__(self):
        return self.get_page_name()
    def __str__(self):
        return self.get_page_name()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.page_name)
        super(Page, self).save(*args, **kwargs)

    def get_page_name(self):
        page_name = self.page_name
        if(page_name.endswith(".hashtag")):
            page_name=page_name.replace('.hashtag','')
            page_name = "#"+page_name
        return page_name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page)
    likes = models.TextField(null=True)
    caption = models.TextField(null=True)
    date_posted = models.TextField(null=True)
    image_directory = models.TextField(blank=False, null=True)
    post_id = models.IntegerField(null = False)

    def __unicode__(self):
        return self.page.__str__()+'/post:' + str(self.post_id)

    def __str__(self):
        return self.page.__str__()+'/post:' + str(self.post_id)
