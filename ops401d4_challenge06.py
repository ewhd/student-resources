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


def EncryptDecryptBytes(input_bytes, option, key):
    # This function takes an option flag, bytes, and a key as arguments, evaluates the option flag to 
    # either encrypt or decrypt using the key, then returns the result
    if option == "encrypt":
        output_bytes = Fernet(key).encrypt(input_bytes)
    elif option == "decrypt":
        output_bytes = Fernet(key).decrypt(input_bytes)
    return output_bytes


def EncryptDecryptString(input_string, option, key):
    # This function just wraps EncryptDecryptBytes() to take and return strings
    input_bytes = input_string.encode()
    output_bytes = EncryptDecryptBytes(input_bytes, option, key)
    return output_bytes.decode('utf-8')


def ApplyFunctionRecursivelyToFilesInDir(function, dir_path, **kwargs):
    # This function calls another function recursively to every file in a directory.
    
    # This function takes a directory path and another function as arguments, as well as
    # unlimited keyword arguments. It assumes that the passed function's first argument 
    # is a path to a directory and that any other arguments it needs will be passed as kwargs.

    # The function tries to walk through the directory and recursively apply the passed 
    # function to every file it finds.
    
    # Finally it returns True/False based on whether it succeeded or if something went wrong.
    # Errors are most likely to be caused by poor configuration of the passed arguments.

    # Walk through the given directory, calling the argued function on each file
    try:
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for name in files:
                function(os.path.join(root, name), **kwargs)
        return True
    except:
        return False


def GetCheckPathFromUser(path_type="system"):
    # This function gets an input from the user and checks if it is a valid path. If it is not,
    # it prompts the user again, unless they type "#back".
    # This function takes an optional argument to check if the user's input is exclusively a
    # valid file path or a valid directory path.
    # If the path is valid it returns the path.
    while True:
        path = input("Please enter a valid " + path_type + " path or '#back' to return to the previous menu: ")
        
        if path_type == "system" and (os.path.isfile(path) or os.path.isdir(path)):
            return path
        elif path_type == "file" and os.path.isfile(path):
            return path
        elif path_type == "directory" and os.path.isdir(path):
            return path
        elif path == "#back":
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


def menu(program_mode_dict):
    # This function displays a menu, validates user choice, and either returns the integer or exits the program
    # This function takes a dictionary of number coded program modes as an argument, adds an additional mode to quit
    # then prints a menu of codes and modes with ordered by code.
    # Then it prompts the user for a number to select, checks that it is a valid option, and if it is returns that number.

    # If it doesn't already exist, add a final "Exit" option to the dictionary of program modes
    exit_code = len(program_mode_dict)
    if program_mode_dict[len(program_mode_dict)] != "Exit":
        exit_code += 1
        program_mode_dict[exit_code] = "Exit"

    # Display menu options:
    for code in sorted (program_mode_dict.keys()):
        print(str(code) + ". " + program_mode_dict[code])

    # This section requests the user to choose one of the options given. It loops until a valid option is selected.
    while True:
        try:
            mode_int_var = int(input("Enter the number of the option you wish to use: "))
            if mode_int_var in program_mode_dict:
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

        # Generate and load a new key
        if option == 1:
            key_name = input("What would you like to name this key?\n(Default: key.key)\n> ") or "key.key"
            print(type(key_name))
            key_file_name = WriteNewKeyToFile(key_name, True)
            current_key = LoadKey(key_file_name)
            print("\nA new key has been written to " + key_file_name + "\nThe current key is: \n" + current_key.decode('utf-8') + "\n")
            PauseForUser()

        # Load an existing key
        if option == 2:
            key_file_name = input("What is the name of the key file you wish to load? Don't forget the '.key' on the end!\n(Default: key.key)\n> ") or "key.key"
            current_key = LoadKey(key_file_name)
            print("\nThe key in " + key_file_name + " has been loaded.\nThe current key is: \n" + current_key.decode('utf-8') + "\n")
            PauseForUser()

        # Show the current key
        if option == 3:
            if CheckForKey(current_key):
                print("The current key is:\n" + current_key.decode('utf-8') + "\n")
                PauseForUser()

        # Encrypt a message
        if option == 4:
            if CheckForKey(current_key):
                message_to_encrypt = input("What is the message you would like to encrypt?\n> ")
                print("Your encrypted message is:\n" + EncryptDecryptString(message_to_encrypt, "encrypt", current_key) + "\n")
                PauseForUser()

        # Decrypt a message
        if option == 5:
            if CheckForKey(current_key):
                message_to_encrypt = input("What is the message you would like to decrypt?\n> ")
                try:
                    decrypted_message = EncryptDecryptString(message_to_encrypt, "decrypt", current_key)
                    print("Your decrypted message is:\n" + decrypted_message + "\n")
                    PauseForUser()
                except:
                    print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                    PauseForUser()

        # Encrypt a file
        if option == 6:
            if CheckForKey(current_key):
                target_file = GetCheckPathFromUser("file")
                if target_file != None:
                    EncryptDecryptFile(target_file, "encrypt", current_key)
                    print("\nThe file at " + target_file + " has been encrypted using the current key: \n" + current_key.decode('utf-8') + "\n\n")
                    PauseForUser()

        # Decrypt a file
        if option == 7:
            if CheckForKey(current_key):
                target_file = GetCheckPathFromUser("file")
                if target_file != None:
                    try:
                        EncryptDecryptFile(target_file, "decrypt", current_key)
                        print("\nThe file at " + target_file + " has been decrypted using the current key: \n" + current_key.decode('utf-8') + "\n\n")
                        PauseForUser()
                    except:
                        print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                        PauseForUser()

        # Recursively encrypt a directory
        if option == 8:
            if CheckForKey(current_key):
                target_dir = GetCheckPathFromUser("directory")
                if target_dir != None:
                    did_it_work = ApplyFunctionRecursivelyToFilesInDir(EncryptDecryptFile, target_dir, option="encrypt", key=current_key)
                    if did_it_work == True:
                        print("\nThe contents of the directory " + target_dir + " have all been encrypted using the current key: \n" + current_key.decode('utf-8') + "\n\n")
                        PauseForUser()
                    elif did_it_work == False:
                        print("ERROR: something is wrong with the arguments and/or keyword arguments.\n")
                        PauseForUser()

        # Recursively decrypt a directory
        if option == 9:
            if CheckForKey(current_key):
                target_dir = GetCheckPathFromUser("directory")
                if target_dir != None:
                    try:
                        did_it_work = ApplyFunctionRecursivelyToFilesInDir(EncryptDecryptFile, target_dir, option="decrypt", key=current_key)
                        if did_it_work == True:
                            print("\nThe contents of the directory " + target_dir + " have all been decrypted using the current key: \n" + current_key.decode('utf-8') + "\n\n")
                            PauseForUser()
                        elif did_it_work == False:
                            print("ERROR: something is wrong with the arguments and/or keyword arguments.\n")
                            PauseForUser()
                    except:
                        print("\nThe key does not seem to fit the lock. Load the correct key and try again.\n")
                        PauseForUser()

if __name__ == "__main__":
    main()