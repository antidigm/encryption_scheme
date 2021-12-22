import sys
from encryption_helper import *

target_file = sys.argv[1]

target_filepath = os.path.join(os.getcwd(), target_file)

print(target_filepath)

name = os.path.splitext(target_file)[0]

print('directory to decrypt is : ' + target_file)
print('basename is: ' + name)

salt_path = os.getcwd() + "/" + name + '.salt'

print(salt_path)

salt = read_salt_file(salt_path)

print(str(salt))

password = ask_password()

print(password)

decrypt_file(target_filepath, password, salt)

unpack_archive(name + '.zip')
