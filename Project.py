# Yihnew Eshetu
# yte9pc

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pycountry
import pycountry_convert
import folium

def connection():
   playersData = pd.DataFrame()
   for page in range(1,560):
       # Url address 
       print(page)
       if page < 71:
           url = 'https://www.futbin.com/20/players?page='+str(page)+'&sort=Player_Rating&order=desc&version=gold'
       elif page >= 71 and page < 352:
           url = 'https://www.futbin.com/20/players?page='+str(page-70)+'&sort=Player_Rating&order=desc&version=silver'
       else:
            url = 'https://www.futbin.com/20/players?page='+str(page-351)+'&sort=Player_Rating&order=desc&version=bronze'
            
       # Retrieve data from url
       response = requests.get(url)
       # BeautifulSoup parser
       soup = BeautifulSoup(response.text, 'html.parser')
       rows = soup.find_all('tr')
        
       playersInfo = []
       for row in range(len(rows)):
           
           if row not in range (0, 2):
               cols = rows[row].find_all('td')
               playerInfo = []
               
               for col in range(0,len(cols)):
                   if col == 0:
                       playersName = cols[col].text.strip()
                       playerInfo.append(playersName)
                       playerClubCountryLeague = cols[col].find('span', {'class' : 'players_club_nation'})
                       NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 0, 'data-original-title')
                       NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 1, 'data-original-title')
                       NoneTypeCheck(playerClubCountryLeague, playerInfo, 'a', 2, 'data-original-title')
                   elif col == 7:
                       playerInfo.append(cols[col].text.replace('\\', '/'))
                   elif col == 14:
                       playerInfo.append(cols[col].text.strip().split('cm')[0])
                   elif col not in range(3,5) and col != 15:
                       playerInfo.append(cols[col].text.strip())
               playersInfo.append(playerInfo)
               
       playersData = playersData.append(playersInfo, ignore_index = True)
       
   playersData.columns =  ['Name', 'Club', 'Country', 'League', 'Overall Rating', 'Position',
                           'Skill' , 'Weak Foot', 'Work Rate', 'Pace', 'Shooting', 'Passing',
                           'Dribbling' , 'Defending', 'Physicality', 'Height', 'Base Stats',
                           'In Game Stats']
   playersData.to_csv('FIFA Player Info.csv')
    return(pd.read_csv('FIFA Player Info.csv'))
        
def NoneTypeCheck(data, listname, item = None, iterator = None, get = None):
    if data is not None and get is not None:
        data = data.findAll(item)[iterator]
        data = data.get(get)
        listname.append(data)
    elif data is not None:
        listname.append(data.text)

def position(DFColumn):
    positions = {
            'Attacker' : ['CF', 'ST', 'RW', 'RF', 'LW', 'LF'], 
            'Midfieder' : ['RM', 'LM', 'CAM', 'CM', 'CDM'],
            'Defender' : ['LB', 'LWB', 'RB', 'RWB', 'CB'],
            'Goal Keeper' : ['GK']}
    for position in positions.keys():
        if DFColumn in positions.get(position):
            print(position)
        
def continent(DFColumn):
  countries = {}
  for country in pycountry.countries:
    countries[country.name] = country.alpha_2
  
  for country in DFColumn:
    #print(country)
    if countries.get(country) is not None:
      print(pycountry_convert.country_alpha2_to_continent_code(countries.get(country)))
    elif country == 'Korea Republic':
      print(pycountry_convert.country_alpha2_to_continent_code('KR'))
    elif country == 'Korea DPR':
      print(pycountry_convert.country_alpha2_to_continent_code('KP'))
    elif country == 'Congo DR':
      print(pycountry_convert.country_alpha2_to_continent_code('CD'))
    elif country == 'Cape Verde Islands':
      print(pycountry_convert.country_alpha2_to_continent_code('CV'))
    elif country == 'China PR':
      print(pycountry_convert.country_alpha2_to_continent_code('CN'))
    elif country == 'Republic of Ireland':
      print(pycountry_convert.country_alpha2_to_continent_code('IE'))
    elif country == 'FYR Macedonia':
      print(pycountry_convert.country_alpha2_to_continent_code('MK'))
    elif country == 'St. Kitts and Nevis':
      print(pycountry_convert.country_alpha2_to_continent_code('KN'))
    elif country == 'São Tomé e Príncipe':
      print(pycountry_convert.country_alpha2_to_continent_code('ST'))
    elif country == 'Chinese Taipei':
      print(pycountry_convert.country_alpha2_to_continent_code('TW'))
    elif country == 'St. Lucia':
      print(pycountry_convert.country_alpha2_to_continent_code('LC'))
    else:
      return(pycountry_convert.country_alpha2_to_continent_code(pycountry.countries.search_fuzzy(country)[0].alpha_2))
                          
if __name__ == '__main__':
    DF = connection()
    DF.insert(6, "Position Group", DF['Position'].apply(position), True)
    DF.insert(4, "Continent", DF['Country'].apply(continent) , True)
    #print(continent())
    #print(DF['Continent'])

