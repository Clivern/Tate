#!/usr/bin/env python3
"""Build the examples website into docs/ for GitHub Pages.

Each example is laid out like Python by Example: full-line # comments become the prose
on the left, the code they describe sits on the right, and the commands from the
header's Run: lines are executed so the page shows their real output.

Usage: python3 site/build.py            # runs every example and writes docs/
       python3 site/build.py --no-run   # skips running, for quick layout work
       python3 -m http.server -d docs   # preview at http://localhost:8000
"""

import ast
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "docs"
REPO = "https://github.com/Clivern/Tate"
SITE_NAME = "Tate"
PAGES_BASE = "/Tate/"

PARTS = [
    ("Basics", 1, 7),
    ("Strings and bytes", 8, 9),
    ("Collections", 10, 13),
    ("Control flow", 14, 17),
    ("Functions", 18, 21),
    ("Classes", 22, 24),
    ("Exceptions and typing", 25, 26),
    ("Built-ins", 27, 27),
    ("System interfaces", 28, 30),
    ("Files and I/O", 31, 32),
    ("Data formats", 33, 35),
    ("SQLite", 36, 36),
    ("Date and time", 37, 38),
    ("Itertools and functools", 39, 41),
    ("Utilities", 42, 44),
    ("Hashing and binary", 45, 46),
    ("Concurrency", 47, 48),
    ("Networking", 49, 49),
    ("Text and regex", 50, 51),
    ("CLI and logging", 52, 53),
    ("Introspection", 54, 55),
    ("Subprocess and testing", 56, 57),
    ("Archives and more", 58, 59),
]

NO_PLAYGROUND = {
    "052_argparse",
    "056_subprocess",
}

DOC_LINE = re.compile(r"^\s*#(?!\!)(?:\s(.*))?$")
NOTE_LINE = re.compile(r"^\s*#\s*(error|output):\s")


# ---------------------------------------------------------------------------
# Python highlighting

KEYWORDS = set(
    "and as assert async await break class continue def del elif else except finally for "
    "from global if import in is lambda match case nonlocal not or pass raise return try "
    "while with yield".split()
)

BUILTINS = set(
    "abs all any ascii bin bool breakpoint bytearray bytes callable chr classmethod compile "
    "complex delattr dict dir divmod enumerate eval exec filter float format frozenset getattr "
    "globals hasattr hash help hex id input int isinstance issubclass iter len list locals map "
    "max memoryview min next object oct open ord pow print property range repr reversed round "
    "set setattr slice sorted staticmethod str sum super tuple type vars zip".split()
)

CONSTANTS = {"True", "False", "None"}

TOKEN = re.compile(
    r"""
    (?P<comment>\#[^\n]*)
    |(?P<str>(?:r|f|fr|rf|b|br|rb)?\"\"\"[\s\S]*?\"\"\")
    |(?P<str2>(?:r|f|fr|rf|b|br|rb)?\'\'\'[\s\S]*?\'\'\')
    |(?P<str3>(?:r|f|fr|rf|b|br|rb)?\"(?:\\.|[^\"\\\n])*\")
    |(?P<str4>(?:r|f|fr|rf|b|br|rb)?\'(?:\\.|[^\'\\\n])*\')
    |(?P<decor>@\w+)
    |(?P<num>\b(?:0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|\d[\d_]*(?:\.\d[\d_]*)?(?:[eE][+-]?\d+)?)\b)
    |(?P<ident>\b[A-Za-z_]\w*\b)
    """,
    re.VERBOSE,
)

NOTE_COMMENT = re.compile(r"#\s*(error|output):")


def highlight(code):
    out = []
    pos = 0
    for m in TOKEN.finditer(code):
        out.append(html.escape(code[pos : m.start()]))
        text = m.group()
        kind = m.lastgroup
        cls = None
        if kind == "comment":
            cls = "e" if NOTE_COMMENT.search(text) else "c"
        elif kind in ("str", "str2", "str3", "str4"):
            cls = "s"
        elif kind == "num":
            cls = "n"
        elif kind == "decor":
            cls = "a"
        elif kind == "ident":
            if text in KEYWORDS:
                cls = "k"
            elif text in CONSTANTS:
                cls = "n"
            elif text in BUILTINS:
                cls = "m"
            elif text[:1].isupper():
                cls = "t"
        esc = html.escape(text)
        out.append(f'<span class="{cls}">{esc}</span>' if cls else esc)
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)


