import taichi as ti
import pytest
import platform


@pytest.mark.skipif(platform.system() == "Windows",
                    reason="Too much virtual memory for github windows env.")
@ti.test(debug=True, gdb_trigger=False, arch=[ti.cpu])
def test_indices_assert():

    overflow = ti.field(int, (334, 334, 334, 2 * 10))

    @ti.kernel
    def access_overflow():
        overflow[0, 0, 0, 0] = 10
        print(overflow[333, 333, 333, 0])

    with pytest.raises(RuntimeError,
                       match='The indices provided are too big!'):
        access_overflow()
