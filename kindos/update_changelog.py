# Desc: Get the latest git tag or commit hash
"""
Get the latest git tag or commit hash
"""
import datetime
import subprocess

from .jinja2 import render_template

try:
    latest_tag = subprocess.check_output(
        ["git", "describe", "--tags", "--abbrev=0"],
        stderr=subprocess.DEVNULL,
        text=True,
    ).strip()
except subprocess.CalledProcessError:
    latest_tag = "Uknown"

if not latest_tag:
    latest_tag = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True
    ).strip()

version = latest_tag
date = datetime.datetime.now().strftime("%Y-%m-%d")

# Generate CHANGELOG.md from CHANGELOG.tpl.md
change_log = render_template("CHANGELOG.md.j2", locals(), ".")
print(change_log)