# ---------------------------------------------------------------------------
# Prose

LEAD = '("“'
TRAIL = '.,;:"”)'
PROSE_ABBREVIATIONS = {"e.g.", "i.e.", "etc.", "vs.", "e.g", "i.e", "vs"}
STD_ROOTS = (
    "abc argparse ast asyncio bisect calendar collections concurrent contextlib copy csv "
    "dataclasses datetime email encodings enum errno faulthandler fnmatch fractions functools "
    "gc getpass glob graphlib hashlib heapq hmac html http importlib inspect io ipaddress "
    "itertools json logging math mmap multiprocessing numbers operator os pathlib pickle "
    "platform pprint queue random re sched secrets select shelve shutil signal socket sqlite3 "
    "ssl statistics string struct subprocess sys tarfile tempfile textwrap threading time "
    "tomllib traceback types typing unicodedata unittest urllib uuid venv wave weakref "
    "xml zipfile zoneinfo".split()
)
PY_WORDS = {"None", "True", "False", "self", "cls", "_", "..."}


def looks_like_code(word):
    if word in PROSE_ABBREVIATIONS:
        return False
    if word in PY_WORDS:
        return True
    if re.search(r"==|!=|<=|>=|\(\)|\[\]|[{}]|%[a-z+#]|^\$|=\w|\w=|\w\(|\w\[", word):
        return True
    if re.fullmatch(r"[a-z]\w*(\.[A-Za-z_]\w*)+[\w.()\[\]:]*", word):
        return True
    if (
        re.fullmatch(r"[a-z0-9_]+(\.[a-z0-9_]+)+", word)
        and word.split(".")[0] in STD_ROOTS
    ):
        return True
    if re.fullmatch(r"[\w-]+\.py", word):
        return True
    if re.fullmatch(r"[a-z]+[A-Z]\w*|[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+|\w+_\w+", word):
        return True
    return bool(re.fullmatch(r"\*\w+|\w+\.\.\.", word))


def split_punct(word):
    lead = ""
    while word and word[0] in LEAD:
        lead += word[0]
        word = word[1:]
    trail = ""
    while len(word) > 1 and word[-1] in TRAIL and not word.endswith("()"):
        if word[-1] == ")" and word.count("(") >= word.count(")"):
            break
        trail = word[-1] + trail
        word = word[:-1]
    return lead, word, trail


def unbalanced(code):
    pairs = ("()", "[]", "{}")
    return (
        any(code.count(a) > code.count(b) for a, b in pairs) or code.count('"') % 2 == 1
    )


def inline(text):
    pieces = []
    run = []
    run_glued = False

    def flush():
        if run:
            pieces.append(
                ("<code>" + html.escape(" ".join(run)) + "</code>", run_glued)
            )
            run.clear()

    for word in text.split():
        if run and unbalanced(" ".join(run)):
            core = word.rstrip(".,;:")
            run.append(core)
            if core != word and not unbalanced(" ".join(run)):
                flush()
                pieces.append((html.escape(word[len(core) :]), True))
            continue
        lead, core, trail = split_punct(word)
        if core and looks_like_code(core):
            if lead:
                flush()
                pieces.append((html.escape(lead), False))
            if not run:
                run_glued = bool(lead)
            run.append(core)
            if trail and unbalanced(" ".join(run)):
                run[-1] += trail
            elif trail:
                flush()
                pieces.append((html.escape(trail), True))
        else:
            flush()
            pieces.append((html.escape(word), False))
    flush()
    out = ""
    for piece, glued in pieces:
        out += piece if glued or not out else " " + piece
    return out


def prose(lines):
    blocks = []
    para = []
    for line in lines + [""]:
        if line.strip():
            para.append(line.strip())
        elif para:
            blocks.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
    return "\n".join(blocks)


