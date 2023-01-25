import time
import pandas as pd
import numpy as np
import calendar


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
    print('Hello! Let\'s explore some US bikeshare data!')
    month = ''
    day = ''
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print("Please enter the valid city (chicago or new york city or washington)")
    
    while True:
        filter_input = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter.\n").lower()
        if filter_input == 'month':
        # TO DO: get user input for month (all, january, february, ... , june)
            month = get_month()
            break
        elif filter_input == 'day':
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
            day = get_day()
            break
        elif filter_input == 'both':
        # TO DO: get user input for month and day of week
            month = get_month()
            day = get_day() 
            break
        elif filter_input == 'none':
            break
        else:
            print("Please enter the valid filter")
    
    print('-'*40)
    return city, month, day, filter_input


def get_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - name of the month to filter 
    """
    while True:
        month = int(input("Which month? January, February, March, April, May or June?\nPlease type your response as an integer with 1 as January\n"))
        if month in (1, 2, 3, 4, 5, 6):
            return month
            break
        else:
            print("Please enter the valid month name")
            

def get_day():
    """
    Asks user to specify a day of the week to analyze.

    Returns:
        (str) day - name of the weekday to filter 
    """
    while True:
        day = int(input("Which day? Please type your response as an integer with 0 as Sunday\n"))
        if day in (0, 1, 2, 3, 4, 5, 6):
            return day
            break
        else:
            print("Please enter the valid day of the week")

    
    
def load_data(city, month, day, filter_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month, day, both or none
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    
    if filter_input == 'month':
        df = df[df['month'] == month]
    elif filter_input == 'day':
        df = df[df['day_of_week'] == day]
    elif filter_input == 'both':
        df = df[(df['month'] == month) & (df['day_of_week'] == day)]

    return df


def time_stats(df, filter_input):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if filter_input not in ('month', 'both'):
        # TO DO: display the most common month
        month_number = df['month'].mode()[0]
        print("The most frequent month of travel is : ", calendar.month_name[month_number])
    
    if filter_input not in ('day', 'both'):
        # TO DO: display the most common day of week
        print("The most frequent day of week of travel is : ", df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour of travel is : ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    print("Popular Start Station is : ", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("Popular End Station is : ", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print("Popular combination of Start Station and End Station trip is : ", 
          df.groupby(['Start Station','End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print("Total duration is : ")
    convert_time(tot_travel_time)

    # TO DO: display mean travel time
    avg_travel_time = int(df['Trip Duration'].mean())
    print("Average duration is : ")
    convert_time(avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_time(travel_time):
    """converts seconds into days, hours, minutes and seconds format."""

    days = travel_time // (24 * 3600)
    travel_time = travel_time % (24 * 3600)
    hours = travel_time // 3600
    travel_time = travel_time % 3600
    minutes = travel_time // 60
    travel_time = travel_time % 60
    seconds = travel_time
    print("{} days, {} hours, {} minutes, {} seconds".format(days, hours, minutes, seconds))
    


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of User Types : \n", df.groupby(['User Type']).size())

    if city != 'washington':
        # TO DO: Display counts of gender
        print("Counts of Gender : \n", df.groupby(['Gender']).size())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("Earliest year of birth is : ", int(df['Birth Year'].min()))
        print("Most recent year of birth is : ", int(df['Birth Year'].max()))
        print("Most Common year of birth is : ", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def show_raw_data(df):
    """Displays 5 lines of raw data at a time."""
    
    start, end = 0, 0
        
    while True:
        show_input = input("Would you like to see individual trip data? Please enter 'yes' or 'no'\n").lower()
        if show_input == 'yes':
            start = end
            end += 5
            if end <= (len(df) + 1):
                print(df[start:end])
            else:
                break
        elif show_input == 'no':
            break 
        else:
            print("Please enter the valid value")
      

def main():
    while True:
        city, month, day, filter_input = get_filters()
   
        df = load_data(city, month, day, filter_input)

        time_stats(df, filter_input)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)
                  
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
