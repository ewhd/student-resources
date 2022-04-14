#!/user/bin/env python3

# Script:                       ops401d4_challenge06.py
# Author:                       Ethan Denny
# Date of latest revision:      4/13/2022
# Purpose:                      Demonstrate use of versatile functions in a program that lets the user 
#                               use a menu system to create and load encryption keys and to encrypt/decrypt 
#                               messages and files.


# Imports:

from cryptography.fernet import Fernet
import os, sys

# Define Variables:

current_key = False

program_modes = {
    1: "Generate and load a new key", 
    2: "Load an existing key",
    3: "Show the current key",
    4: "Encrypt a message", 
    5: "Decrypt a message", 
    6: "Encrypt a file", 
    7: "Decrypt a file",
    9: "Recursively decrypt a directory",
    8: "Recursively encrypt a directory"
}

# Define Functions:

def WriteNewKeyToFile(file_name, return_file_name=False):
    # Generate a new key and save it into a file with a name provided as an argument.
    # If the argument does not include a ".key" suffix, this function adds it.
    # Optionally, this function can return the file name
    
    # If not present, apply the appropriate ".key" suffix
    if file_name[-4:] != ".key":
        file_name = file_name + ".key"

    # Generate new key and write it to file
    key = Fernet.generate_key()
    with open(file_name, "wb") as key_file:
        key_file.write(key)

    # Return filename
    if return_file_name == True:
        return file_name


def LoadKey(file_name="key.key"):
    # Load the key from the current directory named 'file_name'
    # If called without argument, assume file name is 'key.key'
    return open(file_name, "rb").read()


def EncryptDecryptBytes(option, input_bytes, key):
    # This function takes an option flag, bytes, and a key as arguments, evaluates the option flag to 
    # either encrypt or decrypt using the key, then returns the result
    if option == "encrypt":
        output_bytes = Fernet(key).encrypt(input_bytes)
    elif option == "decrypt":
        output_bytes = Fernet(key).decrypt(input_bytes)
    return output_bytes


def EncryptDecryptString(option, input_string, key):
    # This function just wraps EncryptDecryptBytes() to take and return strings
    input_bytes = input_string.encode()
    output_bytes = EncryptDecryptBytes(option, input_bytes, key)
    return output_bytes.decode('utf-8')


def EncryptDecryptFile(option, file_name, key):
    # This function wraps EncryptDecryptBytes() to handle files

    # Read the plaintext contents of the file into a variable
    with open(file_name, "rb") as file:
        file_input = file.read()
    file.close()

    # Encrypt or decrypt the contents of the file
    file_output = EncryptDecryptBytes(option, file_input, key)
    
    # Write the encrypted data back into the file, replacing the original contents
    with open(file_name, "wb") as file:
        file.write(file_output)
    file.close()


def EncryptDecryptDir(option, dir_path, key):
    # This function uses EncryptDecryptFile() to recursively effect a directory and its contents

    # Walk through the given directory, calling EncryptDecryptFile() on each file
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            EncryptDecryptFile(option, os.path.join(root, name), key)


def GetCheckPath(path_type):
    # This function gets an input from the user and if it is a valid file path returns that path. 
    # Otherwise it asks the user again, or else the user can escape.
    while True:
        path = input("Please enter a valid " + path_type + " path or 'back' to return to the previous menu: ")
        if path_type == "file" and os.path.isfile(path):
            return path
        if path_type == "directory" and os.path.isdir(path):
            return path
        if path == "back":
            return None
        else:
            print("That is not a valid " + path_type + " path or option. Try again.\n")


def CheckForKey(key_var):
    # This function checks if the argument is False, which indicates no key has been loaded yet.
    # If the argument is not False then it returns True.
    if key_var == False:
        print("No key has been loaded. Load a key and try again.\n")
        PauseForUser()
        pass
    else:
        return True


def PauseForUser():
    # Pauses until the user presses a key.
    # I have this in here a lot and was tired of copy/pasting it.
    input("Press any key to return to menu...\n\n")