SECTION_MARKER = re.compile(r"^---\s*(.+?)\s*---\s*$")
STDLIB_NAMES = set(STD_ROOTS)
SECTION_TOKEN = {
    "comp": "comprehension",
    "exc": "exceptions",
    "fmt": "formatting",
    "inherit": "inheritance",
    "kw": "keyword",
    "mgr": "manager",
    "mod": "module",
    "op": "operator",
    "perm": "permutations",
    "proto": "protocol",
    "stmt": "statement",
    "sub": "subcommands",
    "comb": "combinations",
}
SECTION_PHRASE = {
    "abc abstract": "Abstract base classes",
    "and or": "and and or",
    "any all": "any() and all()",
    "argparse sub": "Subcommands",
    "argparse types": "Argument types",
    "assert stmt": "assert",
    "asyncio hello": "First coroutine",
    "break continue": "break and continue",
    "cast any": "cast() and Any",
    "chaining": "Chaining comparisons",
    "class attr": "Class attributes",
    "class method": "Class methods",
    "collections abc": "collections.abc",
    "context mgr": "Context managers",
    "copy obj": "Shallow and deep copy",
    "custom exc": "Custom exceptions",
    "dataclasses field": "dataclasses.field",
    "dataclasses frozen": "Frozen dataclasses",
    "datetime fmt": "strftime and strptime",
    "decorator args": "Decorators with arguments",
    "del stmt": "del statement",
    "dict comp": "Dict comprehensions",
    "dict views": "dict views",
    "else loops": "else on loops",
    "else try": "try / except / else",
    "enum flag": "Enum flags",
    "eq hash": "__eq__ and __hash__",
    "format spec": "Format specifications",
    "for": "For loops",
    "fstrings": "F-strings",
    "futures wait": "concurrent.futures.wait",
    "genexp": "Generator expressions",
    "call": "__call__",
    "dunder": "Special methods",
    "getitem": "__getitem__ and slicing",
    "init": "__init__",
    "global kw": "global statement",
    "html escape": "html.escape",
    "identity": "Identity comparisons",
    "if else": "if / else",
    "in op": "The in operator",
    "is vs eq": "is versus ==",
    "iter proto": "Iterator protocol",
    "json custom": "Custom JSON encoding",
    "json indent": "Pretty-printed JSON",
    "keyword only": "Keyword-only parameters",
    "list comp": "List comprehensions",
    "logging fmt": "Formatters",
    "logging levels": "Log levels",
    "map filter": "map() and filter()",
    "match guard": "Match guards",
    "min max sum": "min(), max(), and sum()",
    "multiple inherit": "Multiple inheritance",
    "next fn": "__next__",
    "nonlocal kw": "nonlocal statement",
    "os environ": "Environment variables",
    "os walk": "os.walk",
    "pass ellipsis": "pass and Ellipsis",
    "path glob": "Path.glob",
    "path parts": "Path parts",
    "pathlib write": "Reading and writing paths",
    "positional only": "Positional-only parameters",
    "raw strings": "Raw strings",
    "re flags": "Regex flags",
    "re groups": "Capture groups",
    "re sub": "re.sub",
    "repr str": "__repr__ and __str__",
    "set comp": "Set comprehensions",
    "set ops": "Set operations",
    "sorted key": "sorted() with key=",
    "sqlite join": "SQL joins with sqlite3",
    "star pattern": "Star patterns in match",
    "starargs": "*args and **kwargs",
    "static method": "Static methods",
    "statistics spread": "Variance and spread",
    "subprocess pipe": "Pipes and I/O",
    "sys argv": "Command-line arguments",
    "sys path": "sys.path",
    "ternary": "Conditional expressions",
    "truthiness": "Truthiness",
    "type alias": "Type aliases",
    "typing annotated": "Annotated types",
    "typing literal": "Literal types",
    "typing newtype": "NewType",
    "typing union": "Union types",
    "walrus": "Walrus operator (:=)",
    "while": "While loops",
    "with stmt": "with statement",
    "xml etree": "xml.etree",
    "yield from": "yield from",
}
SECTION_BLURB = {
    "functools lru": "Common patterns with functools.lru_cache.",
    "bytes": "bytes and bytearray basics, plus views into binary data.",
    "classes": "Defining types with methods and instance state.",
    "decorators": "Functions that wrap other functions.",
    "dicts": "Creating and updating key–value mappings.",
    "encoding": "Encoding and decoding text as bytes.",
    "exceptions": "Catching and handling errors.",
    "functions": "Defining and calling functions.",
    "lists": "Mutable sequences: append, pop, sort, and slice.",
    "operators": "Arithmetic, comparison, and logical operators.",
    "sets": "Unordered collections of unique values.",
    "slicing": "Slice notation and assignment on sequences.",
    "strings": "Literals, methods, and everyday string operations.",
    "unicode": "Code points, ord/chr, and composed characters.",
}


