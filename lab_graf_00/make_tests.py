from os import listdir

def generate_tests(catalogue):
    file_list = listdir(catalogue)
    return sorted(file_list)
