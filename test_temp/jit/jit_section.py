import time
import taichi as ti
#from pyinstrument import Profiler
#from pyinstrument.renderers import ConsoleRenderer

from line_profiler import LineProfiler

ti.init(arch=ti.cpu)
a = ti.ndarray(float, 2048*2048)

@ti.kernel
def fill_half(a: ti.any_arr()):
    for I in a:
        a[I] = 0.5

lprofiler = LineProfiler()
lprofiler.add_function(ti.lang.kernel_impl.Kernel.func__)
lp_wrapper = lprofiler(fill_half(a))
lp_wrapper()

lprofiler.print_stats()
