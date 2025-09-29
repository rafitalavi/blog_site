from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        # Only include the main static pages you want indexed
        return ['home', 'about', 'contact']

    def location(self, item):
        return reverse(item)
