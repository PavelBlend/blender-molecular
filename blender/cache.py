import struct

import numpy


# attributes ids
LOCATION = 0
VELOCITY = 1

attribute_file = {
    LOCATION: 'loc',
    VELOCITY: 'vel'
}
attribute_name = {
    LOCATION: 'location',
    VELOCITY: 'velocity'
}

UINT_FMT = 'I'
UINT_SZ = 4
VEC_LEN = 3
VEC_TYPE = numpy.float32
EXT_HEAD = '.bin'
EXT_PART = '.npy'


class ParticlesIO:
    def __init__(self):
        self._attrs = [LOCATION, ]

    def add_attr(self, attr_id):
        if not attr_id in self._attrs:
            self._attrs.append(attr_id)

    def write(self, psys, path):

        # -----------
        # write header
        # -----------

        data = bytearray()

        # attributes count
        attr_count = len(self._attrs)
        count_data = struct.pack(UINT_FMT, attr_count)
        data.extend(count_data)

        # attributes ids
        for attr_id in self._attrs:
            id_data = struct.pack(UINT_FMT, attr_id)
            data.extend(id_data)

        head_path = path + EXT_HEAD
        with open(head_path, 'wb') as file:
            file.write(data)

        data.clear()

        # --------------
        # write particles
        # --------------

        par_count = len(psys.particles)

        for attr_id in self._attrs:
            attr_name = attribute_name[attr_id]
            file_name = attribute_file[attr_id]

            file_path = '{}_{}{}'.format(path, file_name, EXT_PART)

            values = numpy.zeros(par_count * VEC_LEN, dtype=VEC_TYPE)
            psys.particles.foreach_get(attr_name, values)

            values.tofile(file_path)

    def read(self, path):
        # -----------
        # write header
        # -----------

        head_path = path + EXT_HEAD

        with open(head_path, 'rb') as file:
            head = bytearray(file.read())

        offs = 0

        count_bytes = head[offs : offs + UINT_SZ]
        attr_count = struct.unpack(UINT_FMT, count_bytes)[0]
        offs += UINT_SZ

        # particle attributes
        attrs = {}

        for _ in range(attr_count):
            id_bytes = head[offs : offs + UINT_SZ]
            attr_id = struct.unpack(UINT_FMT, id_bytes)[0]
            offs += UINT_SZ

            # --------------
            # read particles
            # --------------

            attr_name = attribute_file[attr_id]
            file_path = '{}_{}{}'.format(path, attr_name, EXT_PART)

            with open(file_path, 'rb') as file:
                data = numpy.fromfile(file, dtype=VEC_TYPE)
                attrs[attr_id] = data

        return attrs
