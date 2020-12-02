import struct, numpy


VERSION_0 = 0
SUPPORT_VERSIONS = (VERSION_0, )
CURRENT_VERSION = SUPPORT_VERSIONS[-1]

# attributes
LOCATION = 0
VELOCITY = 1

FLOAT_32 = 'f'
U_INT_8 = 'B'
U_INT_16 = 'H'
U_INT_32 = 'I'

attributes_names = {
    LOCATION: 'loc',
    VELOCITY: 'vel'
}

attributes_dict = {
    LOCATION: ('location', 3, FLOAT_32),
    VELOCITY: ('velocity', 3, FLOAT_32)
}
format_size = {
    FLOAT_32: 4,
    U_INT_8: 1,
    U_INT_16: 2,
    U_INT_32: 4
}
formats = {
    U_INT_8: 0,
    U_INT_16: 1,
    U_INT_32: 2,
    FLOAT_32: 3
}
formats_keys = {
    0: U_INT_8,
    1: U_INT_16,
    2: U_INT_32,
    3: FLOAT_32
}


class ParticlesCache:
    def __init__(self):
        self.version = CURRENT_VERSION
        self.particles_count = None
        self.attributes = [LOCATION, ]
        self.attributes_values = {
            LOCATION: [],
        }

    def add_attribute(self, attribute_id):
        for attribute in self.attributes:
            if attribute_id == attribute:
                return
        self.attributes.append(attribute_id)

    def remove_attribute(self, attribute_id):
        for index, attribute in enumerate(self.attributes):
            if attribute_id == attribute:
                del self.attributes[index]

    def save(self, psys, file_path):
        data = bytearray()
        data.extend(struct.pack('I', len(self.attributes)))
        for attr_id in self.attributes:
            data.extend(struct.pack('I', attr_id))
        with open(file_path + '.bin', 'wb') as file:
            file.write(data)
        particles_count = len(psys.particles)
        for attribute in self.attributes:
            attr_values = numpy.zeros(particles_count * 3, dtype=numpy.float32)
            attr_name = attributes_dict[attribute][0]
            psys.particles.foreach_get(attr_name, attr_values)
            attr_file_name = attributes_names[attribute]
            attr_file_path = '{}_{}.npy'.format(file_path, attr_file_name)
            with open(attr_file_path, 'wb') as attr_file:
                attr_values.tofile(attr_file)

    def read(self, file_path):
        with open(file_path + '.bin', 'rb') as file:
            data = bytearray(file.read())
        p = 0
        attr_count = struct.unpack('I', data[p : p + 4])[0]
        p += 4
        par_attrs = {}
        for attr_index in range(attr_count):
            attr_id = struct.unpack('I', data[p : p + 4])[0]
            p += 4
            attr_name = attributes_names[attr_id]
            attr_file_path = '{}_{}.npy'.format(file_path, attr_name)
            with open(attr_file_path, 'rb') as npy_file:
                par_attrs[attr_id] = numpy.fromfile(npy_file, dtype=numpy.float32)
        return par_attrs
