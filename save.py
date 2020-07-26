import pickle
"""
module using pickle to save and load values and classes in and out of memory / external files

used for saving settings and progress between sessions
"""


def get_open_arguments(save_type, save_module, save_number, resource_path, additional_path, read):
    """

    :param save_type:
    :param save_module:
    :param save_number:
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path:
    :param read:
    :return:
    """
    if read:
        opening_type = 'rb'
    else:
        opening_type = 'wb'
    return resource_path('saves/' + additional_path + save_module + str(save_number) + '.' + save_type), opening_type


def save(save_object, save_type, save_module, save_number, resource_path, additional_path=''):
    """

    :param save_object:
    :param save_type:
    :param save_module:
    :param save_number:
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path: str; additional path, if file is not directly in saves directory
    """
    file_name, opening_type = get_open_arguments(save_type, save_module, save_number, resource_path, additional_path,
                                                 False)
    with open(file_name, opening_type) as open_file:
        pickle.dump(save_object, open_file)


def load(save_type, save_module, save_number, resource_path, additional_path=''):
    """

    :param save_type:
    :param save_module:
    :param save_number:
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path:
    :return:
    """
    file_name, opening_type = get_open_arguments(save_type, save_module, save_number, resource_path, additional_path,
                                                 True)
    with open(file_name, opening_type) as open_file:
        return pickle.load(open_file)
