import taichi as ti

ti.init(arch=ti.vulkan)

a = ti.ndarray(float, 8)

a[1] = 0.1

print(a[1])
