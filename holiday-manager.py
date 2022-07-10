#Import relevant packages
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import inspect
from config import jsonlocation

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

    def read_json(self, jsonlocation):
        # Read in things from json file location
        with open(jsonlocation, 'r') as f:
            data = json.load(f)
            f.close()
        # Use addHoliday function to add holidays to inner list.
        for holiday in data['holidays']:
            holiday_name = holiday['name']
            holidate = holiday['date']
            date_format = '%Y-%m-%d'
            formatted_date = datetime.strptime(holidate, date_format).date()
            holidayobj = Holiday(holiday_name, formatted_date)
            self.addHoliday(holidayobj)

    def save_to_json(self, jsonlocation):
        #Makee empty holiday dictionary list
        holiday_dict_list= {"holidays" : []}
        #Gather individual holiday objects from innerHoliday list and append to holiday dict list
        for holiday in self.innerHolidays:
            holiday_name = holiday.name
            holidate = holiday.date
            date_format = '%Y-%m-%d'
            date = datetime.strftime(holidate, date_format)
            holiday_dict = {'name': holiday_name, 'date': date}
            holiday_dict_list['holidays'].append(holiday_dict)
        # Write out json file to selected file.
        with open(jsonlocation, 'w') as f:
            json.dump(holiday_dict_list, f, sort_keys = True, indent = 4)
            f.close()

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter innerHolidays by week number and year
        filtered_hol_list = list(filter(lambda x : x.date.isocalendar()[1] == week_number and x.date.isocalendar()[0] == year, self.innerHolidays))
        # return your filtered holidays
        return filtered_hol_list

    def displayHolidaysInWeek(self, year, week_number):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        filt_hol_list = self.filter_holidays_by_week(year, week_number)
        # Output formated holidays in the week.
        for hol in filt_hol_list:
            print(hol)



#UI Start Up
##
def StartUp(holiday_list):
    #Find number of holidays stored in system
    num_holidays = holiday_list.numHolidays()
    print(f'''
        Holiday Management
        =================================
        There are {num_holidays} holidays stored in the system
    ''')
    
    #MainMenu()

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

#UI Save Holiday List
##
def SaveHolidayList(holiday_list):
    #Print welcome message
    print(f'''
        Save Holiday List
        ===================
    ''')
    #User save input
    user_save = str(input('Are you sure you want to save your changes? [y/n]: ')).lower()
    #Check user response
    if user_save == 'n':
        print('''
            Cancelled:
            Holiday list file save cancelled.
        ''')
    elif user_save == 'y':
        #Save list
        holiday_list.save_to_json(jsonlocation)
        print('''
            Success:
            Your Changes have been saved
        ''')
    
    
    #MainMenu()