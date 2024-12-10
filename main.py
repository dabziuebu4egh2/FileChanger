#python3 main.py your_file jpeg kb_size sha256 encoding


import sys
import os
import hashlib

MAGIC_NUMBERS = {
    'jpeg': b'\xFF\xD8\xFF',
    'png': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    'gif': b'\x47\x49\x46\x38',
    'bmp': b'\x42\x4D',
    'pdf': b'\x25\x50\x44\x46',
}

EXTENSIONS = {
    'jpeg': '.jpg',
    'png': '.png',
    'gif': '.gif',
    'bmp': '.bmp',
    'pdf': '.pdf',
}

HASHING_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']
ENCODING_METHODS = [
    'utf-8', 'utf-16', 'ascii', 'latin-1', 
    'windows-1251', 'gbk', 'big5', 'koi8-r', 
    'iso-8859-5', 'windows-1254', 'windows-1256', 'euc-kr'
]

def change_magic_number(file_path, magic_type, target_size_kb='none', hash_algorithm='none', encoding='utf-8'):
    if magic_type not in MAGIC_NUMBERS:
        print(f"Unknown magic type: {magic_type}. Available types: {', '.join(MAGIC_NUMBERS.keys())}")
        return
    if hash_algorithm.lower() not in HASHING_ALGORITHMS + ['none']:
        print(f"Unknown hash algorithm: {hash_algorithm}. Available algorithms: {', '.join(HASHING_ALGORITHMS + ['none'])}")
        return
    if encoding and encoding not in ENCODING_METHODS:
        print(f"Unknown encoding method: {encoding}. Available methods: {', '.join(ENCODING_METHODS)}")
        return

    target_size = None if target_size_kb.lower() == 'none' else int(target_size_kb) * 1024

    with open(file_path, 'r+b') as f:
        f.write(MAGIC_NUMBERS[magic_type])
        current_size = f.tell()
        content = f.read()
        
        if hash_algorithm.lower() != 'none':
            hash_object = hashlib.new(hash_algorithm)
            hash_object.update(content)
            hash_digest = hash_object.digest()
            f.seek(0)
            f.write(MAGIC_NUMBERS[magic_type] + content + hash_digest)
        else:
            f.seek(0)
            f.write(MAGIC_NUMBERS[magic_type] + content)

        if target_size is not None and current_size < target_size:
            f.write(os.urandom(target_size - current_size))
    
    new_file_path = os.path.splitext(file_path)[0] + EXTENSIONS[magic_type]
    os.rename(file_path, new_file_path)
    print(f"Changed magic number of '{file_path}' to {magic_type} and renamed to '{new_file_path}'.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <file_path> <magic_type> [<target_size_kb>] [<hash_algorithm>] [<encoding>]")
        return

    file_path = sys.argv[1]
    magic_type = sys.argv[2]
    target_size_kb = sys.argv[3] if len(sys.argv) > 3 else 'none'
    hash_algorithm = sys.argv[4] if len(sys.argv) > 4 else 'none'
    encoding = sys.argv[5] if len(sys.argv) > 5 else 'utf-8'

    change_magic_number(file_path, magic_type, target_size_kb, hash_algorithm, encoding)

if __name__ == "__main__":
    main()