def menu(program_mode_list):
    # This function displays a menu, validates user choice, and either returns the integer or exits the program
    # This function takes a dictionary of number coded program modes as an argument, adds an additional mode to quit
    # then prints a menu of codes and modes with ordered by code.
    # Then it prompts the user for a number to select, checks that it is a valid option, and if it is returns that number.

    # If it doesn't already exist, add a final "Exit" option to the dictionary of program modes
    exit_code = len(program_mode_list)
    if program_mode_list[len(program_mode_list)] != "Exit":
        exit_code += 1
        program_mode_list[exit_code] = "Exit"

    # Display menu options:
    for code in sorted (program_mode_list.keys()):
        print(str(code) + ". " + program_mode_list[code])

    # This section requests the user to choose one of the options given. It loops until a valid option is selected.
    while True:
        try:
            mode_int_var = int(input("Enter the number of the option you wish to use: "))
            if mode_int_var in program_mode_list:
                break
            else:
                print("That's not an option! Please try again")
        except:
            print("That's not an option! Please try again")

    # This section first checks if the user selected the option to exit the program. If so then the program ends.
    # If not then it 
    if mode_int_var == exit_code:
        sys.exit("Goodbye!")

    return mode_int_var



def main():
    # This script uses a menu to get a choice from the user, then evaluates that choice and calls the appropriate functions
    global current_key
    end = False
    while end == False:
        option = menu(program_modes)

        print("\nYou have chosen to: " + program_modes[option] + "\n")

        if option == 1:
            key_name = input("What would you like to name this key?\n(Default: key.key)\n> ") or "key.key"
            print(type(key_name))
            key_file_name = WriteNewKeyToFile(key_name, True)
            current_key = LoadKey(key_file_name)
            print("\nA new key has been written to " + key_file_name + "\nThe current key is: \n" + current_key.decode('utf-8') + "\n")
            PauseForUser()

        if option == 2:
            key_file_name = input("What is the name of the key file you wish to load? Don't forget the '.key' on the end!\n(Default: key.key)\n> ") or "key.key"
            current_key = LoadKey(key_file_name)
            print("\nThe key in " + key_file_name + " has been loaded.\nThe current key is: \n" + current_key.decode('utf-8') + "\n")
            PauseForUser()

        if option == 3:
            if CheckForKey(current_key):
                print("The current key is:\n" + current_key.decode('utf-8') + "\n")
                PauseForUser()

        if option == 4:
            if CheckForKey(current_key):
                message_to_encrypt = input("What is the message you would like to encrypt?\n> ")
                print("Your encrypted message is:\n" + EncryptDecryptString("encrypt", message_to_encrypt, current_key) + "\n")
                PauseForUser()

        if option == 5:
            if CheckForKey(current_key):
                message_to_encrypt = input("What is the message you would like to decrypt?\n> ")
                try:
                    decrypted_message = EncryptDecryptString("decrypt", message_to_encrypt, current_key)
                    print("Your decrypted message is:\n" + decrypted_message + "\n")
                    PauseForUser()
                except:
                    print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                    PauseForUser()

        if option == 6:
            if CheckForKey(current_key):
                target_file = GetCheckPath("file")
                if target_file != None:
                    EncryptDecryptFile("encrypt", target_file, current_key)
                    print("\nThe file at " + target_file + " has been encrypted using the following key: \n" + current_key.decode('utf-8') + "\n\n")
                    PauseForUser()

        if option == 7:
            if CheckForKey(current_key):
                target_file = GetCheckPath("file")
                if target_file != None:
                    try:
                        EncryptDecryptFile("decrypt", target_file, current_key)
                        print("\nThe file at " + target_file + " has been decrypted using the following key: \n" + current_key.decode('utf-8') + "\n\n")
                        PauseForUser()
                    except:
                        print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                        PauseForUser()

        if option == 8:
            if CheckForKey(current_key):
                target_dir = GetCheckPath("directory")
                if target_dir != None:
                    EncryptDecryptDir("encrypt", target_dir, current_key)
                    print("\nThe contents of the directory " + target_dir + " have all been encrypted using the following key: \n" + current_key.decode('utf-8') + "\n\n")
                    PauseForUser()

        if option == 9:
            if CheckForKey(current_key):
                target_dir = GetCheckPath("directory")
                if target_dir != None:
                    try:
                        EncryptDecryptDir("decrypt", target_dir, current_key)
                        print("\nThe contents of the directory " + target_dir + " have all been decrypted using the following key: \n" + current_key.decode('utf-8') + "\n\n")
                        PauseForUser()
                    except:
                        print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                        PauseForUser()


main()