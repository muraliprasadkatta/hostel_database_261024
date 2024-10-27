from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        # Only include public pages accessible without login
        return [
            'login_and_registration',  # Public login/registration page
            # Add other public views if available
        ]

    def location(self, item):
        return reverse(item)
