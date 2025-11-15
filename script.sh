#!/bin/bash

uv run manage.py reset_db --noinput
uv run manage.py clear_cache
uv run manage.py clean_pyc
find . -name '__pycache__' -type d -exec rm -r {} +
find . -path './*/migrations/*.py' -not -path './.venv/*' -not -name '__init__.py' -delete
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py update_default_site_object
uv run manage.py create_test_users
uv run manage.py create_categories
uv run manage.py create_attributes
uv run manage.py runserver