def humanize_section(slug):
    if slug in SECTION_PHRASE:
        return SECTION_PHRASE[slug]
    words = slug.replace("_", " ").split()
    if not words:
        return slug
    if len(words) >= 2 and words[-1] == "mod":
        return f"{' '.join(words[:-1])} module"
    if len(words) >= 2 and words[0] in STDLIB_NAMES:
        return f"{words[0]}.{'.'.join(words[1:])}"
    text = " ".join(SECTION_TOKEN.get(w, w) for w in words)
    if len(words) == 1 and words[0] not in STDLIB_NAMES:
        return text[0].upper() + text[1:]
    return text


def section_blurb(slug):
    if slug in SECTION_BLURB:
        return SECTION_BLURB[slug]
    words = slug.replace("_", " ").split()
    if len(words) >= 2 and words[-1] == "mod":
        pkg = " ".join(words[:-1])
        return f"Examples from the {pkg} standard library module."
    if len(words) >= 2 and words[0] in STDLIB_NAMES:
        return f"Common patterns with {words[0]}.{'.'.join(words[1:])}."
    title = humanize_section(slug)
    topic = title[0].lower() + title[1:] if title and title[0].isupper() else title
    return f"Runnable examples for {topic}."


def segment_prose(lines):
    blocks = []
    para = []

    def flush_para():
        if para:
            blocks.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    for line in lines + [""]:
        stripped = line.strip()
        if not stripped:
            flush_para()
            continue
        m = SECTION_MARKER.match(stripped)
        if m:
            flush_para()
            slug = m.group(1).strip()
            blurb = section_blurb(slug)
            blocks.append(f"<p>{html.escape(blurb)}</p>")
            continue
        para.append(stripped)
    flush_para()
    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# Example parsing


def header_text(line):
    m = DOC_LINE.match(line)
    if not m:
        return None
    return (m.group(1) or "").strip()


def segments(lines):
    segs = []
    docs, code = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        is_doc = DOC_LINE.match(line) and not NOTE_LINE.match(line)
        if is_doc and i + 1 < len(lines) and NOTE_LINE.match(lines[i + 1]):
            is_doc = False
        if is_doc:
            if code:
                segs.append((docs, code))
                docs, code = [], []
            docs.append(header_text(line))
        elif line.strip() or code:
            code.append(line)
        i += 1
    segs.append((docs, code))
    out = []
    for d, c in segs:
        while c and not c[-1].strip():
            c.pop()
        if d or c:
            out.append((segment_prose(d), "\n".join(c)))
    return out


