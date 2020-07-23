cdef extern from "udunits2.h":
    ctypedef struct ut_system:
        pass
    ctypedef struct ut_unit:
        pass

    ut_system* ut_read_xml(const char * path)
    ut_unit* ut_parse(const ut_system* system, const char* string, int encoding)
    int ut_are_convertible(const ut_unit* unit1, const ut_unit* unit2)
    int ut_format(const ut_unit* unit, char* buf, size_t size, unsigned opts)


cdef class Units:
    cdef ut_system* _c_system
    cdef char[2048] STR_BUFFER

    def __cinit__(self):
        self._c_system = ut_read_xml(NULL)

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
