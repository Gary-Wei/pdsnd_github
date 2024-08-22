import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = False
    while not city_input:
        city = input("Would you like to see data for Chicago, New York, or Washington?").lower()
        if city in ('chicago', 'new york', 'washington'):
            city_input = True
        else:
            print("Oops, you have typed something that I don't understand. Please check. :)")

    # get user inupt for filter option
    filter_input = False
    month_input  = False
    day_input    = False
    month = 'all'
    day   = 'all'
    while not filter_input:
        filter = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.').lower()
        if filter == 'none':
            filter_input = True
            month_input  = True 
            day_input    = True
        elif filter == 'month':
            filter_input = True
            day_input    = True
        elif filter == 'day':
            filter_input = True
            month_input  = True
        elif filter == 'both':
            filter_input = True
        else:
            print("Oops, you have typed something that I don't understand. Please check. :)")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while not month_input:
        month = input("Which month? January, February, March, April, May, or June?").lower()
        if month in months:
            month_input = True
            month = months.index(month) + 1
        else:
            print("Oops, you have typed something that I don't understand. Please check. :)")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while not day_input:
        day = input("Which day? Please type your response as an integer (e.g., 1=Sunday)").lower()
        day = int(day)
        if day in range(7):
            day_input = True
            day -= 2
            if day < 0:
                day = 6
        else:
            print("Oops, you have typed something that I don't understand. Please check. :)")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day. Additional columns for trip starting month, day of week and hour are added.
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # conver the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # list of day of week names
    dow = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = calendar.month_name[popular_month]
    print('Most Popular Start Month: {}.'.format(popular_month))

    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    popular_dow = dow[popular_dow]
    print('Most Popular Start Day of Week: {}.'.format(popular_dow))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}.'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Popular End Station: {}.'.format(popular_end))
    

    # display most frequent combination of start station and end station trip
    # extract only the start and end station
    popular_route = df[['Start Station', 'End Station']]
    # find the most popular route
    popular_route = popular_route.apply(tuple, axis = 1).mode()[0]
    print('Most Popular Trip: From {} to {}.'.format(popular_route[0], popular_route[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is {} minute(s).'.format(total_time))


    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The average travel time is {} minute(s).'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    for type, counts in zip(user_count.keys(), user_count.values):
        print("There are {} {}.".format(counts, type))


    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        for type, counts in zip(gender_count.keys(), gender_count.values):
            print("There are {} {}.".format(counts, type))
    except:
        print("We don't have gender information for this place!")

    # Display earliest, most recent, and most common year of birth
    try:
        year_of_birth = df['Birth Year']
        earliest = int(year_of_birth.min())
        latest   = int(year_of_birth.max())
        common   = int(year_of_birth.mode()[0])
        print('The earliest year of birth is {}.'.format(earliest))
        print('The most recent year of birth is {}.'.format(latest))
        print('The most common year of birth is {}.'.format(common))
    except:
        print("We don't have birth year information for this place!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Display the raw data from the csv file """
    i = 0
    raw = input("Do you want to see the raw data?").lower() 
    pd.set_option('display.max_columns',200)


    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':          
            if i+5 <= len(df): # if there are enough records to show
                # print five records
                print(df[i:i+5]) 
            else:
                # print the remaining records
                print(df[i:])
            raw = input("Do you want to see more raw data?").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
