import pandas as pd
import requests
import time
import numpy as np

# set column headers for DataFrame
url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2024-25&SeasonType=Regular%20Season&StatCategory=PTS"
r = requests.get(url).json()
table_headers = r['resultSet']['headers']
df_cols = ['Year', 'Season_type'] + table_headers 

# create lists to manipulate url
df = pd.DataFrame(columns=df_cols)
season_types = ['Regular%20Season', 'Playoffs']
years = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']

begin_loop = time.time()

# web scrape NBA stats
for y in years:
    for s in season_types:
        api_url = f'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season={y}&SeasonType={s}&StatCategory=PTS'
        r = requests.get(url=api_url).json()

        player_df = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
        season_df = pd.DataFrame({'Year':[y for i in range(len(player_df))],
                         'Season_type':[s for i in range(len(player_df))]})
        temp_df = pd.concat([season_df, player_df], axis=1)
        df = pd.concat([df, temp_df], axis=0)
        
        print(f'Finished scraping data for the {y} {s}.')
        lag = np.random.uniform(low=5, high=40) # waiting between requests to prevent having repetitive requests blocked
        print(f'...waiting {round(lag,1)} seconds')
        time.sleep(lag)

print(f'Process completed. Total runtime: {round((time.time()-begin_loop)/60, 2)}')
df.to_excel('nba_player_data.xlsx', index=False)