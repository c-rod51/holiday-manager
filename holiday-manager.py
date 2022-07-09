#Import relevant packages
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import inspect

#Holiday class
##
@dataclass
class Holiday:
    name: str
    date: datetime
        
    def __str__ (self):
        # String output
        date_format = '%Y-%m-%d'
        date_str = datetime.strftime(self.date, date_format)
        # Holiday output when printed.
        return '%s (%s) ' % (self.name, date_str)

#HolidayList Class

class HolidayList:
    def __init__(self):
        self.innerHolidays = []
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if isinstance(holidayObj, Holiday):
            # Use innerHolidays.append(holidayObj) to add holiday
            self.innerHolidays.append(holidayObj)
            # print to the user that you added a holiday
            print(f'Success: {holidayObj} has been added to the holiday list.')
        else:
            print('Error: Please try again.')

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        found_holiday = [x for x in self.innerHolidays if x.name == HolidayName and x.date == Date]
        # Return Holiday object
        try:
            found_hol_obj = found_holiday[0]
        except IndexError:
            found_hol_obj = None
        return found_hol_obj

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        
        # remove the Holiday from innerHolidays
        self.innerHolidays = list(filter(lambda x : x.name != HolidayName and x.date != Date, self.innerHolidays))
        # inform user you deleted the holiday
        print(f'''
            Success:
            {HolidayName} has been removed from the list.
        ''')

    def read_json(filelocation):
        pass




#UI Add Holiday
##
def AddHoliday(holiday_list):
    #Print welcome message
    print(f'''
        Add a Holiday
        ==============
    ''')
    #Gather Holiday name from user
    holiday_name = str(input("Holiday: "))
    #Gather Holiday date from user and ensure datetime
    incorrect_form = True
    while incorrect_form:
        try:
            testdate = input('Enter date (YYYY-MM-DD): ')
            date_format = '%Y-%m-%d'
            date = datetime.strptime(testdate, date_format).date()
        except ValueError:
            print('Invalid date. Please try again.')
        else:
            incorrect_form = False
            holiday_object = Holiday(holiday_name, date)
            holiday_list.addHoliday(holiday_object)
            
    #MainMenu()

#UI Remove Holiday
##
def RemoveHoliday(holiday_list):
    #Print welcome message
    print(f'''
        Remove a Holiday
        =================
    ''')
    holiday_not_in_list = True
    while holiday_not_in_list:
        #Gather holiday name from user
        holiday_name = str(input('Holiday Name: '))
        #Gather Holiday date from user and ensure datetime
        incorrect_form = True
        while incorrect_form:
            try:
                testdate = input('Enter date (YYYY-MM-DD): ')
                date_format = '%Y-%m-%d'
                date = datetime.strptime(testdate, date_format).date()
            except ValueError:
                print('Invalid date. Please try again.')
            else:
                incorrect_form = False
    
        #Check if holiday_name is in list
        found_holiday = holiday_list.findHoliday(holiday_name, date)
        if isinstance(found_holiday, Holiday):
            holiday_not_in_list = False
            holiday_list.removeHoliday(holiday_name, date)
        elif found_holiday == None:
            print(f'''
                Error:
                {holiday_name} not found.
            ''')
         #holiday_list.findHoliday(name, date)
    
    
    #MainMenu()