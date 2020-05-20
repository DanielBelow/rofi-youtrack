#!/usr/bin/env python3

import html
import re
import subprocess as sp
import sys
import urllib.parse
from youtrack.connection import Connection as YouTrack

# YouTrack configuration
# https://www.jetbrains.com/help/youtrack/standalone/Manage-Permanent-Token.html#obtain-permanent-token
auth_token = "TOKEN"

# Project specific configuration
project_id = "CPP"

# YouTrack URLs
tracker_url = "https://youtrack.jetbrains.com"

project_single_issue_url = f'{tracker_url}/issue/'
project_issues_search_url = f'{tracker_url}/issues/{project_id}?q='
project_issue_re = re.compile(f"^({project_id}-[0-9]+)")

yt = YouTrack(tracker_url, token=auth_token)

# Browser configuration
browser_path = '/usr/bin/google-chrome-stable'


def query_issues(search_str):
    return yt.getIssues(project_id, search_str, 0, 10)


def to_query_string(search_str):
    return f'{search_str} sort by: updated desc'


def is_single_issue_id(search_str):
    return re.match(project_issue_re, search_str)


def print_results(results):
    for r in results:
        attrs = r.to_dict()
        print(f'{attrs["id"]} - {attrs["summary"]}')


def get_query_and_url(search_string):
    m = is_single_issue_id(search_string)
    if m:
        query = urllib.parse.quote_plus(m.group(1))
        return query, project_single_issue_url

    return urllib.parse.quote_plus(search_string), project_issues_search_url


def main():
    search_string = html.unescape((' '.join(sys.argv[1:])).strip())

    if search_string.endswith('!'):
        query = to_query_string(search_string.rstrip('!').strip())
        results = query_issues(query)
        print_results(results)
    elif search_string == '':
        print('!!-- Type something to search on YouTrack')
        print('!!-- Close your search string with "!" to get suggestions')
    else:
        (query, base_url) = get_query_and_url(search_string)
        url = f'{base_url}{query}'
        sp.Popen([browser_path] + [url], stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=False)


if __name__ == "__main__":
    main()
