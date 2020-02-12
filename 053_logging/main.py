# 053. logging
#
# loggers, handlers, levels, warnings, and traceback. ConfigParser for INI.
#
# Run: python 053_logging/main.py

# --- configparser ---
import configparser

from io import StringIO

ini = "[db]\nhost = localhost\nport = 5432\n"
c = configparser.ConfigParser()
c.read_file(StringIO(ini))
print(c["db"]["host"], c.getint("db", "port"))

# --- logging mod ---
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("learn")
log.info("hello")
log.debug("hidden")
print("ok")

# --- logging fmt ---
import logging

from io import StringIO

buf = StringIO()
log = logging.getLogger("buf")
log.setLevel(logging.DEBUG)
h = logging.StreamHandler(buf)
h.setFormatter(logging.Formatter("%(name)s %(message)s"))
log.addHandler(h)
log.warning("boom")
print(buf.getvalue().strip())

# --- warnings mod ---
import warnings

warnings.filterwarnings("error", category=UserWarning)
try:
    warnings.warn("careful", UserWarning)
except UserWarning as e:
    print(e)

# --- traceback mod ---
import traceback

try:
    1 / 0
except ZeroDivisionError:
    text = traceback.format_exc()
print("ZeroDivisionError" in text)

# --- logging levels ---
import logging

log = logging.getLogger("levels")
log.setLevel(logging.WARNING)
print(log.isEnabledFor(logging.DEBUG), log.isEnabledFor(logging.ERROR))
print(logging.getLevelName(30))
