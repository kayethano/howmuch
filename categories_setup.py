#!/usr/bin/env python
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "howmuch.localsettings")

from howmuch.category.functions import create_categories_and_tags
create_categories_and_tags()
