# 049. urllib
#
# urlparse, urlencode, and request helpers.
#
# Run: python 049_urllib/main.py

# --- urllib parse ---
from urllib.parse import urlparse, urlencode, quote

u = urlparse("https://example.com:443/a?x=1#f")
print(u.scheme, u.hostname, u.path, u.query)
print(urlencode({"q": "a b"}))
print(quote("a/b c"))

# --- urllib request ---
from urllib.request import url2pathname

from urllib.parse import urlparse

print(urlparse("https://example.com/x").netloc)
print(url2pathname("/tmp/x"))
