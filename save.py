import pickle
"""
module using pickle to save and load values and classes in and out of memory / external files

used for saving settings and progress between sessions
"""


def get_open_arguments(save_type, save_module, save_number, resource_path, additional_path, read):
    """
    :param save_type: str; 3 characters, saved object's type
    :param save_module: str; module the saved object is in
    :param save_number: int; number used to distinguish between objects of same module
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path: str; directory the file is in after base path + saves/
    :param read: bool; information is loaded and thus read
    :return: str, str; file's resource path and opening type
    """
    opening_type = 'rb' if read else 'wb'
    return resource_path('saves/' + additional_path + save_module + str(save_number) + '.' + save_type), opening_type


def save(save_object, save_type, save_module, save_number, resource_path, additional_path=''):
    """
    saves an object to a file with pickle

    :param save_object: object that is saved
    :param save_type: str; 3 characters, saved object's type
    :param save_module: str; module the saved object is in
    :param save_number: int; number used to distinguish between objects of same module
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path: str; additional path, if file is not directly in saves directory
    """
    file_name, opening_type = get_open_arguments(save_type, save_module, save_number, resource_path, additional_path,
                                                 False)
    with open(file_name, opening_type) as open_file:
        pickle.dump(save_object, open_file)


def load(save_type, save_module, save_number, resource_path, additional_path=''):
    """
    loads an object from a file with pickle
    :param save_type: str; 3 characters, saved object's type
    :param save_module: str; module the saved object is in
    :param save_number: int; number used to distinguish between objects of same module
    :param resource_path: Func; returns the resource path to a relative path
    :param additional_path: str; additional path, if file is not directly in saves directory
    :return: object pickeld in file
    """
    file_name, opening_type = get_open_arguments(save_type, save_module, save_number, resource_path, additional_path,
                                                 True)
    with open(file_name, opening_type) as open_file:
        return pickle.load(open_file)
