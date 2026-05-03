# -*- coding: utf-8 -*-

import html, re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins         import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from mkdocs.utils           import normalize_url

# "You can't parse [X]HTML with regex. Because HTML can't be parsed by regex.
# Regex is not a tool that can be used to correctly parse HTML. As I have
# answered in HTML-and-regex questions here so many times before, the use of
# regex will not allow you to consume HTML..."
HTML_IMAGE_REGEX: re.Pattern = \
    re.compile(r"(<img\s[^>]*?src=)('.*?'|\".*?\"|[^'\"\s]*)([^>]*?>)", re.IGNORECASE)

class FixHTMLImagesPlugin(BasePlugin):
    def on_page_markdown(
        self,
        markdown: str,
        page:     Page,
        config:   MkDocsConfig,
        files:    Files
    ) -> str | None:
        def replace(matched: re.Match) -> str:
            prefix, src, suffix = matched.groups()

            if (src[0] == "'") or (src[0] == "\""):
                src = src[1:-1]

            src = html.unescape(src)
            src = normalize_url(src, page)
            src = html.escape(src, True)

            return f"{prefix}\"{src}\"{suffix}"

        return HTML_IMAGE_REGEX.sub(replace, markdown)
