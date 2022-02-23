import taichi as ti

ti.init(arch=ti.cuda, log_level=ti.TRACE)
#ti.init(arch=ti.cuda)

a = ti.ndarray(float, 16)

@ti.kernel
def p():
    print('p')


p()
