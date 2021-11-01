
import sys
import os
import json
import re

def main():
    github_context = os.environ.get('GITHUB_CONTEXT')
    github_info_dict = {}
    github_info_dict = json.loads(github_context)
    pr_number = re.sub("\D","",github_info_dict["ref"])
    set_pr_num_str = f'export PULL_REQUEST_NUMBER={pr_number}'
    print(set_pr_num_str)
    os.system(set_pr_num_str)

if __name__ == '__main__':
    main()