from os import listdir

# function takes 1 argument:
# catalogue - address of directory to read all the files from
# returns list of all files in given directory sorted alphabetically
def generate_tests(catalogue):
    file_list = listdir(catalogue)
    return sorted(file_list)
