#!/usr/bin/env python3

import html
import re
import subprocess as sp
import sys
import urllib.parse
from youtrack.connection import Connection as YouTrack

yt_url = "https://youtrack.jetbrains.com"
yt = YouTrack(yt_url, token="TOKEN")

project_id = "CPP"
project_single_issue_url = f'{yt_url}/issue'
project_issues_url = f'{yt_url}/issues/{project_id}?q='

clion_issue_re = re.compile(f"^({project_id}-[0-9]+)")

browser_path = '/usr/bin/google-chrome-stable'


def query_issues(search_str):
    return yt.getIssues(project_id, search_str, 0, 10)


def to_query_string(search_str):
    return f'{search_str} sort by: updated desc'


def is_single_issue_id(search_str):
    return re.match(clion_issue_re, search_str)


def main():
    search_string = html.unescape((' '.join(sys.argv[1:])).strip())

    if search_string.endswith('!'):
        query = to_query_string(search_string.rstrip('!').strip())
        results = query_issues(query)
        for r in results:
            attrs = r.to_dict()
            print(f'{attrs["id"]} - {attrs["summary"]}')
    elif search_string == '':
        print('!!-- Type something to search on YouTrack')
        print('!!-- Close your search string with "!" to get suggestions')
    else:
        m = is_single_issue_id(search_string)
        if m:
            search_string = m.group(1)
            query = urllib.parse.quote_plus(search_string)
            url = f'{project_single_issue_url}/{query}'
        else:
            query = urllib.parse.quote_plus(search_string)
            url = f'{project_issues_url}{query}'

        sp.Popen([browser_path] + [url], stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=False)


if __name__ == "__main__":
    main()
