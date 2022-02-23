import time
import taichi as ti
from pyinstrument import Profiler
from pyinstrument.renderers import ConsoleRenderer

ti.init(arch=ti.cpu)
a = ti.ndarray(float, 2048*2048)

@ti.kernel
def fill_half(a: ti.any_arr()):
    for I in a:
        a[I] = 0.5

fill_half(a)
profiler = Profiler()
profiler.start()
fill_half(a)
session = profiler.stop()
profile_renderer = ConsoleRenderer(unicode=True, color=True, show_all=True)
print(profile_renderer.render(session))


