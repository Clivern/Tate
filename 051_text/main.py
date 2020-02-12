# 051. Text and markup
#
# string, textwrap, difflib, codecs, html, and ElementTree.
#
# Run: python 051_text/main.py

# --- string mod ---
import string

print(string.ascii_lowercase[:5], string.digits)
print(string.Template("hi $name").substitute(name="Ada"))
print(string.capwords("ada lovelace"))

# --- textwrap ---
import textwrap

print(textwrap.wrap("one two three four five", width=10))
print(textwrap.dedent("    line\n    next").strip())

# --- difflib ---
import difflib

a = "hello world".split()
b = "hello there".split()
print("".join(difflib.unified_diff(a, b, lineterm="")))
print(difflib.get_close_matches("appel", ["ape", "apple", "peach"]))

# --- codecs ---
import codecs

print(codecs.encode("café", "utf-8"))
print(codecs.decode(b"\xff", "latin-1"))
print(codecs.lookup("utf-8").name)

# --- html escape ---
import html

print(html.escape("<a & b>"))
print(html.unescape("&amp; &lt; &#65;"))

# --- xml etree ---
import xml.etree.ElementTree as ET

root = ET.fromstring('<doc><item id="1">Ada</item></doc>')
el = root.find("item")
print(el.text, el.get("id"))