def find_imports(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    return mods


def parse(folder):
    text = (folder / "main.py").read_text()
    lines = text.splitlines()
    header = []
    i = 0
    while i < len(lines) and DOC_LINE.match(lines[i]):
        header.append(header_text(lines[i]))
        i += 1
    title = header[0].strip() if header else folder.name
    command = re.compile(r"^Run: (.*)")
    commands = [command.match(l).group(1) for l in header if command.match(l)]
    body = [l for l in header[1:] if not command.match(l)]
    extras = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.name != "main.py" and p.suffix == ".py":
            rel = p.relative_to(folder).as_posix()
            src = p.read_text().rstrip()
            extras.append(
                {"name": rel, "source": src, "segments": segments(src.splitlines())}
            )
    sources = [text] + [e["source"] for e in extras]
    imports = set().union(*(find_imports(s) for s in sources))
    return {
        "slug": folder.name,
        "num": int(folder.name[:3]),
        "title": title,
        "intro": prose(body),
        "commands": commands,
        "segments": segments(lines[i:]),
        "source": text.rstrip(),
        "extras": extras,
        "imports": imports,
        "lines": sum(s.count("\n") + 1 for s in sources),
    }


# ---------------------------------------------------------------------------
# Running examples


def scrub(text):
    text = text.replace(str(ROOT), ".")
    text = text.replace(str(Path.home()), "~")
    text = re.sub(r"/private/var/folders/[^\s\"']+?/T\b", "/tmp", text)
    return text.replace(tempfile.gettempdir().rstrip("/"), "/tmp")


def run_example(example):
    shell = []
    for cmd in example["commands"]:
        try:
            proc = subprocess.run(
                ["bash", "-c", cmd],
                cwd=ROOT,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=120,
                text=True,
            )
            output = scrub(proc.stdout).rstrip()
        except subprocess.TimeoutExpired:
            print(f"  {example['slug']}: {cmd!r} timed out", file=sys.stderr)
            output = ""
        shell.append((cmd, output))
    example["shell"] = shell


def run_outputs(examples):
    print("checking examples...", file=sys.stderr)
    files = [str(ROOT / e["slug"] / "main.py") for e in examples]
    subprocess.run([sys.executable, "-m", "py_compile", *files], check=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(run_example, examples))


# ---------------------------------------------------------------------------
# Pages

FONTS = (
    "https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..700"
    "&family=JetBrains+Mono:wght@400;500&display=swap"
)

FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
    "<rect width='32' height='32' rx='8' fill='%231C1B19'/><text x='16' y='22' "
    "font-family='Arial' font-weight='700' font-size='17' fill='white' "
    "text-anchor='middle'>T</text></svg>"
)

THEME_BOOT = (
    "(function(){try{var t=localStorage.getItem('_ftheme');"
    "if(!t&&matchMedia('(prefers-color-scheme: dark)').matches)t='dark';"
    "if(t&&t!=='default')document.documentElement.classList.add('theme-'+t)}catch(e){}})();"
)

ICON_COPY = (
    '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">'
    '<rect x="7" y="7" width="10" height="10" rx="2"/>'
    '<path d="M13 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/></svg>'
)
ICON_PLAY = (
    '<svg viewBox="0 0 20 20" fill="currentColor"><path d="M6 4.5v11l9-5.5z"/></svg>'
)
ICON_GITHUB = (
    '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 '
    "3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49"
    "-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82."
    "72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-"
    "1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 "
    "1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 "
    "2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21."
    '15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>'
)


def page(title, body, base, description):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{FAVICON}">
<script>{THEME_BOOT}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="topbar">
  <button class="menu-btn" type="button" aria-label="Examples" data-menu>
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h14M3 10h14M3 14h14"/></svg>
  </button>
  <a class="brand" href="{base}"><span class="brand-mark">T</span>{SITE_NAME}</a>
  <nav class="topnav">
    <a class="nav-link" href="{base}">Examples</a>
    <a class="nav-link" href="{REPO}" aria-label="GitHub">{ICON_GITHUB}<span>GitHub</span></a>
    <select class="input-field theme-select" aria-label="Theme" data-theme-select>
      <option value="default">Default</option>
      <option value="blue">Blue</option>
      <option value="slate">Slate</option>
      <option value="emerald">Emerald</option>
      <option value="dark">Dark</option>
    </select>
  </nav>
