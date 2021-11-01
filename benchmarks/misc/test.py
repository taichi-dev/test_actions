
import sys
import os
import json
import jsbeautifier
import datetime
import re

def dump2json(obj):
    if type(obj) is dict:
        obj2dict = obj
    else:
        obj2dict = obj.__dict__
    options = jsbeautifier.default_options()
    options.indent_size = 4
    return jsbeautifier.beautify(json.dumps(obj2dict), options)

def main():
    github_context = os.environ.get('GITHUB_CONTEXT')
    github_info_dict = {}
    github_info_dict = json.loads(github_context)
    pr_number = re.sub("\D","",github_info_dict["ref"])
    print(github_info_dict["ref"])
    print(pr_number)

if __name__ == '__main__':
    main()