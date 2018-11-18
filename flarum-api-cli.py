#!/usr/bin/env python

import argparse
import sys
import requests
import json
import httplib
import dateutil.parser
from prettytable import PrettyTable
from config import *

prog_name = 'flarum-api-cli.py'

class FParse(object):
    global prog_name
    def __init__(self):
        parser = argparse.ArgumentParser(description='Minimal Flarum API CLI', usage='''%s <command> [<args>]

Active commands are:
   token            Retrieve authentication token
   config           Show config
   users            Manage users
   groups           Manage groups
   tags             Manage tags
''' % prog_name)
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def token(self):
        parser = argparse.ArgumentParser(description='Retrieve authentication token',
            usage='%s token [-h] -u USERNAME -p PASSWORD' % prog_name )
        parser.add_argument('-u', '--username', action='store', help='admin username')
        parser.add_argument('-p', '--password', action='store', help='admin password')
        args = parser.parse_args(sys.argv[2:])
        if not args.username or not args.password:
            print 'Admin USERNAME and PASSWORD required'
        else:
            t = PrettyTable(['Token'])
            t.add_row([retrieve_token(username=args.username, password=args.password)])
            print t

    def config(self):
        parser = argparse.ArgumentParser(description='Show config',
            usage='%s config [-h]' % prog_name )
        args = parser.parse_args(sys.argv[2:])
        t = PrettyTable(['Authorization Token', 'Flarum Base URL'])
        t.add_row([auth_token, base_url])
        print t

    def users(self):
        parser = argparse.ArgumentParser(description='Manage users',
            usage='%s users [-h] [-g] [-d -i ID] [-n -u USERNAME -e EMAIL -p PASSWORD]' % prog_name)
        parser.add_argument('-g', '--get', action='store_true', help='get all users')
        parser.add_argument('-d', '--delete', action='store_true', help='delete a user by ID')
        parser.add_argument('-c', '--create', action='store_true', help='register a new user. USERNAME, EMAIL, PASSWORD required')
        parser.add_argument('-u', '--username', action='store', help='insert USERNAME')
        parser.add_argument('-e', '--email', action='store', help='insert EMAIL')
        parser.add_argument('-p', '--password', action='store', help='insert PASSWORD')
        parser.add_argument('-i', '--id', action='store', help='insert ID')
        args = parser.parse_args(sys.argv[2:])
        if args.get:
            t = get_all_users()
            print '\nUsers in %s' % base_url
            print t

        if args.delete:
            if not args.id:
                print 'ID required'
            if args.id:
                t = delete_user_by_id(id=args.id)
                print t

        if args.create:
            if not args.username or not args.email or not args.password:
                print 'USERNAME, EMAIL, PASSWORD required'
            else:
                print register_user(username=args.username, email=args.email, password=args.password)

    def groups(self):
        parser = argparse.ArgumentParser(description='Manage groups',
            usage='%s groups [-h] [-g] [-c -s S_NAME -p P_NAME] [-d -i ID]' % prog_name )
        parser.add_argument('-g','--get', help='get all groups', action='store_true')
        parser.add_argument('-c','--create', help='create new group, SINGULAR and PLURAL name required', action='store_true')
        parser.add_argument('-s','--singular', help='group SINGULAR NAME', action='store')
        parser.add_argument('-p','--plural', help='group PLURAL NAME', action='store')
        parser.add_argument('-d','--delete', help='delete a group by ID', action='store_true')
        parser.add_argument('-i','--id', help='group ID', action='store')
        args = parser.parse_args(sys.argv[2:])
        if args.get:
            t = get_all_groups()
            print '\nGroups in %s' % base_url
            print t

        if args.delete:
            if not args.id:
                print 'group ID required'
            if args.id > 0:
                t = delete_group_by_id(id=args.id)
                print t

        if args.create:
            if not args.singular or not args.plural:
                print 'SINGULAR and PLURAL group name required'
            if args.singular and args.plural:
                t = create_group(name_singular=args.singular, name_plural=args.plural)
                print t

    def tags(self):
        parser = argparse.ArgumentParser(description='Manage tags',
            usage='%s tags [-h] [-g] [-c -n NAME -s SLUG] [-d -i ID]' % prog_name )
        parser.add_argument('-g','--get', help='get all tags', action='store_true')
        parser.add_argument('-c','--create', help='create new tag, NAME and SLUG required', action='store_true')
        parser.add_argument('-n','--name', help='tag NAME', action='store')
        parser.add_argument('-s','--slug', help='tag SLUG', action='store')
        parser.add_argument('-d','--delete', help='delete a tag by ID', action='store_true')
        parser.add_argument('-i','--id', help='tag ID', action='store')
        args = parser.parse_args(sys.argv[2:])
        if args.get:
            t = get_all_tags()
            print '\nTags in %s' % base_url
            print t

        if args.create:
            if not args.name or not args.slug:
                print 'tag NAME and SLUG required'
            if args.name and args.slug:
                print create_tag(name=args.name, slug=args.slug)

        if args.delete:
            if not args.id:
                print 'tag ID required'
            if args.id:
                print delete_tag_by_id(id=args.id)

## MAIN
# api-endpoint
api_endpoint = base_url + '/api'
api_token = api_endpoint + '/token'
api_users = api_endpoint + '/users'
api_tags = api_endpoint + '/tags'
api_groups = api_endpoint + '/groups'

api_header = { 'Content-Type' : 'application/vnd.api+json' }
auth_headers = {'Content-Type':'application/json',
               'Authorization': 'Token {}'.format(auth_token)}

