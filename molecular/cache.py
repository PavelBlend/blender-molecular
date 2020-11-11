import struct


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
        particles_count = len(psys.particles)
        data.extend(struct.pack(U_INT_32, particles_count))
        data.extend(struct.pack(U_INT_8, len(self.attributes)))
        for attribute in self.attributes:
            data.extend(struct.pack(U_INT_8, attribute))
            attr_name, attr_length, attr_format = attributes_dict[attribute]
            data.extend(struct.pack(U_INT_8, attr_length))
            data.extend(struct.pack(U_INT_8, formats[attr_format]))
            attr_values = [None, ] * particles_count * attr_length
            psys.particles.foreach_get(attr_name, attr_values)
            for value in attr_values:
                bin_value = struct.pack(attr_format, value)
                data.extend(bin_value)
        with open(file_path, 'wb') as file:
            file.write(data)

    def read(self, file_path):
        with open(file_path, 'rb') as file:
            data = bytearray(file.read())
        p = 0
        particles_count = struct.unpack(U_INT_32, data[p : p + 4])[0]
        p += 4
        self.particles_count = particles_count
        attributes_count = struct.unpack(U_INT_8, data[p : p + 1])[0]
        p += 1
        par_attrs = {}
        for _ in range(attributes_count):
            attribute = struct.unpack(U_INT_8, data[p : p + 1])[0]
            p += 1
            attr_length = struct.unpack(U_INT_8, data[p : p + 1])[0]
            p += 1
            attr_format = struct.unpack(U_INT_8, data[p : p + 1])[0]
            p += 1
            attr_format = formats_keys[attr_format]
            size = format_size[attr_format]
            par_attrs[attribute] = [None, ] * particles_count * attr_length
            for index in range(particles_count * attr_length):
                value = struct.unpack(attr_format, data[p : p + size])[0]
                p += size
                par_attrs[attribute][index] = value
        return par_attrs
