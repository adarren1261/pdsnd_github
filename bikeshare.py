import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cityValid = None
    while( cityValid is None ):
        selected_city = input('What city to do you want to analyze? (washington, new york city, or chicago)\n').lower()
        cityValid = CITY_DATA.get( selected_city )
        if cityValid is None :
            print('Invalid entry please try again')
        else:
            city = selected_city
            break
            
                        

    # TO DO: get user input for month (all, january, february, ... , june)
    months = {'january', 'february', 'march', 'april', 'may', 'june'}
    
    while True :
        selected_month = input('What month to do you want to analyze? (all, january, february, ... , june)\n').lower()
        if selected_month in months or selected_month == 'all' :
            month = selected_month
            break
        else:
            print('Invalid entry please try again')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_of_week = {'monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    
    while True :
        selected_day = input('What day to do you want to analyze? (all, monday, tuesday, ... sunday)\n').lower()
        if selected_day in days_of_week or selected_day == 'all' :
            day = selected_day
            break
        else:
            print('Invalid entry please try again')

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
      # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    ####print( df['month'].value_counts().index[0] )
    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    max_month =  months[df['month'].value_counts().index[0] - 1]
    print( 'Most common month is {}'.format( max_month.title() ) )
    # TO DO: display the most common day of week
    max_day = df['day_of_week'].value_counts().index[0]
    print( 'Most common day of the week is {}'.format( max_day ) )
    # TO DO: display the most common start hour
    max_hour = df['Start Time'].dt.hour.value_counts().index[0]
    print( 'Most common hour of the day is {}'.format( max_hour ) )
          
         
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    max_Start_station = df['Start Station'].value_counts().index[0]
    print( 'Most common start station is {}.'.format( max_Start_station ) )
    
    # TO DO: display most commonly used end station
    max_End_station = df['End Station'].value_counts().index[0]
    print( 'Most common end station is {}.'.format( max_End_station ) )
          
    # TO DO: display most frequent combination of start station and end station trip
    df_stations = df.groupby(['Start Station','End Station']).size().reset_index(name='Count').sort_values(by=['Count'],ascending=False)

    ###print(df_stations.head(3) )
    print('The most common start and end station combination is from {} to {}.'.format(df_stations['Start Station'].iloc[0], df_stations['End Station'].iloc[0] ) )
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print( 'Total trip time was about {} about hours.'.format(df['Trip Duration'].sum()//3600) )

    # TO DO: display mean travel time
    print( 'Average trip time was about {} minutes.'.format(df['Trip Duration'].mean()//60) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print( 'Here the different user types: \n {}.'.format(df['User Type'].value_counts() ) )

    # TO DO: Display counts of gender
    try:
        print( '\nHere the gender counts: \n {}.'.format(df['Gender'].value_counts() ) )
    except KeyError:
        print('\nThere is no gender data in this dataset.\n')
        
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print( df['Birth Year'].head(5) )
        print('\nThe earliest birth year is {}'.format(df['Birth Year'].min() ) )
        print('\nThe most recent birth year is {}'.format(df['Birth Year'].iloc[0] ) )
        print('\nThe most common birth year is {}'.format(df['Birth Year'].value_counts().index[0] ) )
        print("\nThis took %s seconds." % (time.time() - start_time))
    except KeyError:
        print('\nThere is no birth-year data in this dataset.\n')
            
      
    print('-'*40)

def raw_data(df):
    """
    Allows the user to view the loaded and filtered raw data.
    
    """
        
    view_raw_data = input('\nWould you like to view the raw data? Enter yes or no.\n')
    index = 0
    increment = 5
    while view_raw_data.lower() == 'yes':
        print( df.iloc[ index : index+increment ] )
        index += 5
        view_more = input('Continue viewing data? Enter yes or no.\n')
        if view_more.lower() == 'yes':
            continue
        else: 
            break            
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
