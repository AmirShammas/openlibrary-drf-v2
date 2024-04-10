# Openlibrary-DRF-V2

This app scrapes into the [openlibrary](https://openlibrary.org) website using django_rest_framework and saves the scraped data into sqlite database.

## Installation

This app is developed using python 3.11.

After making venv, install the necessary packages using the command below:

```
pip install -r requirements.txt
```

## Usage

Copy `sample_settings.py` file and rename it to `local_settings.py`.

To generate the secret key, run the command below:

```
py -c "import secrets; print(secrets.token_urlsafe())"
```

Copy and paste this new value into the `local_settings.py` under the variable `SECRET_KEY`.

Run the server:

```
py manage.py runserver
```

## Endpoints

`http://localhost:8000/scraper/` => Post request must contain 2 parameteres: one for `search_subject` (default = music) and the other for `search_page_count` (default = 1).
