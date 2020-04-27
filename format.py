from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


class StaticFormat:
    def __init__(self, fp, parser="html.parser"):
        with open(fp, "rb") as f:
            self.soup = BeautifulSoup(f, parser)
    def _valid_url(self, str):
        """
        Checks if a resource locator is a valid URL
        """
        parsed = urlparse(str)
        nloc, scheme = getattr(parsed, "netloc"), getattr(parsed, "scheme")
        return nloc and scheme
    def _format_str(self, str, prefix):
        """
        Formats resource locator string to meet django static template tag syntax with given prefix
        """
        #relative directory prefixes
        res = re.findall(r"\w+/+", str)
        path = "".join(res)
        #append prefix (if not None)
        if prefix:
            path = f"{prefix}/{path}"
        return f"{{% static '{path}' %}}"
    def replace_locators(self, prefix=None):
        """
        Updates html elements resource locators for use in Django template tags
        """  
        RESOURCE_LOCATOR_ELEMS = ("a", "img", "script", "link") #elements that can have resource locator attribute (img or src)
        page_soup = self.soup.select(", ".join(RESOURCE_LOCATOR_ELEMS))
        for elem in page_soup:
            #get elements src or elem if they exist
            src, href = elem.get("src"), elem.get("href")
            if src and not self._valid_url(src): #update element if src attr exists and is not valid url
                elem["src"] = self._format_str(src, prefix)
            elif href and not self._valid_url(href): #update element if href attr exists and is not valid url
                elem["href"] = self._format_str(href, prefix)
        #store updated in member variable
        self.updt_html = self.soup.prettify("utf-8")
    def write_html(self, fp):
        """
        Writes formatted html passed specified file path
        """
        assert "updt_html" in self.__dict__, "You must call `replace_locators` before writing html."
        with open(fp, "wb") as f:
            f.write(self.updt_html)