def errors(json):
    e = {}
    json_data = json['errors']
    for dict in json_data:
        for key, value in dict.iteritems():
            if key == 'status' or key == 'code' or key == 'detail':
                e.update({key: value})
    return e

def retrieve_token(username, password):
    data = { "identification" : str(username), "password" : str(password) }
    r = requests.post (url = api_token, data = json.dumps(data), headers = api_header, verify = ssl_verity_cert)
    if r.status_code == 200:
        return json.loads(r.text)['token']
    else:
        return 'Error: %s' % httplib.responses[r.status_code]

## TAGS

def get_all_tags():
    r = requests.get (url = api_tags, headers = auth_headers, verify = ssl_verity_cert)
    json_data = r.json()
    t = PrettyTable(['ID', 'Name'])
    if r.status_code == 200:
        for tag in json_data['data']:
            t.add_row([ tag['id'], tag['attributes']['name'] ])
    else:
        t.add_row(['failed', httplib.responses[r.status_code]])
    return t

def delete_tag_by_id(id):
    api_delete_tags = api_tags + '/' + id
    r = requests.delete (url = api_delete_tags, headers = auth_headers, verify = ssl_verity_cert)
    t = PrettyTable(['Tag ID', 'Status'])
    if r.status_code == 204:
        t.add_row([id, 'deleted'])
    else:
        t.add_row([id, errors(r.json())['code']])
    return t

def create_tag(name, slug):
    data = {'data': { 'attributes': {'name': name, 'slug': slug }}}
    r = requests.post (url = api_tags, headers = auth_headers, data = json.dumps(data), verify = ssl_verity_cert)
    if r.status_code == 201:
        t = PrettyTable(['ID', 'Tag name', 'Tag slug', 'Status'])
        id = r.json()['data']['id']
        t.add_row([id, name, slug, 'created'])
    else:
        t = PrettyTable(['Tag name', 'Tag slug', 'Status'])
        t.add_row([name, slug, httplib.responses[r.status_code]])
    return t

## GROUPS

def create_group(name_singular, name_plural):
    data = {'data': { 'attributes': {'nameSingular': name_singular, 'namePlural': name_plural }}}
    r = requests.post (url = api_groups, headers = auth_headers, data = json.dumps(data), verify = ssl_verity_cert)
    if r.status_code == 201:
        t = PrettyTable(['ID', 'Name singular', 'Name plural', 'Status'])
        id = r.json()['data']['id']
        t.add_row([ id, name_singular, name_plural, 'created' ])
    else:
        t = PrettyTable(['Name singular', 'Name plural', 'Status'])
        t.add_row([name_singular, name_plural, httplib.responses[r.status_code]])
    return t

def get_all_groups():
    r = requests.get (url = api_groups, headers = auth_headers, verify = ssl_verity_cert)
    t = PrettyTable(['ID', 'Name singular', 'Name plural'])
    json_data = r.json()
    if r.status_code == 200:
        for group in json_data['data']:
            t.add_row([ group['id'], group['attributes']['nameSingular'], group['attributes']['namePlural']])
    else:
        t.add_row(['failed', 'reason', httplib.responses[r.status_code]])
    return t

def delete_group_by_id(id):
    api_delete_group = api_groups + '/' + id
    r = requests.delete (url = api_delete_group, headers = auth_headers, verify = ssl_verity_cert)
    t = PrettyTable(['Group ID', 'Status'])
    if r.status_code == 204:
        t.add_row([id, 'deleted'])
    else:
        t.add_row([id, errors(r.json())['code']])
    return t

## USERS

def get_all_users():
    r = requests.get (url = api_users, headers = auth_headers, verify = ssl_verity_cert)
    t = PrettyTable(['ID', 'Username', 'Email', 'Activated', 'Last Seen', 'Joined'])
    json_data = r.json()
    if r.status_code == 200:
        for user in json_data['data']:
            user_id = user['id']
            user_username = user['attributes']['username']
            user_email = user['attributes']['email']
            user_activated = user['attributes']['isActivated']
            user_lastseen = user['attributes']['lastSeenTime']
            user_join = user['attributes']['joinTime']
            if user_activated:
                dfl = dateutil.parser.parse(user_lastseen).strftime("%d %b %Y %H:%M")
            else:
                dfl = 'never'
            dfj = dateutil.parser.parse(user_join).strftime("%d %b %Y %H:%M")

            t.add_row([ user_id, user_username, user_email, user_activated, dfl, dfj ])
    return t

def register_user(username, email, password):
    data = {'data': { 'attributes': {'username': username, 'email': email, 'password': password }}}
    r = requests.post (url = api_users, headers = auth_headers, data = json.dumps(data), verify = ssl_verity_cert)
    if r.status_code == 201:
        t = PrettyTable(['ID', 'Username', 'Email', 'Status'])
        id = r.json()['data']['id']
        t.add_row([ id, username, email, 'created'])
    if r.status_code == 422:
        t = PrettyTable(['Username', 'Email', 'Status'])
        t.add_row([ username, email, errors(r.json())['detail']])
    return t

def delete_user_by_id(id):
    api_delete_user = api_users + '/' + id
    r = requests.delete (url = api_delete_user, headers = auth_headers, verify = ssl_verity_cert)
    t = PrettyTable(['ID', 'Status'])
    if r.status_code == 204:
        t.add_row([ id, 'deleted'])
    else:
        t.add_row([ id, errors(r.json())['code']])
    return t

if __name__ == '__main__':
    FParse()
