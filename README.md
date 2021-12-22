# encryption_scheme
a database encryption scheme that allows for minimal data exposure when accessing files

i am experimenting with making an encryption scheme to solve for my own peace of mind, i’m curious for the input from people with actual training and understanding of encryption protocol

from what i can gather about encryption in general, when a database is decrypted (is this even a real word?), it is held in ram on the host machine, or on the storage media itself.

what i am trying to solve for in this case is this:
if i have a large database of directories, sub-directories and files, with presumably sensitive material held within this database, how can in confidently access a single file within this database, while exposing the least amount of data possible in the process.  since even processors can be de-lidded and examined to retrieve data.  (please bare with me, i feel like i might be going a bit off the deep end, but let me keep my tinfoil hat on for a moment)

——————————————————————————————

if i simply encrypt the database ass a whole, when i decrypt said database, the entire thing is decrypted as a whole, subsequently exposing all data, even if I only want to access one file, correct?  this seems to unnecessarily expose my data as a whole.

[encrypted database]
v
decryptDatabase()
v
decrypted database
- files
- sub-directories
  - files
  - sub-directories
    - so on
    - so fourth
      - .....

——————————————————————————————

i could encrypt every file individually, leaving the directory structure the same, however, this exposes prying eyes to the entire structure of the database, including directory names, and individual file sizes

unencrypted database
- [encrypted files]
- visible sub-directories
  - [encrypted files]
  - visible sub-directories
    - [encrypted files]
    - visible sub-directories
      - so on
      - so fourth
        - .....

——————————————————————————————

the encryption scheme that i have been conceptualizing is a bit different.  it encrypts the data from the bottom of the tree upwards, individually encrypting all files in the bottom-most directory, then zipping and encrypting their parent directory.  then recursively going up the tree until the entire database is encrypted.  what I THINK this solves for, comes when accessing data within the database. only directory names and file names of the specific directory and filenames of the accessed file path will be visible.  and how much name and filetype information that is exposed, can be obfuscated by how files and directories are named during the decryption process.

[encrypted database]
v
decryptDatabase()
v
decrypted database
- [encrypted files]
- [encrypted sub-directories]
v
decryptSubDirectory()
v
decrypted database
- [encrypted files]
- decrypted sub-directory
  - [encrypted files]
  - [encrypted sub-directories]
v
decryptSubDirectory()
v
decrypted database
- [encrypted files]
- decrypted sub-directory
  - [encrypted files]
  - decrypted sub-directory
    - [encrypted files]
    - [encrypted sub-directories]
v
decryptFile()
v
decrypted database
- [encrypted files]
- decrypted sub-directory
  - [encrypted files]
  - decrypted sub-directory
    - decrypted file
    - [encrypted files]
    - [encrypted sub-directories]