</header>
{body}
<script src="{base}assets/site.js"></script>
</body>
</html>
"""


def copy_button(text=None):
    attr = f'data-copy-text="{html.escape(text)}"' if text is not None else "data-copy"
    return f'<button class="icon-btn" type="button" {attr} title="Copy">{ICON_COPY}</button>'


def segment_table(segs, source, extra_buttons=""):
    rows = []
    for i, (doc, code) in enumerate(segs):
        actions = ""
        if i == 0:
            actions = (
                f'<div class="code-actions">{extra_buttons}{copy_button(source)}</div>'
            )
        code_html = f"<pre><code>{highlight(code)}</code></pre>" if code else ""
        empty = "" if code else " empty"
        rows.append(
            f'<div class="seg"><div class="seg-doc prose">{doc}</div>'
            f'<div class="seg-code code{empty}">{actions}{code_html}</div></div>'
        )
    return f'<div class="segs">{"".join(rows)}</div>'


def shell_block(shell):
    parts = []
    for cmd, output in shell:
        parts.append(
            f'<span class="prompt">$</span> <span class="cmd">{html.escape(cmd)}</span>'
        )
        if output:
            parts.append(html.escape(output))
    return '<div class="shell"><pre>' + "\n".join(parts) + "</pre></div>"


def sidebar(examples, active, base):
    out = [
        '<aside class="sidebar" data-sidebar>',
        '<input class="input-field side-search" type="search" placeholder="Filter examples  /" data-filter>',
    ]
    for name, lo, hi in PARTS:
        links = []
        for e in examples:
            if lo <= e["num"] <= hi:
                cls = "side-link active" if e["slug"] == active else "side-link"
                links.append(
                    f'<a class="{cls}" href="{base}{e["slug"]}/">'
                    f'<span class="side-num">{e["num"]:03}</span>'
                    f"<span>{html.escape(e['title'])}</span></a>"
                )
        out.append(
            f'<div class="side-part"><div class="side-title">{html.escape(name)}</div>'
            + "".join(links)
            + "</div>"
        )
    out.append("</aside>")
    return "\n".join(out)


def part_of(num):
    return next(name for name, lo, hi in PARTS if lo <= num <= hi)


def example_page(ex, prev, nxt, examples):
    base = "../"
    slug = ex["slug"]
    play = ""
    if slug not in NO_PLAYGROUND and not ex["extras"]:
        play = (
            '<button class="icon-btn" type="button" data-play title="Copy and open in Playcode">'
            f"{ICON_PLAY}</button>"
        )
    body_parts = [segment_table(ex["segments"], ex["source"], play)]
    if ex.get("shell"):
        body_parts.append(shell_block(ex["shell"]))
    for extra in ex["extras"]:
        body_parts.append(
            f'<h3 class="file-name">{html.escape(slug + "/" + extra["name"])}</h3>'
        )
        body_parts.append(segment_table(extra["segments"], extra["source"]))
    pager = ['<nav class="pager">']
    if prev:
        pager.append(
            f'<a class="pager-card" href="{base}{prev["slug"]}/" data-prev>'
            f'<span class="pager-dir">← Previous</span>'
            f'<span class="pager-title">{prev["num"]:03}. {html.escape(prev["title"])}</span></a>'
        )
    else:
        pager.append("<span></span>")
    if nxt:
        pager.append(
            f'<a class="pager-card next" href="{base}{nxt["slug"]}/" data-next>'
            f'<span class="pager-dir">Next →</span>'
            f'<span class="pager-title">{nxt["num"]:03}. {html.escape(nxt["title"])}</span></a>'
        )
    pager.append("</nav>")
    packages = " ".join(f"<code>{html.escape(p)}</code>" for p in sorted(ex["imports"]))
    body = f"""<div class="layout">
{sidebar(examples, slug, base)}
<div class="content wide">
<main class="main example">
  <div class="page-header">
    <div class="eyebrow">{html.escape(part_of(ex["num"]))} · Example {ex["num"]:03}</div>
    <h1 class="page-title">{html.escape(ex["title"])}</h1>
    <div class="page-subtitle">{packages}</div>
  </div>
  <section class="intro prose">{ex["intro"]}</section>
  {"".join(body_parts)}
  <div class="source-link"><a class="btn-secondary btn-sm" href="{REPO}/tree/master/{slug}">{ICON_GITHUB}View on GitHub</a></div>
  {"".join(pager)}
