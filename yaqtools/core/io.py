import os


def get_list_files(diretory, file_pattern):
    """
    Find list of files in a directory that matches a certain file pattern

    Parameters
    ----------
    diretory: directory to scan
    file_pattern: file pattern to find

    Returns
    -------

    """
    lst_file = []
    for root, dirs, files in os.walk(diretory):
        for file in files:
            if file.endswith(file_pattern):
                lst_file.append(os.path.join(root, file))

    return lst_file
