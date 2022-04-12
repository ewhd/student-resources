#!/user/bin/env python3

# Script:                       challenge313-request-library.py
# Author:                       Ethan Denny
# Date of latest revision:      3/18/2021
# Purpose:          This script performs an HTTP request on a given url 
#                   and returns status and header information.

# Description:
# This script prompts the user for a URL, then saves that as a string to a variable.
# Then it prompts the user for an HTTP method.
# Then the script repeats back what it is about to do (perform X HTTP method on Y URL)
# and asks the user for confirmation.
# Then it uses the requests library to perform the operation.
# Then it translates the response code into human language and pritns it, along with
# response header iformation.


import requests, sys, validators


# Define Variables

# This variable will hold the url received from the user
target_url_var = str
# target_url_var = "http://google.com"

# This variable will hold the integer value of the choice made by the user from a list of options
http_method_int_var = int

# This variable holds a tuple of HTTP methods + and exit option
http_methods = ("get", "post", "put", "delete", "head", "patch", "options", "exit")

# This variable will hold the name of the HTTP method as a string
http_method_name_var = str

# This variable will hold the output of calling the `requests` module
response = None

# This variable holds a dictionary mapping HTTP response codes to messages
# Entries have the form {code: (shortmessage, longmessage)}
# Copied from here:https://gist.github.com/bl4de/3086cf26081110383631
response_codes = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this server.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }



# Define Functions

# This is a function to prompt a user for yes or no (y/n) and return True or False.
# I pulled it from here: https://gist.github.com/garrettdreyfus/8153571#gistcomment-3519679
def yesno(question):
    """Simple Yes/No Function."""
    prompt = f'{question} ? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False


def Main():
    proceed = False
    url_valid = False
    option_valid = False

    # This while loop gets inputs from the user and confirms that the inputs are valid
    while proceed == False:
        # This section prompts the user for a url, then checks that it is valid. If the url is
        # is valid it continues, and if not it loops until it is
        # See: https://www.codespeedy.com/check-if-a-string-is-a-valid-url-or-not-in-python/
        while url_valid == False:
            target_url_var = input("Enter a valid URL or 'exit' to quit:\n")
            if target_url_var == "exit":
                sys.exit("Goodbye!")
            if validators.url(target_url_var) == True:
                break
            print("That is not a valid URL. Please try again.\n(Hint: did you begin with http://?)")

        # # This section gives the user options of different HTTP methods (and an option to exit)
        # print("\nPlease select an HTTP Method from the follwoing options: \n\
        #     1. GET\n\
        #     2. POST\n\
        #     3. PUT\n\
        #     4. DELETE\n\
        #     5. HEAD\n\
        #     6. PATCH\n\
        #     7. OPTIONS\n\
        #     8. Exit Program\n\
        #     ")

        # This alternative way to print the options is derived from Carsten's script.
        # It has the benefit of drawing options from the initial variable, rather than 
        # keeping a separate listing of options in a string, which could get out of sync.
        i = 1
        for method in http_methods:
            print(str(i) + ". " + method.upper())
            i += 1

        # This section requests the user to choose one of the options given. It loops until a valid option is selected.
        while True:
            try:
                http_method_int_var = int(input("Enter the number (1-8) of the option you wish to use: "))
                if http_method_int_var in range(1, len(http_methods) + 1):
                # if 1 <= http_method_int_var <= 8:
                    break
            except:
                print("That's not a number! Please try again")

        # This line converts the integer value of the user's method choice into a string with the method name
        http_method_name_var = http_methods[http_method_int_var - 1]
        

        # This section first checks if the user selected the option to exit the program. If so then the program ends.
        # If not then it prints what the program will do next and asks the user to confirm
        if http_method_int_var == 8:
            sys.exit("Goodbye!")
        else:
            print("\nThis script is about to perform a " + http_method_name_var.upper() + " request on " + str(target_url_var))
            proceed = yesno("Would you like to proceed")

    # This section uses getattr to call the module `requests` with http_method_name_var as the method and target_url_var
    # as the argument
    response = getattr(requests, http_method_name_var)(target_url_var)
    
    # This section looks up a human readable explanation of the response code and prints it along with the code
    print("\nStatus Code: " + str(response.status_code) + "\n" "Code Meaning: {}".format(str(response_codes.get(response.status_code)[1])))

    # This section prints the response header information for target_url_var
    print("\n===Response Header Information==")
    for key, value in response.headers.items():
        print(key, " : ", value)
    


# Main
Main()

# End