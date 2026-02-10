#!/bin/bash

uv run manage.py reset_db --noinput
uv run manage.py clear_cache
uv run manage.py clean_pyc
find . -name '__pycache__' -type d -exec rm -r {} +
find media -mindepth 1 -maxdepth 1 ! -name 'Around_v1.0' -exec rm -rf {} +
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py update_site_domain_and_name
uv run manage.py create_test_superusers
uv run manage.py create_test_users
uv run manage.py create_test_products
uv run manage.py runserver
