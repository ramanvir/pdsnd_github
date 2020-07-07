import pandas as pd

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']
day_of_week = ['monday', 'tuesday', 'wednesday',
               'thursday', 'friday', 'saturday', 'sunday']

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Start Hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        day = day_of_week.index(day)
        df = df.loc[df['day_of_week'] == day]

    trip_count = df.count()[0]
    trip_count = f"{trip_count:,d}"
    total_trip_duration = round(df['Trip Duration'].sum(),0)
    avg_trip_duration = round(df['Trip Duration'].mean(),0)
    most_popular_station = df['Start Station'].mode()[0]
    most_popular_destination = df['End Station'].mode()[0]
    most_popular_trip = (df['Start Station'] + ' TO ' + df['End Station']).mode()[0]
    most_popular_month = months[df['month'].mode()[0] -1].title()
    most_popular_day = day_of_week[df['day_of_week'].mode()[0]].title()
    most_popular_hour = df['Start Hour'].mode()[0]

    txt = "A total of {} trips were taken. Avg. trip duration was {} and total trip duration was {}. \nPopular month - {}, Popular day - {}, Popular hour - {}. \nMost popular starting station was {} and most popular destination was {}."

    print(txt.format(trip_count, avg_trip_duration, total_trip_duration, most_popular_month, most_popular_day, most_popular_hour, most_popular_station, most_popular_destination))
    print("Most popular trip was - {}.\n".format(most_popular_trip))

    user_types = df['User Type'].value_counts()

    for user_type, num in user_types.items():
        print('{} {}s took trips.'.format(num, user_type))

    print('\n')

    if 'Gender' in df.columns and 'Birth Year' in df.columns:

        gender_stats = df['Gender'].value_counts()

        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        common_birth_year = df['Birth Year'].mode()[0].astype(int)

        for gender, num in gender_stats.items():
            print('{} of {}s took trips.'.format(num, gender))

        print('\n')

        print('Birth year youngest user - {}. Birth year of oldest user - {}. Most common birth year among users - {}.'.format(min_birth_year, max_birth_year, common_birth_year))

        print('\n')

    return df

x = 'yes'

while x == 'yes':

    next = 'next'
    row_counter = 0
    print('\n')
    print("Welcome to BikeShare Data Reporting Program.")
    print('\n')
    print("You can check the data of any of the following cities and filter by 'month' and 'day of the week'.")
    print('\n')

    for city_name, val in city_data.items():
        print(city_name)
        print('\n')

    tester = 1
    while tester == 1:
        city = input('Please enter the city name - ').lower()
        if city_data.get(city) is None:
            city = print('Please enter the correct input of city name. ')
        else:
            tester = 0
    print('\n')
    tester=1
    while tester == 1:
        month = input('Please enter month name or \'all\' - ').lower()
        if month in months or month == 'all':
            tester = 0
        else:
            month = print('Please enter the correct input of month. ')
    print('\n')
    tester=1
    while tester == 1:
        day = input('Please enter a day name or \'all\' - ').lower()
        if day in day_of_week or day == 'all':
            tester = 0
        else:
            day = print('Please enter the correct input of day of the week. ')
    print('\n')
    df = load_data(city, month, day)

    while True:
        try:
            view_rows = input('Enter \'yes\' if you want to view detailed report ')
            print('\n')
            break
        except:
            print("Please provide correct input.")

    if view_rows == 'yes':
        while next == 'next':
            print(df.iloc[row_counter:row_counter+5, 0:8])
            next = input('Type \'next\' if you want to see next 5 rows of the data. Type any key and press enter to exit. ')
            row_counter = row_counter+5+1
            print('\n')

    x = input('Type \'yes\' if you want to run this program again. Type any key and press enter to exit. ')
    print('\n')
