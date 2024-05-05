

import requests
import pprint
import pandas as pd
import json
import math


race_schedule_url = "http://ergast.com/api/f1.json"


def main_request(url,off_set_num):

    response = requests.get(race_schedule_url + f"?offset={off_set_num}")

    get_data = response.json()

    return get_data



def race_parser(get_response):
    my_race_list = []

    for race in range(0,len(get_response["MRData"]["RaceTable"]["Races"])):
        a_race = {
                            
                'season':get_response["MRData"]["RaceTable"]["Races"][race]["season"],
                
                'round':get_response["MRData"]["RaceTable"]["Races"][race]["round"],
                
                'url':get_response["MRData"]["RaceTable"]["Races"][race]["url"],
                
                'raceName':get_response["MRData"]["RaceTable"]["Races"][race]["raceName"],
                
                'circuitID':get_response["MRData"]["RaceTable"]["Races"][race]["Circuit"]["circuitId"],
                
                'CircuitName':get_response["MRData"]["RaceTable"]["Races"][race]["Circuit"]["circuitName"],
                
                'Locality':get_response["MRData"]["RaceTable"]["Races"][race]["Circuit"]["Location"]["locality"],

                'country':get_response["MRData"]["RaceTable"]["Races"][race]["Circuit"]["Location"]["country"],

                'eventDate':get_response["MRData"]["RaceTable"]["Races"][race]["date"],
            }
      
        my_race_list.append(a_race)

    return my_race_list




def main():
    """
    Description: fetches races data from Formula 1 api and transforms it from json to a csv format
    """
    initial_response = requests.get(race_schedule_url)

    data = initial_response.json()

    total = float(data["MRData"]['total'])
    limit = float(data["MRData"]['limit'])
    calls = math.ceil(total/limit)

    races_data = []

    for call in range(0,calls):

        x = int(call*limit)
        
        data = main_request(race_schedule_url,x)

        parsed_data = race_parser(data)

        races_data.extend(parsed_data)

    my_df = pd.DataFrame(races_data)
    my_df.to_csv("races.csv",index=False)
        
        



if __name__ == '__main__':
    main()

