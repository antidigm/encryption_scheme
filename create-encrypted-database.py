# assembles functions from
from encryption_helper import *
#to create an encrypted database

##### create database #####

#
database_directory = choose_target_directory()

database_name = input_name()

database_path = make_database(database_directory, database_name)

##### populate the database with test data #####

# get test database path
test_database_path = os.path.join(os.getcwd(), 'test_database_documents')

# populate the database
populate_database(database_path, test_database_path)

##### encrypt database #####

# create and save salt #

salt_path = create_salt_file(database_directory, database_name)

salt = read_salt_file(salt_path)

print('salt is: ' + str(salt))

# log password #

password = log_password()

# encrypt files #

encrypt_all_files(database_name, database_path, password, salt)

# compress and encrypt directories #

compress_directories(database_name, database_path, password, salt)
