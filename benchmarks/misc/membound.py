import json
import os
import time

from membound_cases import fill, reduction, saxpy
from utils import (arch_name, dtype2str, dump2json, geometric_mean, kibibyte,
                   md_table_header, repeat_times, size2str)

import taichi as ti


class SuiteInfo:
    cases = [fill, saxpy, reduction]
    supported_archs = [ti.x64, ti.cuda]
    dtype = [ti.i32, ti.i64, ti.f32, ti.f64]
    dsize = [(4**i) * kibibyte for i in range(1, 10)]  #[4KB,16KB...256MB]
    repeat = 10
    evaluator = [geometric_mean]


class CaseResult:
    def __init__(self, name, arch, dtype, dsize, evaluator):
        self.test_name = name
        self.test_arch = arch
        self.data_type = dtype
        self.data_size = dsize  #list
        self.min_time_in_us = []  #list
        self.evaluator = evaluator

    def result_to_markdown(self):
        string = '|' + self.test_name + '.' + dtype2str[self.data_type] + '|'
        string += ''.join(
            str(round(time, 4)) + '|' for time in self.min_time_in_us)
        string += ''.join(
            str(round(item(self.min_time_in_us), 4)) + '|'
            for item in self.evaluator)
        return string

    def result_to_dict(self):
        result_dicts = {}
        for i in range(len(self.data_size)):
            dsize = self.data_size[i]
            reslut_name = size2str(dsize).replace('.0', '')
            repeat = repeat_times(self.test_arch, dsize, SuiteInfo.repeat)
            elapsed_time = self.min_time_in_us[i]
            item_dict = {
                'dsize_byte': dsize,
                'repeat': repeat,
                'elapsed_time_ms': elapsed_time
            }
            result_dicts[reslut_name] = item_dict
        return result_dicts


class CaseImpl:
    def __init__(self, func, arch, data_type, data_size):
        self.func = func
        self.name = func.__name__
        self.env = None
        self.device = None
        self.arch = arch
        self.data_type = data_type
        self.data_size = data_size
        self.case_results = []

    def run(self):
        for dtype in self.data_type:
            ti.init(kernel_profiler=True, arch=self.arch)
            print("TestCase[%s.%s.%s]" %
                  (self.func.__name__, arch_name(self.arch), dtype2str[dtype]))
            result = CaseResult(self.name, self.arch, dtype, self.data_size,
                                SuiteInfo.evaluator)
            for size in self.data_size:
                print("data_size = %s" % (size2str(size)))
                result.min_time_in_us.append(
                    self.func(self.arch, dtype, size, SuiteInfo.repeat))
                time.sleep(0.2)
            self.case_results.append(result)

    def to_markdown(self):
        header = '|kernel elapsed time(ms)' + ''.join(
            '|' for i in range(len(self.data_size) + len(SuiteInfo.evaluator)))
        lines = [header]
        for result in self.case_results:
            lines.append(result.result_to_markdown())
        return lines


class MemoryBound:
    suite_name = 'memorybound'
    supported_archs = SuiteInfo.supported_archs

    def __init__(self, arch):
        self.arch = arch
        self.cases_impl = []
        for case in SuiteInfo.cases:
            self.cases_impl.append(
                CaseImpl(case, arch, SuiteInfo.dtype, SuiteInfo.dsize))

    def run(self):
        for case in self.cases_impl:
            case.run()

    def get_suite_info(self):
        info_dict = {
            'cases': [func.__name__ for func in SuiteInfo.cases],
            'dtype': [dtype2str[type] for type in SuiteInfo.dtype],
            'dsize': [size for size in SuiteInfo.dsize],
            'repeat': [
                repeat_times(self.arch, size, SuiteInfo.repeat)
                for size in SuiteInfo.dsize
            ],
            'evaluator': [func.__name__ for func in SuiteInfo.evaluator]
        }
        return dump2json(info_dict)

    def get_markdown_str(self):
        lines = []
        lines += md_table_header(self.suite_name, self.arch, SuiteInfo.dsize,
                                 SuiteInfo.repeat, SuiteInfo.evaluator)
        for case in self.cases_impl:
            lines += case.to_markdown()
        lines.append('')
        return lines

    def save_to_json(self, suite_path='./'):
        #save suite benchmark result to case.json
        for case in self.cases_impl:  #[fill,saxpy,reduction]
            case_path = os.path.join(suite_path, (case.name + '.json'))
            results_dict = {}
            for result in case.case_results:
                type_str = dtype2str[result.data_type]
                result_name = self.suite_name + '.' + case.name + '.' + arch_name(
                    self.arch) + '.' + type_str
                results_dict[result_name] = result.result_to_dict()
            with open(case_path, 'w') as f:
                case_str = dump2json(results_dict)
                print(case_str, file=f)
