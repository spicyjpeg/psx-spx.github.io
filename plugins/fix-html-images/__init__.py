# -*- coding: utf-8 -*-

"""MkDocs plugin to fix relative URLs in HTML-in-Markdown images

MkDocs allows for use of HTML tags in Markdown, but does not process them in any
way. When using <img> tags, this results in the src attribute *not* being
resolved to the image's actual path in the generated files (see
https://github.com/mkdocs/mkdocs/issues/3618).

This is a problem in pages other than index.md, which MkDocs puts in subfolders;
page.md for instance becomes /page/index.html. If page.md contains a tag such as
<img src="assets/image.png">, the browser will attempt to fetch
/page/assets/image.png rather than the intended /assets/image.png.

This is a simple plugin that works around the issue by scanning each Markdown
file for <img> tags before it is converted to HTML and replacing src attributes
containing relative paths with their respective absolute paths.

NOTE: there are other workarounds that wouldn't require a plugin, such as
explicitly using absolute URLs (e.g. <img src="/assets/image.png">), but they
would prevent other Markdown viewers (IDEs, GitHub, etc.) from displaying the
images.
"""

__version__ = "0.1.0"
__author__  = "spicyjpeg"

__all__ = [ "plugin" ]

from .plugin import FixHTMLImagesPlugin
