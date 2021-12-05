import hashlib
import os.path


def __exceptions(input_file_path, passwd):
    if not isinstance(input_file_path, str):
        raise Exception("input_file_path must be a string")

    if not os.path.exists(input_file_path):
        raise Exception(f"{input_file_path} does not exist")

    if not os.path.isfile(input_file_path):
        raise Exception(f"{input_file_path} is not a file")

    if not isinstance(passwd, str):
        raise Exception("passwd must be a string")

    if len(passwd) == 0:
        raise Exception("passwd must have a non-zero length")


def encrypt(input_file_path, passwd):

    __exceptions(input_file_path, passwd)

    current_index = 0

    pass_len = len(passwd)

    output_path = f"Encrypted/{os.path.basename(input_file_path)}.crypted"

    md5 = hashlib.md5()

    with open(output_path, "wb") as output:
        with open(input_file_path, "rb") as input_file:
            while True:
                data = input_file.read(1024)
                if not data:
                    break
                crypted_bytes = []
                for byte in data:
                    new_byte = ((int(byte) + ord(passwd[current_index % pass_len])) % 256)
                    crypted_bytes.append(new_byte)
                    current_index += 1
                md5.update(data)
                output.write(bytearray(crypted_bytes))
        hex_digest = md5.hexdigest()
        output.write(bytes(hex_digest, "utf-8"))
        print(hex_digest)


def decrypt(input_file_path, passwd):

    __exceptions(input_file_path, passwd)

    current_index = 0

    pass_len = len(passwd)

    decrypted_file_path = os.path.basename(input_file_path).removesuffix(".crypted")

    output_path = f"Decrypted/{decrypted_file_path}"

    md5 = hashlib.md5()

    with open(output_path, "wb") as output:
        with open(input_file_path, "rb") as input_file:

            # getting the hash from the end of the file
            input_file.seek(-32, os.SEEK_END)
            hex_digest = input_file.read(32)
            hex_digest = hex_digest.decode("utf-8")
            input_file.seek(0, os.SEEK_SET)

            # getting number of bytes
            nb_bytes = os.stat(input_file_path).st_size

            while True:
                data = input_file.read(1024)
                if not data:
                    break
                decrypted_bytes = []
                for byte in data:
                    if current_index >= nb_bytes - 32:
                        break
                    new_byte = ((int(byte) - ord(passwd[current_index % pass_len])) % 256)
                    decrypted_bytes.append(new_byte)
                    current_index += 1
                if len(decrypted_bytes):
                    output.write(bytearray(decrypted_bytes))
                    md5.update(bytearray(decrypted_bytes))
        if hex_digest == md5.hexdigest():
            print(hex_digest)
            print("The password is correct")



