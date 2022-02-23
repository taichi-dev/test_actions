import os
import numpy as np
import taichi as ti

this_dir = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(this_dir, 'ell.json')

ti.init(arch=ti.x64)

def test_mesh_for(cell_reorder=False, vert_reorder=False, extra_tests=True):
    mesh_builder = ti.Mesh.Tet()
    mesh_builder.verts.place({'t': ti.i32}, reorder=vert_reorder)
    mesh_builder.cells.place({'t': ti.i32}, reorder=cell_reorder)
    mesh_builder.cells.link(mesh_builder.verts)
    mesh_builder.verts.link(mesh_builder.cells)
    mesh_builder.cells.link(mesh_builder.cells)
    mesh_builder.verts.link(mesh_builder.verts)
    model = mesh_builder.build(ti.Mesh.load_meta(model_file_path))

    @ti.kernel
    def cell_vert():
        for c in model.cells:
            for j in range(c.verts.size):
                c.t += c.verts[j].id

    cell_vert()

test_mesh_for(False, False)
