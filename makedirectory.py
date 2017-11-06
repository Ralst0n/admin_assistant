import os
import shutil
import time

class Directory:
    '''creates a directory in a location based on information provided by the user'''

    def __init__(self, path, first_name, last_name):
        self.path = path
        self.fname = first_name
        self.lname = last_name
        self.fullpath = os.path.join(path, "{}, {}".format(last_name, first_name))
        #keep track of if the person wanted to create a status change form but didn't create directory first
        self.statuschange = False

class FileSystem:

    def __init__(self):
        pass

    def run(self):
        path = self.get_path()
        fname, lname = self.get_name()
        self.directory = Directory(path, fname, lname)
        self.add_directory()

    def gather_employee_info(self):
        '''find out for whom we are creating files.'''
        path = self.get_path()
        fname, lname = self.get_name()
        self.directory = Directory(path, fname, lname)

    def update_status(self):
        self.gather_employee_info()
        if self.verify_directory():
            self.add_status_change()
        else:
            self.statuschange = True
            print(f"You must create a directory for {self.directory.fname} {self.directory.lname} before creating a status change form")
            time.sleep(2)
            self.add_directory()

    def add_status_change(self):
        '''Grabs a status change template form and adds it to the folder of the current employee'''
        template = r"P:\Version Control\xl_invoice_form\Status Change Form (New Hire).xlsm"
        status_change_folder = os.path.join(self.directory.fullpath, "Status Change" )
        shutil.copy2(template, status_change_folder)
        change_type = self.status_change_type()
        os.chdir(status_change_folder)
        status_form_name = "Status Change Form ({}).xlsm".format(change_type)
        os.rename("Status Change Form (New Hire).xlsm", status_form_name  )
        print("Opening {} in Excel".format(status_form_name))
        os.startfile(status_form_name)

    def status_change_prompt(self):
        '''ask users if they'd like to add a status change form whenever
           changes are made to an employee folder'''
        status_change =input("Would you like to add a status change form for {}? \n>".format(self.directory.fname.capitalize()))
        if status_change.lower() in ["y","ye","yes"]:
            self.add_status_change()

    def status_change_type(self):
        '''return the type of status change based on user inputing a Corresponding number'''
        status_change = {"1": "New Hire",
                         "2": "Wage Increase",
                         "3": "Layoff",
                         "4": "Re-hire",
                         "5": "Other"}
        print('''What type of status change is this?n
        1. New Hire
        2. Wage Increase :)
        3. Layoff :(
        4. Re-hire
        5. Other''')
        change_type = int(input(">"))
        if change_type < 5:
            return status_change[str(change_type)]
        else:
            return input("Type the status change below: \n")

    def run_again(self):
        '''give option to add another new employee'''
        run_again = input("Would you like to create a folder for another employee? \n>").lower()
        if run_again in ['y',"ye", "yes"]:
            self.run()
        else:
            print("Returning to main menu")

    def get_path(self):
        '''city must be one of Prudent's business cities in Pennsylvania '''
        while True:
            city = input("Is the employee in KOP or Pitt? \n>")
            #return kop dir if a kop term is used
            if city.lower() in ["kop", "king of prussia"]:
                return r"P:\012 - EMPLOYMENT\PERSONNEL FILE\ACTIVE EMPLOYEES\KOP\\"
            #return pgh dir if a pgh term is used
            elif city in ["pgh", "pitt", "pit", "pittsburgh"]:
                return r"P:\012 - EMPLOYMENT\PERSONNEL FILE\ACTIVE EMPLOYEES\PGH\\"

    def get_name(self):
        '''prompt for employee name. return 2 element list first name, last name'''
        while True:
            name = []
            names = input("Enter employee name (first & last) \n>")
            if len(names.split(" ")) == 2:
                for x in names.split(" "):
                    #put last name as first item in list to get to [last, first]
                    name.append(x.upper())
                return name

    def verify_directory(self):
        '''verifies the employee has a directory'''
        return os.path.isdir(self.directory.fullpath)


    def add_directory(self):
        '''create new directory for employee if they don't have one'''
        if not self.verify_directory():
           print("Creating directory... " + self.directory.fullpath)
           os.makedirs(self.directory.fullpath)
           os.chdir(self.directory.fullpath)

        #add each of the following folders to the directory if they don't exist already
        folders = ["Correspondence", "Emergency Contact", "New Hire Documents", "Status Change", "Wage Acknowledgement", "Certifications", "Equipment"]
        changes = False
        for i in folders:
            if os.path.isdir(os.path.join(self.directory.fullpath, i)):
                next
            else:
                os.makedirs(os.path.join(self.directory.fullpath, i))
                print("Added " + i + " folder")
                changes = True
        if changes and self.statuschange:
            '''if the request comes from an original status form request doesn't ask to update status form goes right into it'''
            self.add_status_change()
        elif changes:
            self.status_change_prompt()
        if not changes:
            print("{} {} already has a Personnel folder. No changes made.".format(self.directory.fname.capitalize(), self.directory.lname.capitalize()))
