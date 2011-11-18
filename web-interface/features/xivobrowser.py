import re
from selenium import webdriver

class MissingTranslationException(Exception):
    pass

class XiVOBrowser(webdriver.Firefox):

    def get(self, url):
        """Get the url and check that there is no missing translation, or raise an exception.
        The missing_translation tag is added in the Webi i18n bbf function."""

        # Get the page
        webdriver.Firefox.get(self, url)

        # Remove newline, to allow regexp substitution
        source = self.page_source.replace('\n', ' ')
        # Remove HTML comments
        source = re.sub('<!--.*-->', '', source)
        # Extract missing translations
        missing_translations = re.finditer("__missing_translation:([^:]*):([^:]*):", source)

        # Format missing translations for output
        missing_translations_list = []
        for missing_translation in missing_translations:
            missing_translations_list.append(missing_translation.group(1) + ":" + missing_translation.group(2))

        # Raise exception if necessary
        if missing_translations_list :
            # Uniquify
            missing_translations_list = sorted(set(missing_translations_list))

            raise MissingTranslationException('\n'.join(missing_translations_list))
