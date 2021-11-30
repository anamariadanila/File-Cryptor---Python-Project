import os.path


class FileCryptor:

    def exceptions(self, input_file_path, passwd):
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

    def encrypt(self, input_file_path, passwd):

        self.exceptions(input_file_path, passwd)

        current_index = 0

        pass_len = len(passwd)

        output_path = f"Encrypted/{os.path.basename(input_file_path)}.crypted"

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
                    output.write(bytearray(crypted_bytes))

    def decrypt(self, input_file_path, passwd):

        self.exceptions(input_file_path, passwd)

        current_index = 0

        pass_len = len(passwd)

        decrypted_file_path = os.path.basename(input_file_path).removesuffix(".crypted")

        output_path = f"Decrypted/{decrypted_file_path}"

        with open(output_path, "wb") as output:
            with open(input_file_path, "rb") as input_file:
                while True:
                    data = input_file.read(1024)
                    if not data:
                        break
                    crypted_bytes = []
                    for byte in data:
                        new_byte = ((int(byte) - ord(passwd[current_index % pass_len])) % 256)
                        crypted_bytes.append(new_byte)
                        current_index += 1
                    output.write(bytearray(crypted_bytes))
