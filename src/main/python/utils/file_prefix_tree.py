import os

from anytree import Node


def to_name(folder):
    return folder.split(os.path.sep)[-2]


# TODO check if i need this.
def find_next_nested_folder_prefix_in(nested_folders):
    for nested_folder in nested_folders:
        if nested_folder == os.path.sep:
            continue
        return nested_folder


def add_all_folders(parent, current_folder, paths):
    relative_paths = [os.path.relpath(path, current_folder) for path in paths]
    relative_paths.sort()
    num_files = 0
    nested_folders = []
    for relative_path in relative_paths:
        split = os.path.split(relative_path)
        if not split[0]:
            num_files += 1
        else:
            nested_folders.append(str(split[0]))
    current_folder_node = Node(to_name(current_folder), parent, files=num_files)
    tested_prefixes = []
    if nested_folders:
        for nested_folder in nested_folders:
            if nested_folder == os.path.sep:
                continue
            nested_folder_name = current_folder + nested_folder.split(os.path.sep)[0] + os.path.sep
            if nested_folder_name in tested_prefixes:
                continue
            else:
                nested_folder_paths = [path for path in paths if path.startswith(nested_folder_name)]
                tested_prefixes.append(nested_folder_name)
                add_all_folders(current_folder_node, nested_folder_name, nested_folder_paths)


class FilePrefixTree:

    def __init__(self, root_name, paths):
        # paths = [os.path.normpath(path) for path in paths]
        # paths = [os.path.normcase(path) for path in paths]
        self.root = Node("ROOT")
        add_all_folders(self.root, root_name, paths)
        if paths:
            self.basedir = self.root.children[0]
