import taichi as ti
import time

ti.init(arch=ti.cuda)

print("test to numpy")
N = 2048*2048

a = ti.ndarray(ti.f32, N)
a.to_numpy

iterations = 100000
t_start = time.perf_counter()
for i in range(iterations):
    a.to_numpy
t_used = time.perf_counter() - t_start 
print('total time:', "{:.3f}".format(t_used*1000), "ms")


