import platform
import os
import time
import pandas as pd
import numpy as np

# Python and Pandas documentation has been heavily utilised alongside Udacity learning materials during the production of this tool.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\n', '#'*42, '\nHello! Let\'s explore some US bikeshare data using Bert\'s BAT!', '\n', '#'*42)
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nPlease enter the city you would like to filter by: \n').lower()
    while city not in CITY_DATA.keys():
        city = input("\nSorry, we don't hold data for that city. Please select another city from the available cities: Chicago, New York City, Washington \n").lower()

    # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    month = input("\nPlease enter the month you would like to filter by, or enter all: \n").lower()
    while month not in valid_months:
        month = input("\nSorry, we don't hold data for that month or the inpuit was invalid. Please select another month or enter all: \n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("\nPlease enter the day of the week you would like to filter by, or enter all:\n").lower()
    while day not in valid_days:
        day = input("Invalid input. Please enter the day of the week you would like to filter by, or enter all:\n").lower()
    
    print('-'*40)
    
    print('\nYou have selected to see data for {}\n'.format(city.title()))
    
    if month == 'all':
        print('\nYou have selected to see data for all months\n')
    else:
        print('\nYou have selected to see data for {}\n'.format(month.title()))
        
    if day == 'all':
        print('\nYou have selected to see data for all days\n')
    else:
        print('\nYou have selected to see data for {}s\n'.format(day.title()))

    input('Press ENTER to continue')
    
    print('-' * 40)
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

# Load relevant csv file for chosen city
    print('\nLoading data...')
    df = pd.read_csv(CITY_DATA[city])

# Convert start time column to date time format, rather than string
    print('\nconverting start time to datetime format...')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
# Convert end time column to date time format, rather than string
    print('\nConverting end time to datetime format...')
    df['End Time'] = pd.to_datetime(df['End Time'])
# Create a new column for named months, rather than use numbers, for better user experience
    print('\nCreating additional columns of derived data....')
    df['Month'] = df['Start Time'].dt.month_name()
# Create new column for named days, rather than use numbers, for better user experience
    df['Day'] = df['Start Time'].dt.day_name()
# Create new column for hour in which hire period began to make statistical generation easier
    df['Hour'] = df['Start Time'].dt.hour

# If specific month is chosen, then update filter
    if month != 'all':
        print('\nCreating new dataframe filtered by month...')
        df = df[df['Month'] == month.title()]

# If specific day of week is chosen, then update filter
    if day != 'all':
        print('\nCreating new dataframe filtered by day...')
        df = df[df['Day'] == day.title()]

    print('\nReturning new df for later use...')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = '\nThe most common month is {}'.format(df['Month'].mode()[0])
    print(mode_month)

    # TO DO: display the most common day of week
    mode_day = '\nThe most common day is {}'.format(df['Day'].mode()[0])
    print(mode_day)

    # TO DO: display the most common start hour
    if df['Hour'].mode()[0] < 10:
        mode_hour_start = '\nThe most common time to start a hire period is between 0{}00-0{}59'.format(df['Hour'].mode()[0],df['Hour'].mode()[0])
    else:
        mode_hour_start = '\nThe most common time to start a hire period is between {}00-{}59'.format(df['Hour'].mode()[0],df['Hour'].mode()[0])
    print(mode_hour_start)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mode_origin = '\nThe most common starting station is {}'.format(df['Start Station'].mode()[0])
    print(mode_origin)
    

    # TO DO: display most commonly used end station
    mode_destination = '\nThe most common destination station is {}'.format(df['End Station'].mode()[0])
    print(mode_destination)

    # TO DO: display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' to ' +  df['End Station']
    mode_combo = '\nThe most common combination of start station and end station is {}'.format(df['Route'].mode()[0])
    print(mode_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = '\nTotal travel time was %s hours' % (df['Trip Duration'].sum()/3600)
    print(total_trip_duration)

    # TO DO: display mean travel time
    mean_trip_duration = '\nMean travel time was %s minutes' % (df['Trip Duration'].mean()/60)
    print(mean_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = df.groupby(['User Type']).size().sort_values(ascending=False)
        print('\n')
        print(user_types)
    except:
        print('\nThere is no user type data recorded for this dataset') 
    

    # TO DO: Display counts of gender
    try:
        gender_count = df.groupby(['Gender']).size().sort_values(ascending=False)
        print('\n')
        print(gender_count)
    except:
        print('\nThere is no gender data recorded for this dataset')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        mode_birth_year = int(df['Birth Year'].mode()[0])
        print('\nThe oldest user was born in', oldest_user)
        print('\nThe youngest user was born in', youngest_user)
        print('\nThe most common birth year of users was', mode_birth_year)
    except:
        print('\nThere is no age data for this dataset')

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def clear():
    current_os = platform.system()
    if current_os == 'Linux':
        os.system('clear')
    elif current_os == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
        
def raw_data_display(df):
    """Displays dataframe 5 rows at a time"""
    clear()
    # Sets to display all columns where screen size is too small for full table
    pd.set_option('max_columns', None)
    print(df.head())
    more_data = input('\nWould you like to see the next 5 rows of data? Enter yes or no:\n').lower()
    line_location = 5
    # Prints next 5 lines if requested by user
    while more_data == 'yes':
        print(df[line_location:line_location+5])
        line_location += 5
        more_data = input('\nWould you like to see te next 5 rows of data? Enter yes or no:\n').lower()
        

def main():
    while True:
        clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        clear()
        time_stats(df)
        input('\nPress ENTER to continue')
        
        clear()
        station_stats(df)
        input('\nPress ENTER to continue')
        
        clear()
        trip_duration_stats(df)
        input('\nPress ENTER to continue')    
        
        clear()
        user_stats(df)
        
        clear()
        raw = input('\nWould you like to view the raw data summarised above? Enter yes or no.\n').lower()
        if raw == 'yes':
            raw_data_display(df)
        else:
            print('\nSkipping display of raw data')
                  

        clear()
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            print('#' * 42)
            print("\nThanks for using Bert's BAT  today!\n")
            print('#' * 42)
            break


if __name__ == "__main__":
	main()


