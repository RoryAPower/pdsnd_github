import time
import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_city_data():
    cities = list(CITY_DATA.keys())
    assert cities == ['chicago', 'new york city', 'washington']


INPUT_DATA = {
    'city': {
        'data': list(CITY_DATA.keys()),
        'question': 'Please enter one of the following cities - Chicago, New York City or Washington: ',
        'prompt': 'This is not a valid city for analysis purposes.\nThe only available cities are Chicago, New York City or Washington.'
    },
    'month': {
        'data': ['january', 'february', 'march', 'april', 'may', 'june'],
        'question': 'Please enter a month between January and June - leave blank to search all months: ',
        'prompt': 'This is not a valid month for analysis purposes.\nThe only valid months range from January to June inclusive.'
    },
    'day': {
        'data': ['monday', 'tuesday', 'wednesday',
                 'thursday', 'friday', 'saturday', 'sunday'],
        'question': 'Please enter a day of the week - leave blank to search all days: ',
        'prompt': 'This is not a valid day for analysis purposes.\nThe only valid days range from Monday to Sunday inclusive.'
    }
}


def get_input(input_type, optional_input=True):
    '''
    Deal with user input.

    Args:
        (str) input_type - the type of data used to build the question functionality
        (bool) optional_input - allows for optional or required input
    Returns:
        (str|None) user_input - the information the user has input
    '''
    user_input = None

    input_data = INPUT_DATA.get(input_type)

    while user_input is None or user_input not in input_data.get('data'):
        question = input_data.get('question')
        user_input = input(question).lower()

        if(optional_input and len(user_input) == 0):
            user_input = None
            break

        if user_input not in input_data.get('data'):
            print(input_data.get('prompt'))

    return user_input


def get_raw_input(df, number_to_show=5):
    '''
    Deal with raw input.

    Args:
        (DataFrame) df - Pandas DataFrame
        (int) - number of results to show
    '''

    df_slice = 0
    answer = 'yes'
    first_question = 'Would you like to view {} lines of raw data? (The results will be ordered as per your initial input - Enter yes or no) '.format(
        number_to_show)
    continue_question = 'Would you like to view the next {} lines of raw data? (Enter yes or no) '.format(
        number_to_show)
    all_data_viewed = 'All raw data has now been viewed'

    while answer == 'yes':
        question = first_question if df_slice == 0 else continue_question
        answer = input('\n' + question)

        if answer != 'yes':
            return

        # grab the raw data
        raw_rows = df.iloc[df_slice:df_slice+number_to_show]
        number_of_rows = len(raw_rows)

        if number_of_rows > 0:
            # remove first column (has no real meaning for user)
            # remove columns that were added to do calculation work
            formatted_raw_rows = raw_rows.drop(
                raw_rows.columns[[0, -1, -2, -3]], axis=1)

            print('\n' + formatted_raw_rows.to_string())

        # partial rows returned - none left to view
        if number_of_rows < number_to_show:
            print('\n' + all_data_viewed)
            return

        df_slice += number_to_show


def print_gender_count_data(df):
    '''Displays the counts for genders where available.'''

    if 'Gender' not in df:
        print('Gender data unavailable for this city' + '\n')
        return

    print('The counts of genders are - ')
    gender_count = df['Gender'].value_counts()
    print(gender_count.to_string() + '\n')


def print_birth_year_data(df):
    '''Displays birth year data where available.'''

    if 'Birth Year' not in df:
        print('Year of birth data unavailable for this city')
        return

    earliest_birth_year = int(df['Birth Year'].min())
    print('The earliest birth year is {}'.format(earliest_birth_year))

    most_recent_birth_year = int(df['Birth Year'].max())
    print('The most recent birth year is {}'.format(most_recent_birth_year))

    most_common_birth_year = int(df.mode()['Birth Year'][0])
    print('The most common birth year is {}'.format(most_common_birth_year))


def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    '''

    print('Hello! Let\'s explore some US bikeshare data!')

    # get city input
    city = get_input('city', optional_input=False)

    # get month input
    month = get_input('month')

    # get day input
    day = get_input('day')

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    '''
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    '''

    # create panda series from city data
    df = pd.read_csv(CITY_DATA.get(city))

    # convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # add month from datetime
    df['month'] = df['Start Time'].dt.month_name()
    # add day from datetime
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # month filtering
    if month is not None:
        df = df[df.month.eq(month.title())]

    # day filtering
    if day is not None:
        df = df[df.day_of_week.eq(day.title())]

    return df


def time_stats(df):
    '''Displays statistics on the most frequent times of travel.'''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # get most common month
    most_common_month = df.mode()['month'][0]
    print('The most common month is {}'.format(most_common_month))

    # get most common day
    most_common_day = df.mode()['day_of_week'][0]
    print('The most common day of the week is {}'.format(most_common_day))

    # get most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_start_hour = int(df.mode()['start_hour'][0])
    print('The most common start hour is {} (24 hour clock)'.format(
        most_common_start_hour))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    '''Displays statistics on the most popular stations and trip.'''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # get most common start station
    most_common_start_station = df.mode()['Start Station'][0]
    print('The most most commonly used start station is \'{}\''.format(
        most_common_start_station))

    # get most common end station
    most_common_end_station = df.mode()['End Station'][0]
    print('The most most commonly used end station is \'{}\''.format(
        most_common_end_station))

    # get most frequent combination of start and end station
    frequent_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip is \'{}\' and \'{}\''.format(
        frequent_combination[0], frequent_combination[1]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    '''Displays statistics on the total and average trip duration.'''

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # get total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('The total travel time is {}'.format(total_travel_time))

    # get mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('The mean travel time is {}'.format(mean_travel_time))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    '''Displays statistics on bikeshare users.'''

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display user types count
    print('The counts for user types are - ')
    user_types_count = df['User Type'].value_counts()
    print(user_types_count.to_string() + '\n')

    # Display genders count
    print_gender_count_data(df)

    # Display earliest, most recent, and most common year of birth
    print_birth_year_data(df)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    try:
        check_city_data()
    except AssertionError:
        print('Cities do not match, exiting program')
        return

    while True:
        city, month, day = get_filters()

        try:
            df = load_data(city, month, day)
        except Exception as e:
            print('We are sorry there seems to be a problem with our data\n' +
                  str(e) + '\nexiting program')
            return

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_input(df, 10)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()