</main>
</div>
</div>"""
    title = f"{ex['title']} · {SITE_NAME}"
    return page(title, body, base, f"{SITE_NAME}: Python by example, {ex['title']}")


def index_page(examples):
    packages = set().union(*(e["imports"] for e in examples))
    lines = sum(e["lines"] for e in examples)
    parts = []
    for name, lo, hi in PARTS:
        cards = []
        for e in examples:
            if lo <= e["num"] <= hi:
                cards.append(
                    f'<a class="lesson-card" href="{e["slug"]}/">'
                    f'<span class="lesson-num">{e["num"]:03}</span>'
                    f'<span class="lesson-title">{html.escape(e["title"])}</span></a>'
                )
        parts.append(
            f'<section class="part" data-part><h2 class="section-title">{html.escape(name)}'
            f'<span class="part-range">{lo:03}–{hi:03}</span></h2>'
            f'<div class="lesson-grid">{"".join(cards)}</div></section>'
        )
    stat = lambda label, value: (
        f'<div class="stat-card"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value:,}</div></div>'
    )
    body = f"""<main class="home">
  <section class="hero">
    <div class="eyebrow">Python 3.12+</div>
    <h1 class="hero-title">A hands-on introduction to Python, <br>one annotated example at a time.</h1>
    <p class="hero-sub">Each example is a runnable script. The comments explain the code next
    to them, and the output underneath is what the program really prints. Language basics and
    the standard library only — third-party packages come later.</p>
    <div class="hero-actions">
      <a class="btn-primary" href="{examples[0]["slug"]}/">Start with Hello</a>
      <a class="btn-secondary" href="{REPO}">{ICON_GITHUB}Clone the repo</a>
    </div>
  </section>
  <section class="stats">
    {stat("Examples", len(examples))}{stat("Topics", len(PARTS))}{stat("Modules imported", len(packages))}{stat("Lines of Python", lines)}
  </section>
  <div class="home-search"><input class="input-field" type="search" placeholder="Search examples  /" data-filter></div>
  {"".join(parts)}
</main>"""
    return page(
        f"{SITE_NAME} · Python by example",
        body,
        "",
        "Annotated, runnable Python examples.",
    )


def not_found_page():
    body = f"""<main class="home not-found">
  <div class="eyebrow">404</div>
  <h1 class="hero-title">This page does not exist.</h1>
  <p class="hero-sub">The example may have been renamed.</p>
  <div class="hero-actions"><a class="btn-primary" data-home href="/">Browse all examples</a></div>
</main>
<script>document.querySelector('[data-home]').href=location.pathname.split('/').slice(0,2).join('/')+'/';</script>"""
    return page(f"Not found · {SITE_NAME}", body, PAGES_BASE, "Page not found")


def main():
    examples = [
        parse(f)
        for f in sorted(ROOT.glob("[0-9][0-9][0-9]_*"))
        if (f / "main.py").is_file()
    ]
    if "--no-run" not in sys.argv:
        run_outputs(examples)
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("[0-9][0-9][0-9]_*"):
        shutil.rmtree(old)
    shutil.rmtree(OUT / "assets", ignore_errors=True)
    (OUT / "assets").mkdir()
    shutil.copy(SITE / "style.css", OUT / "assets" / "style.css")
    shutil.copy(SITE / "site.js", OUT / "assets" / "site.js")
    shutil.copy(SITE / "hero.jpg", OUT / "assets" / "hero.jpg")
    (OUT / ".nojekyll").write_text("")
    for i, ex in enumerate(examples):
        prev = examples[i - 1] if i > 0 else None
        nxt = examples[i + 1] if i + 1 < len(examples) else None
        (OUT / ex["slug"]).mkdir()
        (OUT / ex["slug"] / "index.html").write_text(
            example_page(ex, prev, nxt, examples)
        )
    (OUT / "index.html").write_text(index_page(examples))
    (OUT / "404.html").write_text(not_found_page())
    empty = [
        e["slug"]
        for e in examples
        if "shell" in e and not any(o for _, o in e["shell"])
    ]
    if empty:
        print("no output for: " + ", ".join(empty), file=sys.stderr)
    print(f"wrote {len(examples)} examples to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
