import datetime

from membound import Membound
from taichi.core import ti_core as _ti_core

import taichi as ti

test_suites = [Membound]
test_archs = [ti.cuda]


class PerformanceMonitoring:
    suites = []

    def __init__(self):
        for s in test_suites:
            self.suites.append(s())

    def run(self):
        print("Running...")
        for s in self.suites:
            s.run()

    def write_md(self,path='/home/benchmarkbot/benchmark/'):
        current_time = datetime.datetime.now().strftime("%Y%m%dd%Hh%Mm%Ss")
        commit_hash = _ti_core.get_commit_hash()[:8]
        filename = f'perfresult_{current_time}_{commit_hash}.md'
        #format like perfresult_20211013d20h46m03s_581fdac8.md
        #TODO: get pr id and add to file name perfresult_pr3104_20211013d20h46m03s_581fdac8.md
        with open(path+filename, 'w') as f:
            for arch in test_archs:
                for s in self.suites:
                    lines = s.mdlines(arch)
                    for line in lines:
                        print(line, file=f)
        with open('performance_result.md', 'w') as f: # for /benchamark
            for arch in test_archs:
                for s in self.suites:
                    lines = s.mdlines(arch)
                    for line in lines:
                        print(line, file=f)


p = PerformanceMonitoring()
p.run()
p.write_md()