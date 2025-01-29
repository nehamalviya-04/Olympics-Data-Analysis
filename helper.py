import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    temp_df = df.drop_duplicates(subset=['Year',col])

    # Count the number of unique regions per Year
    nations_over_time = temp_df['Year'].value_counts().reset_index()

    # Rename columns
    nations_over_time.columns = ['Edition',col]

    # Sort by Edition (Year)
    nations_over_time = nations_over_time.sort_values(by='Edition')

    return nations_over_time

def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the number of medals for each athlete
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge with the original DataFrame to get additional details
    result = medal_counts.merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Medals', 'Sport', 'region']
    ].drop_duplicates('Name')  # Drop duplicates to avoid redundancy

    return result.head(15)  # Return the top 15 athletes

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City',
    'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt= new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
        # Drop rows where 'Medal' is NaN
        temp_df = df.dropna(subset=['Medal'])

        # Filter for a specific country if provided
        if country != 'Overall':
            temp_df = temp_df[temp_df['region'] == country]

        # Count medals for each athlete and get the top 15
        medal_counts = temp_df['Name'].value_counts().reset_index()
        medal_counts.columns = ['Name', 'Medals']  # Rename columns for clarity

        # Merge with the original DataFrame to add 'Sport' and 'region' information
        result = (
            medal_counts
            .head(10)  # Select top 15
            .merge(df[['Name', 'Sport', 'region']], on='Name', how='left')
            .drop_duplicates(subset='Name')  # Drop duplicate entries for the same athlete
        )

        return result

def weight_v_heigh(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport!= "Overall":
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return  temp_df
    else:
       return  athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': "Male", "Name_y": "Female"}, inplace=True)

    final.fillna(0, inplace=True)

    return final