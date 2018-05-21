from django.contrib import admin

# Register your models here.

from instagram.models import Page
from instagram.models import Post

admin.site.register(Page)
admin.site.register(Post)



