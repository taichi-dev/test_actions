import json
import os
import re
import sys


def main():
    num = os.environ.get('PULL_REQUEST_NUMBER')
    print(f'PULL_REQUEST_NUMBER = {num}')


if __name__ == '__main__':
    main()
