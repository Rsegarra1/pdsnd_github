import pandas as pd
import numpy as np
import matplotlib as plt
import time

#import the CSV datas for the respective cities
new_york = pd.read_csv("./new_york_city.csv")
chicago = pd.read_csv("./chicago.csv")
washington = pd.read_csv("./washington.csv")
cities = [new_york,chicago,washington]
# Lets add the missing columns for washington
washington['Gender'] = np.nan
washington['Birth Year'] = pd.Series(dtype='Int64')
# trip diration should be an int but looks like we got a float!
washington['Trip Duration'] = washington['Trip Duration'].round(0).astype('Int64')

# each df has an unnamed so lets remove it as it appears to not be relevent
for city in cities:
    city.drop(columns='Unnamed: 0', inplace=True)
    city['Start Time'] = pd.to_datetime(city['Start Time'])
    #city['Birth Year'] = city['Birth Year'].astype('Int64')
    city['Hour'] = city['Start Time'].dt.strftime('%I %p').str.lstrip('0')
    city['Month'] = city['Start Time'].dt.month_name().str.upper()
    city['Day'] = city['Start Time'].dt.day_name().str.upper()
    city['Day Type'] = city['Start Time'].dt.weekday.apply(lambda x: 'WEEKEND' if x >= 5 else 'WEEKDAY')
    city['Trip'] = city['Start Station'].astype(str) + ' TO ' + city['End Station'].astype(str)

# Let's also add where the source is from!
new_york['City'] = 'NEW YORK'
chicago['City'] = 'CHICAGO'
washington['City'] = 'WASHINGTON'

# We can now union them together!
bikeshare = pd.concat(cities)


def filters(df):
    '''
        This function prompts user for filtering options
    '''
    bikeshare_df_copy = df.copy()
    unique_cities = list(bikeshare_df_copy['City'].unique())
    unique_cities.append('ALL')

    city = input(f'What city do you want to filter the data for?\nChoose from the following list: {unique_cities}\n...').upper().strip().replace(' ','')
    try:
        while city not in unique_cities:
            if city == 'NEWYORK':
                city = 'NEW YORK'
            else:
                city = input(f'The city you selected [{city}] is not in the approved list...\nPlease reselect city {unique_cities}...').upper().strip().replace(' ','')
    except Exception as e:
        print(f'An error occured resulting in failure. Please review error:\n{e}')

    if city == 'ALL':
        bikeshare_df_copy
    else:
        bikeshare_df_copy = bikeshare_df_copy[bikeshare_df_copy['City'] == city]
    time.sleep(1)

    unique_months = list(bikeshare_df_copy['Month'].unique())
    unique_months.append('ALL')
    month = input(f'What month do you want to filter the data for?\nChoose from the following list: {unique_months}\n...').upper().strip().replace(' ','')
    try:
        while month not in unique_months:
            month = input(f'Selected Month of {month} is not avaliable. Please select from the options listed {unique_months}').upper().strip().replace(' ','')

    except Exception as e:
        print(f'An error occured resulting in failure. Please review error:\n{e}')

    if month == 'ALL':
        bikeshare_df_copy
    else:
        bikeshare_df_copy = bikeshare_df_copy[bikeshare_df_copy['Month'] == month]
    time.sleep(1)

    unique_day = list(bikeshare_df_copy['Day'].unique())
    unique_day.append('ALL')
    day = input(f'What day do you want to filter the data for?\nChoose from the following list: {unique_day}\n...').upper().strip().replace(' ','')
    try:
        while day not in unique_day:
            day = input(f'Selected Month of {day} is not avaliable. Please select from the options listed {unique_day}').upper().strip().replace(' ','')

    except Exception as e:
        print(f'An error occured resulting in failure. Please review error:\n{e}')

    if day == 'ALL':
        bikeshare_df_copy
    else:
        bikeshare_df_copy = bikeshare_df_copy[bikeshare_df_copy['Day'] == day]
    time.sleep(1)

    return (bikeshare_df_copy,city,month,day)



recalculate = 'Y'

