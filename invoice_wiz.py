import os
import shutil

class InvoiceManager:
    '''The invoice manager class represents the creation and appropriate filing
    of an invoice. Through this class you start any standard penndot invoice'''

    def __init__(self):
        pass

    def run(self):
        project_num = self.get_project_num()
        invoice_dir = self.get_invoice_directory(project_num)
        #make the invoice directory the new working directory and create the next invoice folder there.
        os.chdir(r"S:\FIN"+"\\"+project_num[0]+"\\"+project_num[1]+"\\"+invoice_dir)
        #next_invoice returns year (space) invoice xx i.e. 2017-02-19 Invoice 22

        next_invoice = self.create_next_folder()

        os.chdir(os.path.join(os.getcwd(), next_invoice))
        os.mkdir("Invoice Logs")

        #copy the most up to date invoice workbook into the new folder
        shutil.copy2(r"R:\Version Control\xl_invoice_form\E0XXXX Part xx Invoice xx.xlsm", os.getcwd())

        penndot_number = project_num[-1].split(" ")[-1]
        invoice_name = penndot_number + " Part 01 " + next_invoice.split(" ", 1)[-1] + ".xlsm"
        os.rename("E0XXXX Part xx Invoice xx.xlsm", invoice_name)
        os.startfile(invoice_name)

    def get_project_num(self):
        '''prompt user for number until a valid penndot/prudent project number is given'''
        print("Please enter the prudent project number")
        while True:
            project_number = input(">")
            if (project_number[0].upper() == "E"):
                project_number = self.penndot_to_prudent(project_number)

            prudent_numbers = project_number.split(".")
            regional_dir = prudent_numbers[0]
            project_dir = False
            if self.validate_project_num(prudent_numbers):
                project_dir = self.get_project_dir(prudent_numbers)
                if project_dir:
                    return [regional_dir, project_dir]
            else:
                print("invalid Prudent project number")
                print("retry:")


    def validate_project_num(self, str_array):
        '''checks that 2 elements are in the array and that the two elements make
           up a legitimate directory in S:\FIN...'''
        if len(str_array) != 2:
            return False
        if not(str_array[0].isnumeric() and str_array[1].isnumeric()):
            return False
        if not(len(str_array[0]) == 3 and len(str_array[1]) == 3):
            return False
        return True

    def get_project_dir(self, str_array):
        '''takes project number as a 2 element array and verifies that the directory
           with those numbers exist in S:\FIN. returns directory if True'''
        for directory in os.listdir(r"S:\FIN"+"\\"+str_array[0]):
            if str_array[1] in directory:
                return directory
        else:
            return False


    def get_invoice_directory(self, array):
        for directory in os.listdir(r"S:\FIN"+"\\"+array[0] + "\\" + array[1]):
            if "inv" in directory.lower():
                return directory
        else:
            print("No Invoice Directory Found")
            return(1)


    def create_next_folder(self):
        '''iterate through directories in invoice dir. find highest number invoice,
           create an invoice directory that increments the highest by 1'''
        max_num = 0
        for directory in os.listdir():
            if directory.split(" ")[-1].isnumeric():
                num = directory.split(" ")[-1]
                if int(num) > max_num:
                    max_num = int(num)
        if max_num == 0:
            shutil.copy2(r"R:\Version Control\xl_invoice_form\Invoice Aggregate Worksheet.xlsx", os.getcwd())
        print("enter the end date for the invoice")
        print("(format: yyyy-mm-dd) i.e. 2019-02-19")
        year = input(">")
        next_folder_name = ("{} Invoice {}".format(year, format(max_num + 1, "02")))
        os.mkdir(next_folder_name)
        return (next_folder_name)


    def penndot_to_prudent(self, project_number):
        base = r"S:\FIN"
        for direc in os.listdir(base):
            for sub_dir in os.listdir(os.path.join(base, direc)):
                if sub_dir.split(" ")[-1] == project_number:
                    prudent_num = "{}.{}".format(direc, sub_dir.split(" ")[0].split("-")[0])
                    return(prudent_num)
        return("000000")
