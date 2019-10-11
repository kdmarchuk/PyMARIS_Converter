import h5py

"""
tid = h5py.h5t.C_S1.copy()
tid.set_size(2)
tid.set_strpad(h5py.h5t.STR_NULLTERM)
H5T_C_S1_64 = h5py.Datatype(tid)
"""


def write_attribute(group_name, attribute_name, attribute_value):
    group_name.attrs.create(attribute_name, [x for x in attribute_value], dtype=h5py.h5t.C_S1)
