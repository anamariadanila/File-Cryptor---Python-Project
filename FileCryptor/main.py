import sys

import FileCryptor as fc


def get_arguments():
    if len(sys.argv) != 4:
        raise Exception("You must enter 3 parameters in this order: mode, file path and password")
    return sys.argv[1:]


def main():
    try:
        mode, file_path, passwd = get_arguments()
        if not (mode == "crypt" or mode == "decrypt"):
            raise Exception("Mode must be crypt or decrypt")
        if mode == "crypt":
            fc.encrypt(file_path, passwd)
        if mode == "decrypt":
            fc.decrypt(file_path, passwd)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
