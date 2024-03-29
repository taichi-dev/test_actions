import taichi as ti
from tests import test_utils

from .bls_test_template import bls_particle_grid


@test_utils.test(require=ti.extension.bls)
def test_scattering():
    bls_particle_grid(N=128, ppc=10, block_size=8, scatter=True, use_offset=False)


@test_utils.test(require=ti.extension.bls)
def test_scattering_offset():
    bls_particle_grid(N=128, ppc=10, block_size=8, scatter=True, use_offset=True)


@test_utils.test(require=ti.extension.bls)
def test_scattering_two_pointer_levels():
    bls_particle_grid(N=128, ppc=10, block_size=8, scatter=True, pointer_level=2, use_offset=False)


@test_utils.test(require=ti.extension.bls)
def test_gathering():
    bls_particle_grid(N=128, ppc=10, block_size=8, scatter=False, use_offset=False)


@test_utils.test(require=ti.extension.bls)
def test_gathering_offset():
    bls_particle_grid(N=128, ppc=10, block_size=8, scatter=False, use_offset=True)


# TODO: debug mode behavior of assume_in_range
