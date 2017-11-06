from makedirectory import FileSystem, Directory
from philip_invoice_wiz import InvoiceManager
from chatbot import *
import sys
import os
import datetime
import yaml
import datetime

with open("config.yml", "r") as ymlfile:
    config = yaml.load(ymlfile)

class Menu:

    def __init__(self):
        pass
        self.choices = {
        "1": self.get_invoice_numbers,
        "2": self.invoice_tracker,
        "3": self.start_invoice,
        "4": self.update_status,
        "5": self.cert_tracker,
        "6": self.makedir,
        "7": self.quit
        }

    def display_menu(self):
            print("""
    What can I do for you?

    1. Open Request Invoice Numbers Form
    2. Update Invoice Tracker
    3. Start An Invoice
    4. Create Status Change Form
    5. Update Certifications Tracker
    6. Create New Employee Folder
    7. Exit program

    """)
    def greet(self):
        os.system('cls')
        ctime = datetime.datetime.now().hour
        if ctime < 12:
            print("Good Morning, {}".format(config["user"]))
        elif ctime >12 and ctime < 15:
            print("Good Afternoon, {}".format(config["user"]))
        elif ctime == 15:
            print("Hey, {}! It's almost quittin time!".format(config["user"]))
        elif ctime > 15:
            print("\n\n\nMake it fast, {}, I'm trying to get out of here on time".format(config["user"]))
            time.sleep(1)
        time.sleep(1)
        self.run()

        print('''''' )
    def run(self):
        '''Display menu and respond to choice.'''
        while True:
            time.sleep(2)
            self.filesystem = FileSystem()
            self.invoicemanager = InvoiceManager()
            os.system('cls')
            self.display_menu()
            choice = input("Enter the number for an option: ")
            #os.system('cls')
            if choice.isnumeric() and choice in self.choices:
                program = self.choices.get(choice)
                program()
            elif choice.lower() == "help":
                print('''One day, but today is not that day''')
                time.sleep(1.5)
                input("\n\n\n\n\npress enter to return to the menu")
            elif choice.lower() in config["greetings"]:
                self.chatbot()
            elif choice.lower() == "bye":
                self.quit()
            else:
                print("{} is not a valid option".format(choice))

    def start_invoice(self):
        self.invoicemanager.run()

    def quit(self):
        os.system('cls')
        ctime = datetime.datetime.now().hour
        if ctime > 15:
            if datetime.datetime.now().weekday() > 3:
                print("See you next week!")
            else:
                print("See you tomorrow!")
        else:
            print("Hasta Luego!")
        time.sleep(1)
        sys.exit(0)


    def chatbot(self):
        bootup()

    def makedir(self):
        self.filesystem.run()

    def update_status(self):
        self.filesystem.update_status()

    @staticmethod
    def cert_tracker():
        print("Opening the Excel file...")
        os.startfile(config["cert_tracker"])


    @staticmethod
    def invoice_tracker():
        print("Opening the Excel file...")
        os.startfile(config["invoice_tracker"])


    @staticmethod
    def get_invoice_numbers():
        print("Opening the file in your web browser...")
        os.startfile(config["invoice_numbers"])



if __name__ == "__main__":
    Menu().greet()
