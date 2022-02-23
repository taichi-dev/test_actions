import time
import taichi as ti

print('end2end time')

t_start = time.perf_counter()
ti.init(arch=ti.cpu)
t_used = time.perf_counter() - t_start
print('ti.init time:', "{:.8f}".format(t_used), "s")

a = ti.ndarray(float, 2048*2048)

@ti.kernel
def fill_half(a: ti.any_arr()):
    for I in a:
        a[I] = 0.5

t_start = time.perf_counter()
fill_half(a)
t_used = time.perf_counter() - t_start
print('first execution time:', "{:.8f}".format(t_used), "s")


t_start = time.perf_counter()
fill_half(a)
t_used = time.perf_counter() - t_start
print('second execution time:', "{:.8f}".format(t_used), "s")

