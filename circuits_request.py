
import requests
from pprint import pprint
import pandas as pd
import json
import math

    
url = "http://ergast.com/api/f1/circuits.json"

def main_request(url,x):
    
    response = requests.get(url +f'?offset={x}')
   
    get_data = response.json()
    return get_data


def circuit_parser(data):

    circuit_list = []

    for circuit in range(0,len(data["MRData"]["CircuitTable"]["Circuits"])):
        each_circuit = {
            'circuitID':data["MRData"]["CircuitTable"]["Circuits"][circuit]['circuitId'],
            'circuitName':data["MRData"]["CircuitTable"]["Circuits"][circuit]['circuitName'],
            'locality':data["MRData"]["CircuitTable"]["Circuits"][circuit]['Location']['locality'],
            'country':data["MRData"]["CircuitTable"]["Circuits"][circuit]['Location']['country'],
            'latitude':data["MRData"]["CircuitTable"]["Circuits"][circuit]['Location']['lat'],
            'longitude':data["MRData"]["CircuitTable"]["Circuits"][circuit]['Location']['long'],
            'url':data["MRData"]["CircuitTable"]["Circuits"][circuit]['url']
        }
        circuit_list.append(each_circuit)

    return circuit_list



def main():
    """
    Description: Fetches circuit data from Formula 1 Api and transform it into csv format
    """
    response = requests.get(url)
    data = response.json()
    total = float(data["MRData"]["total"])
    limit = float(data["MRData"]["limit"])
    calls = math.ceil(total/limit)
    
    circuit_data = []

    for call in range(0,calls):
        x = int(call*limit)
        print(x)
        data = main_request(url,x)
        parsed_data = circuit_parser(data)
        circuit_data.extend(parsed_data)
    
    circuit_df = pd.DataFrame(circuit_data)
    circuit_df.to_csv("circuit.csv",index=False)


if __name__ == "__main__":
    main()

