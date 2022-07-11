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
        #Make sure holidayObj is not already in list
        found_hol = self.findHoliday(holidayObj.name, holidayObj.date)
        if found_hol != None:
            print(f'Error: {holidayObj} already exists in list')
            
        elif found_hol == None:
            
            # Make sure holidayObj is a Holiday Object by checking the type
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

    def scrapeHolidays(self):
        current_year = int(datetime.now().isocalendar()[0])
        #Years from current year-2 to current year+2
        for year in range(current_year-2, current_year+3):
            year_str = str(year)
            # Scrape Holidays from https://www.timeanddate.com/holidays/us/2022?hol=33554809
            html = getHTML(f"https://www.timeanddate.com/holidays/us/{year_str}?hol=33554809")
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table', attrs = {'id' : 'holidays-table'})
            #Get each holiday name and date
            for table_entry in table.find_all('tr', attrs = {'class' : 'showrow'}):
                holiday = table_entry.find('a').string
                date = table_entry.find('th').string
                holiday_date = year_str + ' ' + date
                date_format = '%Y %b %d'
                holidate = datetime.strptime(holiday_date, date_format).date()
                # Check to see if name and date of holiday is in innerHolidays array done in addHoliday method
                hol_obj = Holiday(holiday, holidate)
                self.addHoliday(hol_obj)

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

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        current_year = datetime.now().isocalendar()[0]
        current_week = datetime.now().isocalendar()[1]
        # Use your filter_holidays_by_week function to get the list of holidays
        #current_week_hol = self.innerHolidays.filter_holidays_by_week(current_year, current_week)
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(current_year, current_week)
        # Ask user if they want to get the weather
        #get_weather = str(input('Would you like to see the weather? [y/n]: ')).lower()
        # If yes, use your getWeather function and display results
        #if get_weather == 'y':
        #    for hol in



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
    
    MainMenu(holiday_list)

#UI MainMenu
##
def MainMenu(holiday_list):
    print(f'''
        Holiday Menu
        =====================================
    ''')
    #Store user selection from Main Menu
    getting_input = True
    while getting_input:
        try:
            user_selection = int(input('''
                1. Add a Holiday
                2. Remove a Holiday
                3. Save Holiday List
                4. View Holidays
                5. Exit
            '''))
            getting_input = False
        except:
            print('Enter the number again')
    #Point to appropriate directory
    if user_selection == 1:
        AddHoliday(holiday_list)
    elif user_selection == 2:
        RemoveHoliday(holiday_list)
    elif user_selection == 3:
        SaveHolidayList(holiday_list)
    elif user_selection == 4:
        ViewHolidays(holiday_list)
    elif user_selection == 5:
        Exit(holiday_list)

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
            global changes_saved
            changes_saved = False
            
    MainMenu()

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
            global changes_saved
            changes_saved = False
        elif found_holiday == None:
            print(f'''
                Error:
                {holiday_name} not found.
            ''')
         #holiday_list.findHoliday(name, date)
    
    
    MainMenu()

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
    
    
    MainMenu()

#UI View Holidays

def ViewHolidays(holiday_list):
    #Print welcome message
    print(f'''
        View Holidays
        ==============
    ''')
    #User save input
    holiday_year = int(input('Which year?: '))
    #Ensure year is within [current year-2, current_year+2]
    holiday_week = input('Which week? #[1-52, Leave blank for the current week]: ')
    #Print holidays in week
    if holiday_week == '':
        print(f'These are the holidays for this week:')
        holiday_list.viewCurrentWeek()
        
    else:
        holiday_week = int(holiday_week)
        print(f'These are the holidays for {holiday_year} week#{holiday_week}:')
        holiday_list.displayHolidaysInWeek(holiday_year, holiday_week)
    
    
    MainMenu()

#UI Exit
##
def Exit(holiday_list):
    #Print welcome message
    print(f'''
        Exit
        =====
    ''')
    #Check if changes need to be saved
    global changes_saved
    #User exit input
    if changes_saved == True:
        user_exit = str(input('Are you sure you want to exit? [y/n]: ')).lower()
    elif changes_saved == False:
        user_exit = str(input('''
            Are you sure you want to exit?
            Your changes will be lost.
            [y/n]: 
            ''')).lower()
    
    if user_exit == 'n':
        MainMenu()
    elif user_exit == 'y':
        global user_using
        user_using = False