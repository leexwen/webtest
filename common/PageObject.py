from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

_LOACATOR_MAP = {'css': By.CSS_SELECTOR,
                 'id': By.ID,
                 'name': By.NAME,
                 'xpath': By.XPATH,
                 'link_text': By.LINK_TEXT,
                 'partial_link_text': By.PARTIAL_LINK_TEXT,
                 'tag_name': By.TAG_NAME,
                 'class_name': By.CLASS_NAME}


class PageObject(object):
    def __init__(self, webdirver, root_url=None):
        self.w = webdirver
        self.root_url = root_url if root_url else getattr(self.w, 'root_url', None)

    def get(self, url):
        root_url = self.root_url or ''
        self.w.get(root_url + url)


class PageElement(object):
    def __init__(self, context=False, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        self.locator = (_LOACATOR_MAP[k], v)
        self.has_context = bool(context)

    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None
        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)
        if not context:
            context = instance.w

        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.clear()
        elem.send_keys(value)


class MultiPageElement(PageElement):
    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


page_element = PageElement
multi_page_element = MultiPageElement
