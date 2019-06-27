# django_periodiq

**django_periodiq** is a Django app that integrates with [periodiq](https://gitlab.com/bersace/periodiq) a simple scheduler for Dramatiq Task Queue.


## Requirements

* [Django][django] 1.11+
* Slightly modified version of periodiq [https://gitlab.com/sovetnikov/periodiq](https://gitlab.com/sovetnikov/periodiq)
You can install it from repo:
    
    
    pip install git+https://gitlab.com/sovetnikov/periodiq

## Installation
Installation is only available directly from this repo:

    pip install git+https://github.com/Sovetnikov/django_periodiq

Add `django_periodiq` to installed apps *after* django_dramatiq:

``` python
import os

INSTALLED_APPS = [
    "django_dramatiq",
    "django_periodiq",

    "myprojectapp1",
    "myprojectapp2",
    # etc...
]
```

## Usage

### Running scheduler

django_periodiq provides a management command you can use to
auto-discover task modules (same as django_dramatiq) and run scheduler:

    python manage.py runperiodiq

or with debug information:


    python manage.py runperiodiq -v2
