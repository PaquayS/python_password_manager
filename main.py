import pickle
import os
import base64

# import numpy as np #just in case I want to use it.

manager_list = []
clear_list = ["Site", "UID", "Login"]
main_password = ""
firstTime = True
correctPassword = False
bsufdbos = False


class Manager:
    def __init__(self, site, UID, password):
        self.site = site
        self.UID = UID
        password_encrypted = password.encode('utf-8')
        self.password = base64.b64encode(password_encrypted, altchars=None)
        _decrypted_password = base64.b64decode(self.password, altchars=None, validate=False)
        _decoded_password = _decrypted_password.decode('utf-8')
        print(self.site + '\t' + self.UID + '\t' + _decoded_password)


def new_manager():
    global manager_list
    _manager = Manager(
        input("site:\t"),
        input("UID:\t"),
        input("password:\t"),
    )
    manager_list.append(_manager)
    write_text()
    do_what()


def do_what():  # the "main" menu
    global manager_list

    print("what do you want to do?\n")
    print("New log in.\t\tnew\n"
          "Show selected log in.\tselected\n"
          "Show all.\t\tall\n"
          "Change main password.\tchange password\n"
          "Change a login.\t\tchange login\n"
          "Remove a login.\t\tremove login\n"
          "End the program.\tquit\n")
    command = input()

    if command.lower() == "new":  # give a new login
        new_manager()
    elif command.lower() == "all":  # show all logins
        show_all()
    elif command.lower() == "selected":  # show the selected log in
        show_selected()
    # elif command.lower() == "clear all": #clear all logins
    #   clear_file()
    elif command.lower() == "change password":  # change your password
        new_password()
    elif command.lower() == "change login":  # change a login
        change_manager()
    elif command.lower() == "remove login":
        remove_login()
    elif command.lower() == "quit":  # end the program
        end()
    else:  # ask the question again on wrong input
        do_what()


def end():  # end the program and save everything.
    write_text()
    print("goodbye")


def write_text():
    global manager_list
    global main_password
    _encrypted_1 = main_password.encode('utf-8')
    _encrypted_2 = base64.b64encode(_encrypted_1, altchars=None)
    with open("venv/random.txt", "wb") as fp:
        pickle.dump(_encrypted_2, fp)
        pickle.dump(manager_list, fp)


def read_text():
    global manager_list
    global main_password
    with open("venv/random.txt", "rb") as fp:
        _file_size = os.path.getsize("venv/random.txt")
        if _file_size > 0:
            _decrypted_2 = pickle.load(fp)
            manager_list = pickle.load(fp)
            _decrypted_1 = base64.b64decode(_decrypted_2, altchars=None, validate=False)
            main_password = _decrypted_1.decode('utf-8')


def _main_password():
    global main_password
    global firstTime
    global correctPassword
    if firstTime:
        first_time()
    elif not firstTime:
        _given_password = input("Enter your password.\n")
        if _given_password == main_password:
            correctPassword = True
            print("\nWelcome.\n")
            do_what()
        else:
            correctPassword = False
            print("Incorrect password.\n")
            _main_password()


def first_time():
    global main_password
    global firstTime
    if main_password:
        firstTime = False
    else:
        firstTime = True
    if firstTime:
        main_password = input("Enter a password.\n")
        firstTime = False
        write_text()
    _main_password()


def show_all():
    global manager_list
    print("\nshow all\n")
    for i, value in enumerate(manager_list):
        _decrypted_password = base64.b64decode(value.password, altchars=None, validate=False)
        _decoded_password = _decrypted_password.decode('utf-8')
        print(i, '\t', value.site, '\t', value.UID, '\t', _decoded_password, '\n')
    do_what()


def show_selected():
    global manager_list
    print("\nGive the index of the login you want to see.\n")
    for i, value in enumerate(manager_list):
        print('\n', i, value.site, '\n')
    _index = int(input())
    for i, value in enumerate(manager_list):
        if _index == i:
            _decrypted_password = base64.b64decode(value.password, altchars=None, validate=False)
            _decoded_password = _decrypted_password.decode('utf-8')
            print(value.site + '\t' + value.UID + '\t' + _decoded_password, '\n')
    do_what()


# currently not working as intended.
def clear_file():  # clear all your logins.
    global clear_list
    print("\nAre you sure? Y/N\n")
    confirm = input()
    if confirm.lower() == "y":
        with open("venv/random.txt", "wb") as fp:
            pickle.dump(clear_list, fp)
    elif confirm.lower() == "n":
        do_what()
    else:
        print("\nPlease use Y or N.\n")
        clear_file()


def new_password():  # change your login password
    global main_password
    main_password = input("\nPlease enter your new password:\t")
    print("\n")
    write_text()
    do_what()


def change_manager():  # change a single input off an already existing login.
    global manager_list
    print("\nGive the sitename of which password you want to see.\n\n")
    for i in range(len(manager_list)):  # print all the site names.
        print(manager_list[i].site)
    _sitename = input()
    for i in range(len(manager_list)):  # go to your selected site
        if _sitename == manager_list[i].site:
            print("\nWhat do you want to change?\n")
            _change_1 = input("Site, UID or password?\n")  # select if you want to change site, UID or password.
            if _change_1.lower() == "site":
                print("\nEnter the new address.\n\n")
                manager_list[i].site = input()  # get new input
                manager_list[i].UID = manager_list[i].UID  # put old input back
                manager_list[i].password = manager_list[i].password  # put old input back
            elif _change_1.lower() == "uid":
                print("\nEnter the new UID.\n\n")
                manager_list[i].site = manager_list[i].site
                manager_list[i].UID = input()
                manager_list[i].password = manager_list[i].password
            elif _change_1.lower() == "password":
                print("\nEnter the new password.\n")
                manager_list[i].site = manager_list[i].site
                manager_list[i].UID = manager_list[i].UID
                manager_list[i].password = input()
    write_text()
    do_what()  # go back to "main" menu


def remove_login():
    global manager_list
    print("\nGive the index of the login you want remove.\n\n")
    for i, value in enumerate(manager_list):
        print(i, value.site)
    _index = int(input())
    for i, value in enumerate(manager_list):
        if _index == i:
            print("delete this login?\tY/N\t", value)
            if input().lower() == "y":
                print("removed.\n\n")
                del manager_list[i]
    write_text()
    do_what()


#with open("venv/random.txt", "rb") as fp:
#    file_size = os.path.getsize("venv/random.txt")
#    if file_size > 0:
#        read_text()

read_text()
_main_password()


# To DO list:
# find a way to hide the .txt file
# clean up code
# upload to git
