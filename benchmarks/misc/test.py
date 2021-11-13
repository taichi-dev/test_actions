import json
import os
import re
import sys


def main():
    github_context = os.environ.get('GITHUB_CONTEXT')
    github_info_dict = {}
    github_info_dict = json.loads(github_context)
    pr_number = re.sub("\D", "", github_info_dict["ref"])
    os.environ['PULL_REQUEST_NUMBER'] = pr_number
    print(os.environ.get('PULL_REQUEST_NUMBER'))


if __name__ == '__main__':
    main()
