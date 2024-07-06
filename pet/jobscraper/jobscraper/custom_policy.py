import re
from scrapy.http.response.text import TextResponse

class CustomBanDetectionPolicy:

    BANNED_PATTERN = re.compile(r'banned|captcha', re.IGNORECASE)

    def response_is_ban(self, request, response):
        if isinstance(response, TextResponse):
            return self.BANNED_PATTERN.search(response.text) is not None
        return False

    def exception_is_ban(self, request, exception):
        return False
