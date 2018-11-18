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

## Usage examples

#### Users

Get all users

```bash
$ flarum-api-cli.py users --get

Users in https://your.forum.url
+----+----------+--------------------+-----------+-------------------+-------------------+
| ID | Username |       Email        | Activated |     Last Seen     |       Joined      |
+----+----------+--------------------+-----------+-------------------+-------------------+
| 1  |  admin   |  admin@forum.url   |    True   | 09 Jan 2018 15:10 | 08 Jan 2018 16:19 |
| 2  |  user1   |  user1@forum.url   |    True   | 10 Nov 2018 20:39 | 09 Jan 2018 16:04 |
+----+----------+--------------------+-----------+-------------------+-------------------+
```

Create user

```bash
$ flarum-api-cli.py users --create --username user2 --email user2@forum.url --password user2password
+----+----------+-----------------+---------+
| ID | Username |      Email      |  Status |
+----+----------+-----------------+---------+
| 3  |  user2   | user2@forum.url | created |
+----+----------+-----------------+---------+
```

#### Groups

Get all groups

```bash
$ ./flarum-api-cli.py groups --get

Groups in https://your.forum.url
+----+---------------+-------------+
| ID | Name singular | Name plural |
+----+---------------+-------------+
| 1  |     Admin     |    Admins   |
| 2  |     Guest     |    Guests   |
| 3  |     Member    |   Members   |
| 4  |      Mod      |     Mods    |
+----+---------------+-------------+
```

Create group

```bash
$ ./flarum-api-cli.py groups --create --singular test --plural tests
+----+---------------+-------------+---------+
| ID | Name singular | Name plural |  Status |
+----+---------------+-------------+---------+
| 12 |     test      |    tests    | created |
+----+---------------+-------------+---------+
```

#### Tags

Get all tags

```bash
$ ./flarum-api-cli.py tags --get

Tags in https://your.forum.url
+----+-----------+
| ID |     Name  |
+----+-----------+
| 3  |  tag1     |
| 5  |  tag2     |
+----+-----------+
```

Create tag

```bash
$ ./flarum-api-cli.py tags --create --name tag1 --slug tag1
+----+----------+----------+---------+
| ID | Tag name | Tag slug |  Status |
+----+----------+----------+---------+
| 57 |   tag1   |   tag1   | created |
+----+----------+----------+---------+
```
