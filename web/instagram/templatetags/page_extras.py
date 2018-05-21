from django import template
from instagram.models import Page
from instagram.models import Post


register = template.Library()

@register.inclusion_tag('instagram/tags/pages.html')
def get_page_list():
	return {'pages': Page.objects.all().order_by('-id')}

@register.inclusion_tag('instagram/tags/posts.html')
def get_post_list(page):
	return {'posts': Post.objects.filter(page = page)}

@register.inclusion_tag('instagram/tags/posts.html')
def search_post(keyword):
	results_page_name = Post.objects.filter(page__page_name=keyword)
	results_caption = Post.objects.filter(caption__contains=keyword)
	return {'posts': results_caption.union(results_page_name)}