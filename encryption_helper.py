# this library contains the functions necissary to build the described database
import os
from distutils.dir_util import copy_tree
import random
import string
import getpass
import shutil

##### database creation #####

def choose_target_directory():
    #reminder to add file picker later
    if True:
        return os.getcwd()
    else:
        #add file picker
        pass

def input_name():
    name = input('type database name: ')
    return name

def make_database(dir, name):
    database_path = os.path.join(dir, name)
    os.mkdir(database_path)
    return database_path

def populate_database(target_database_path, test_database_path):
    #populates the created database with test data

    # Copy the content of source to destination
    copy_tree(test_database_path, target_database_path)

    #get database name for displaying
    database_name = os.path.basename(target_database_path)

    print("database: " + database_name + " populated successfully")

##### database encryption #####

# salt creation and saving

def generate_salt_string(length):
    #initiate a string to hold characters
    string_holder = ""
    #generate a list of choices for random selection
    choices = string.ascii_letters + string.digits + string.punctuation
    #for a given length requested, recursively add characters
    for i in range(length):
        #add a random choice to string holder
        string_holder += random.choice(choices)
    #return string holder
    return string_holder

def create_salt_file(target_directory, target_database_name):
    salt = generate_salt_string(64)
    print("encryption salt is: " + str(salt))

    salt_path = os.path.join(target_directory, target_database_name) + ".salt"

    print("saving salt to: " + os.path.basename(salt_path))

    with open(salt_path, "w") as salt_file:
        salt_file.write(str(salt))
    salt_file.close()

    return salt_path


def read_salt_file(salt_path):
    print("reading salt file")
    with open(salt_path, "rb") as opened_salt_file:
        return opened_salt_file.read()
    opened_salt_file.close()

# log password #

def log_password():
    password_confirmed = False

    while not password_confirmed:
        # password_holder = input("input password: ")
        # password_confrim = input("confirm password: ")
        password_holder = getpass.getpass("input password: ")
        password_confrim = getpass.getpass("confirm password: ")

        if password_holder == password_confrim:
            print("password confirmed")
            password_confirmed = True
            return password_holder
        else:
            print("password confirmation failed, try again")

# encryption #

def encrypt_file(database_name, input_file, password_input, salt_input):
    import os
    import base64
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    #goal is to encrypt a file and return a file of the same name and type, but encrypted

    file_name, file_extension = os.path.splitext(input_file)
    display_name = os.path.basename(input_file)

    print(os.path.basename(input_file))

    if os.path.basename(input_file) == database_name:
        encrypted_filename = file_name + ".enc_database"
    elif file_extension != ".zip_dir":
        encrypted_filename = file_name +  ".enc_file"
    else:
        encrypted_filename = file_name +  ".enc_dir"

    #print("starting " + display_name + " file encryption")

    #print("building encryption scheme")
    password_bytes = bytes(password_input, 'utf-8')
    #salt = os.urandom(16)
    salt = salt_input
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    f = Fernet(key)

    #print("converting " + display_name + " to bytes")
    with open(input_file, "rb") as opened_input_file:
        original_bytearray = opened_input_file.read()

    #print("original bytes: " + str(original_bytearray))

    #print("encrypting" + display_name + "bytes")
    encrypted_bytearray = f.encrypt(original_bytearray)

    #print("saving"  + display_name + "bytes to encrypted file")
    with open(encrypted_filename, "wb") as output_file:
        output_file.write(encrypted_bytearray)

    #print("closing"  + display_name + " working files")
    opened_input_file.close()
    output_file.close()

    #print("deleting"  + display_name + " working vault")
    os.remove(input_file)

    #print("encrypted file"  + display_name + " saved")

def encrypt_all_files(database_name, path, password_input, salt_input):
    import os
    import shutil

    database = os.path.basename(path)

    print("encrypting all files in: " + database)

    #recursively go through all files in directory and encrypt them
    for root, dirs, files in os.walk(path):
        #encrypt files
        #encrypt_file(file, password_input, salt)
        for file_name in files:
            individual_file = os.path.join(root, file_name)

            #print("encrypting file: " + individual_file)
            encrypt_file(database_name, individual_file, password_input, salt_input)

# compression #

def compress_file(input_directory):

    file_name, file_extension = os.path.splitext(input_directory)
    #compressed_file_path = os.path.dirname(input_directory)
    os.chdir(input_directory)
    shutil.make_archive(file_name, 'zip', input_directory)
    os.rename(file_name + ".zip", file_name + ".zip_dir")
    shutil.rmtree(input_directory)

def compress_directories(database_name, path, password_input, salt_input):

    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            #print("in directoy: " + os.path.join(root, name))
            individual_folder = os.path.join(root, dir)
            #print("compressing: " + dir)
            compress_file(individual_folder)
            encrypt_file(database_name, individual_folder + ".zip_dir", password_input, salt_input)
    print('root directory is: ' + path)
    compress_file(path)
    encrypt_file(database_name, path + ".zip_dir", password_input, salt_input)

# decryption #

def ask_password():
    return getpass.getpass("input password: ")

def unpack_archive(input_filename):
    import os
    import shutil

    print("unpacking: " + os.path.basename(input_filename))

    file_name, file_extension = os.path.splitext(input_filename)
    os.mkdir(file_name)
    compressed_file_path = os.path.dirname(input_filename)
    #os.chdir(compressed_file_path)
    shutil.unpack_archive(input_filename, file_name)
    os.remove(input_filename)

def decrypt_file(encrypted_file, password, salt_input):
    import os
    import base64
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    print("starting file decryption")

    print("building decryption scheme")
    password_bytes = bytes(password, 'utf-8')

    salt = salt_input
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    f = Fernet(key)

    print("loding file")
    with open(encrypted_file, "rb") as input_vault:
        input_bytearray = input_vault.read()

    print("decrypting file")
    decrypted_bytearray = f.decrypt(input_bytearray)

    print("saving compressed file")

    output_name = encrypted_file[:-8] + ".zip"
    output_filename = os.path.basename(output_name)

    with open(output_name, "wb") as output_file:
        output_file.write(decrypted_bytearray)

    print("closing working files")
    input_vault.close()
    output_file.close()

    #remove working file
    os.remove(encrypted_file)

    print(output_filename +" decrypted successfully")
