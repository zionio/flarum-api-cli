## Built for
[![Flarum](http://flarum.org/img/logo.png)](https://flarum.org)

> Flarum is free, open-source forum software built with PHP and Mithril.js.

# flarum-api-cli

**Flarum API CLI** is a very simple and minimal python script to manage some
features of [Flarum forum software](https://flarum.org) such as users, groups and tags from the command line.


###### Current Features

|Users  |Groups |Tags   |
|:-:    |:-:    |:-:    |
|Create |Create |Create |
|Delete |Delete |Delete |
|View   |View   |View   |

## Requirements

```bash
$ pip install argparse
$ pip install requests
$ pip install python-dateutil
$ pip install prettytable
```

## Configuration

1. Clone the repository
2. Edit `config.py` and insert your Flarum forum url in `base_url`
3. Retrieve the `Authorization Token` from your Flarum forum using administrator credentials.

```bash
    $ ./flarum-api-cli.py token -u admin -p admin
    +---------------------+
    |        Token        |
    +---------------------+
    | ******************* |
    +---------------------+
```

4. Edit `config.py` and save token in `auth_token`
