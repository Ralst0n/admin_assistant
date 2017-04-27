import os
import shutil

class Directory:
    '''creates a directory in a location based on information provided by the user'''

    def __init__(self, path, first_name, last_name):
        self.path = path
        self.fname = first_name
        self.lname = last_name
        self.fullpath = os.path.join(path, "{}, {}".format(last_name, first_name))


class FileSystem:

    def __init__(self):
        pass

    def run(self):
        path = self.get_path()
        fname, lname = self.get_name()
        self.directory = Directory(path, fname, lname)
        self.add_directory()
        self.run_again()

    def update_status(self):
        path = self.get_path()
        fname, lname = self.get_name()
        self.directory = Directory(path, fname, lname)
        self.add_status_change()

    def add_status_change(self):
            template = r"R:\Version Control\xl_invoice_form\Status Change Form (New Hire).xlsm"
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
        print('''What type of status change is this?
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
        '''city defaults to kop if anything but pgh is entered'''
        while True:
            city = input("Is the employee in KOP or Pitt? \n>")
            #return kop dir if a kop term is used
            if city.lower() in ["kop", "king of prussia"]:
                return r"R:\012 - EMPLOYMENT\PERSONNEL FILE\ACTIVE EMPLOYEES\KOP\\"
            #return pgh dir if a pgh term is used
            elif city in ["pgh", "pitt", "pit", "pittsburgh"]:
                return r"R:\012 - EMPLOYMENT\PERSONNEL FILE\ACTIVE EMPLOYEES\PGH\\"

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

    def add_directory(self):
        '''verifies if the employee has a directory, if so it adds necessary folders,
           if not, adds directory and requests to add status change form.'''
        #name the directory last name, first name
        new_directory = os.path.join(self.directory.path, "{}, {}".format(self.directory.lname, self.directory.fname))
        #if there is no directory for that person, create one and enter it
        if not os.path.isdir(new_directory):
           print("Creating directory... " + new_directory)
           os.makedirs(new_directory)
           os.chdir(new_directory)
           print(os.getcwd())

        #add each of the following folders to the directory if they don't exist already
        folders = ["Correspondence", "Emergency Contact", "New Hire Documents", "Status Change", "Wage Acknowledgement", "Certifications", "Equipment"]
        changes = False
        for i in folders:
            if os.path.isdir(os.path.join(new_directory, i)):
                next
            else:
                os.makedirs(os.path.join(new_directory, i))
                print("Added " + i + " folder")
                changes = True
        if changes:
            self.status_change_prompt()
        if not changes:
            print("{} {} already has a Personnel folder. No changes made.".format(self.directory.fname.capitalize(), self.directory.lname.capitalize()))
