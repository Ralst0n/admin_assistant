from makedirectory import FileSystem, Directory
from invoice_wiz import InvoiceManager
from chatbot import *
import sys
import os
import time
import yaml

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
    How can I help you?

    1. Start invoice numbers email Request Invoice Numbers
    2. Update Invoice Tracker
    3. Start An Invoice
    4. Create Status Change Form
    5. Update Certifications Tracker
    6. Create New Employee Folder
    7. Exit program

    """)

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
            if choice.isnumeric():
                program = self.choices.get(choice)
                program()
            elif choice.lower() == "help":
                print('''One day, but today is not that day''')
                time.sleep(1.5)
                input("\n\n\n\n\npress enter to return to the menu")
            elif choice.lower() in config["greetings"]:
                self.chatbot()
            else:
                print("{} is not a valid option".format(choice))

    def start_invoice(self):
        self.invoicemanager.run()

    def quit(self):
        os.system('cls')
        print("See you next time!")
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
    Menu().run()
