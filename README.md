# Cache it pls!

Turn your rate-limited APIs into unlimited cached APIs through a dead-simple UI.

> This is alo Aadvik's CS50w's final project!

## Distinctiveness and Complexity

This service was built as a response to a problem I came across when using [GitHub's highly rate-limited RestAPI](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api), the solution to this would be to cache the responses which would require 18-20 fully-tested, bug-free lines of code AND a storage solution (Local, SQL); **Cache it pls!** tries to abstract away this process and spit out a single URL you can reliably call to your hearts content.

Unlike previous challenges of [CS50 Web](https://github.com/aadv1k/cs50) which were "web apps" this tries to be a useful, real-world micro-service to aid in building larger applications.

## Quickstart

```shell
pip install -r requirements.txt
python manage.py runserver
```

**TBD** If you would like to provide your own database you can add a `config.toml`  

```toml

cache_type = "sql" # or local (default)

[db_config]

# ...
```
