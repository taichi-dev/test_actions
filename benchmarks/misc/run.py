import os

from membound import MemoryBound
from taichi.core import ti_core as _ti_core
from utils import arch_name, datatime_with_format, dump2json

import taichi as ti

benchmark_suites = [MemoryBound]
benchmark_archs = [ti.cpu, ti.cuda]


class BenchmarkInfo:
    def __init__(self, pull_request_id, commit_hash):
        self.pull_request_id = pull_request_id  #int
        self.commit_hash = commit_hash  #str
        self.archs = []  #list ['x64','CUDA','Vulkan', ...]
        self.datetime = []  #list [begin, end]


class PerformanceMonitoring:
    def __init__(self, arch):
        self.suites = []
        self.arch = arch
        for suite in benchmark_suites:
            self.suites.append(suite(arch))

    def run(self):
        print(f'Arch : {arch_name(self.arch)} Running...')
        for suite in self.suites:
            suite.run()

    def save_to_json(self, file_dir='./'):
        #arch info
        arch_dict = {}
        arch_dict['arch_name'] = arch_name(self.arch)
        arch_dict['suites'] = [suite.suite_name for suite in self.suites]
        info_path = os.path.join(file_dir, '_info.json')
        info_str = dump2json(arch_dict)
        with open(info_path, 'w') as f:
            print(info_str, file=f)
        #suite info
        for suite in self.suites:
            #suite folder
            suite_path = os.path.join(file_dir, suite.suite_name)
            os.makedirs(suite_path)
            #suite info
            info_path = os.path.join(suite_path, '_info.json')
            info_str = suite.get_suite_info()
            with open(info_path, 'w') as f:
                print(info_str, file=f)
            #cases info
            suite.save_to_json(suite_path)

    def save_to_markdown(self, arch_dir='./'):
        current_time = datatime_with_format()
        commit_hash = _ti_core.get_commit_hash()  #[:8]
        for s in self.suites:
            file_name = f'{s.suite_name}.md'
            path = os.path.join(arch_dir, s.suite_name, file_name)
            with open(path, 'w') as f:
                lines = [
                    f'commit_hash: {commit_hash}\n',
                    f'datatime: {current_time}\n'
                ] + s.get_markdown_str()
                for line in lines:
                    print(line, file=f)


def check_supported(arch_list):
    for arch in arch_list:
        for suite in benchmark_suites:
            if arch not in suite.supported_archs:
                raise RuntimeError(
                    'arch[' + arch_name(arch) +
                    '] does not exist in SuiteInfo.supported_archs of class ' +
                    suite.__name__)


def main():
    # TODO parser & test_archs = sys.argv[1]
    test_archs = benchmark_archs  #default
    check_supported(test_archs)

    result_file_name = 'results'
    benchmark_dir = os.path.join(os.getcwd(), result_file_name)
    os.makedirs(benchmark_dir)

    pull_request_id = os.environ.get('PULL_REQUEST_NUMBER')
    print(f'pull_request_id = {pull_request_id}')
    commit_hash = _ti_core.get_commit_hash()  #[:8]
    info = BenchmarkInfo(pull_request_id, commit_hash)
    info.datetime.append(datatime_with_format())  #start time
    for arch in test_archs:
        #make dir
        arch_dir = os.path.join(benchmark_dir, arch_name(arch))
        os.makedirs(arch_dir)
        #init & run
        impl = PerformanceMonitoring(arch)
        impl.run()
        #append info
        info.archs.append(arch_name(arch))
        #save result
        impl.save_to_json(arch_dir)
        impl.save_to_markdown(arch_dir)
    info.datetime.append(datatime_with_format())  #end time
    #save benchmark info
    info_path = os.path.join(benchmark_dir, '_info.json')
    info_str = dump2json(info)
    with open(info_path, 'w') as f:
        print(info_str, file=f)


if __name__ == '__main__':
    main()
