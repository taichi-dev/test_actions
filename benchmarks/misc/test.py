
import sys
import os
import json
import jsbeautifier
import datetime
import re

perf_monitoring_dir = os.environ.get('PERF_MONITORING_DIR')
if perf_monitoring_dir is None:
    raise RuntimeError('Missing environment variable PERF_MONITORING_DIR')

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
    # info_path = os.path.join(perf_monitoring_dir, 'context.json')
    #traverse pr_results
    pr_dict = {}
    # with open(info_path, 'r') as f:
    pr_dict = json.loads(github_context)
    pr_number = re.sub("\D","",pr_dict["ref"])
    print(pr_dict["ref"])
    print(pr_number)
    # print(dump2json(pr_dict))

if __name__ == '__main__':
    main()