while recalculate =='Y':
    df, city,month,day = filters(bikeshare)
    print(f'The following results are for the selected choices of\nCITY SELECTION: {city} | MONTH SELECTION: {month} | DAY SELECTION: {day}')
    print('-----------------------------------------------------------------------------')
    print('QUESTION SET 1: Popular times of travel')
    print('')
    print(f'Most common Month of Usage: {df["Month"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'Most common Week Type of Usage: {df["Day Type"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'Most common Day of Usage: {df["Day"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'Most common hour of Usage: {df["Hour"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print('QUESTION SET 2: Popular stations and trip')
    print('')
    print(f'The most common start station was {df["Start Station"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'The most common end station was {df["End Station"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'The most common trip was {df["Trip"].mode()[0]}')
    print('-----------------------------------------------------------------------------')
    print('QUESTION SET 3: Trip duration')
    time.sleep(1)
    print(f'The total travel time for was {df["Trip Duration"].sum()} minutes or {df["Trip Duration"].sum()/60} hours')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print(f'The average travel time was {df["Trip Duration"].mean()} minutes or {df["Trip Duration"].mean()/60} hours')
    print('-----------------------------------------------------------------------------')
    time.sleep(1)
    print('QUESTION SET 4: User info')
    print('')
    print(f'Counts of each user type:')
    time.sleep(1)
    print(df['User Type'].value_counts())
    print('-----------------------------------------------------------------------------')
    time.sleep(1)

    if city != 'WASHINGTON':
        if city == 'ALL':
            print(f'Counts of each gender for CHICAGO')
            print(df[df['City']=='CHICAGO']['Gender'].value_counts())
            print('-----------------------------------------------------------------------------')
            print(f'Counts of each gender for NEW YORK')
            print(df[df['City']=='NEW YORK']['Gender'].value_counts())
            print('-----------------------------------------------------------------------------')
            print('WASHINGTON has no avaliable gender infromation...')
            print('-----------------------------------------------------------------------------')
            print(f'Counts of each gender for ALL cities')
            print(df[(df['City']=='NEW YORK')|(df['City']=='CHICAGO')]['Gender'].value_counts())
            print('-----------------------------------------------------------------------------')
            print(f'Birth year information is as follows...')
            print(f"Youngest Birth Year: {df['Birth Year'].max()}\nOldest Birth Year: {df['Birth Year'].min()}\nMost common Birth year: {df['Birth Year'].mode()[0]}")
            print('-----------------------------------------------------------------------------')
            print(f"Youngest Birth Year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].max()}\nOldest Birth Year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].min()}\nMost common Birth year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].mode()[0]}")
            print('-----------------------------------------------------------------------------')
            print(f"Youngest Birth Year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].max()}\nOldest Birth Year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].min()}\nMost common Birth year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].mode()[0]}")
        elif city == 'CHICAGO':
                print(f'Counts of each gender for CHICAGO')
                print(df[df['City']=='CHICAGO']['Gender'].value_counts())
                print('-----------------------------------------------------------------------------')
                print(f'Birth year information is as follows...')
                print(f"Youngest Birth Year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].max()}\nOldest Birth Year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].min()}\nMost common Birth year in CHICAGO: {df[df['City']=='CHICAGO']['Birth Year'].mode()[0]}")
                print('-----------------------------------------------------------------------------')
        else:
            print(f'Counts of each gender for NEW YORK')
            print(df[df['City']=='NEW YORK']['Gender'].value_counts())
            print('-----------------------------------------------------------------------------')
            print(f'Birth year information is as follows...')
            print(f"Youngest Birth Year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].max()}\nOldest Birth Year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].min()}\nMost common Birth year in NEW YORK: {df[df['City']=='NEW YORK']['Birth Year'].mode()[0]}")
            print('-----------------------------------------------------------------------------')

    raw = input('Do you wish to see the first 5 records of raw data?... [Y/N] ').upper().strip()
    if raw == 'Y':
        indx = 5
        print(df.iloc[:indx])
        time.sleep(1)
        continue_data = input('Continue with next 5 raw data records?... [Y/N] ').upper().strip()
        indx +=5
        try:
            while (continue_data =='Y'):
                if indx <= int(len(df)-5):
                    print(df.iloc[indx:(indx+5)])
                    indx +=5
                    time.sleep(1)
                    continue_data = input('Continue with next 5 raw data records?... [Y/N] ').upper().strip()
                else:
                    print(df.iloc[int(len(df)-5):])
        except Exception as e:
                print(f'An error has occured. Please see the following {e}\nThis is likeley due to an incorrect response to the continue statement.')

    recalculate = input(f'Do you wish to restart the program? [Y/N]...').upper().strip().replace(' ','')
else:
    print('Thank you for diving into the bikeshare data!')
    recalculate = 'N'
