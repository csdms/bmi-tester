# cython: language_level=3
import contextlib
import os
import pkg_resources

from libc.stdlib cimport free, malloc
from libc.string cimport strcpy


@contextlib.contextmanager
def suppress_stdout():
    null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
    # Save the actual stdout (1) and stderr (2) file descriptors.
    save_fds = [os.dup(1), os.dup(2)]

    os.dup2(null_fds[0], 1)
    os.dup2(null_fds[1], 2)

    yield

    # Re-assign the real stdout/stderr back to (1) and (2)
    os.dup2(save_fds[0], 1)
    os.dup2(save_fds[1], 2)
    # Close the null files
    for fd in null_fds + save_fds:
        os.close(fd)


cdef extern from "udunits2.h":
    ctypedef struct ut_system:
        pass
    ctypedef struct ut_unit:
        pass

    ut_system* ut_read_xml(const char * path)
    void ut_free_system(ut_system* system)
    ut_unit* ut_parse(const ut_system* system, const char* string, int encoding)
    int ut_are_convertible(const ut_unit* unit1, const ut_unit* unit2)
    int ut_format(const ut_unit* unit, char* buf, size_t size, unsigned opts)


cdef class Units:
    cdef ut_system* _c_system
    cdef char[2048] STR_BUFFER
    cdef char* _filepath

    def __cinit__(self):
        try:
            filepath = os.environ["UDUNITS2_XML_PATH"]
        except KeyError:
            filepath = pkg_resources.resource_filename(
                "bmi_tester", "data/udunits/udunits2.xml"
            )
        as_bytes = str(filepath).encode("utf-8")
        self._filepath = <char*>malloc((len(as_bytes) + 1) * sizeof(char))
        strcpy(self._filepath, as_bytes)

        with suppress_stdout():
            self._c_system = ut_read_xml(self._filepath)

        # self._c_system = ut_read_xml(NULL)

    def norm(self, units):
        unit = ut_parse(self._c_system, units.encode("utf-8"), 0)
        str_len = ut_format(unit, self.STR_BUFFER, 2048, 4 | 8)
        return self.STR_BUFFER

    def is_valid(self, units):
        return ut_parse(self._c_system, units.encode("utf-8"), 0) != NULL

    def is_time(self, units):
        src_unit = ut_parse(self._c_system, units.encode("utf-8"), 0)
        dst_unit = ut_parse(self._c_system, "s".encode("utf-8"), 0)
        return bool(ut_are_convertible(src_unit, dst_unit))

    def __dealloc__(self):
        ut_free_system(self._c_system)
        free(self._filepath)
        self._c_system = NULL
        self._filepath = NULL
