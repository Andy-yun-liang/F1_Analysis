
import requests
from pprint import pprint
import pandas as pd
import json
import math


url = "http://ergast.com/api/f1/constructors.json"


def get_constructor_data(url,offset_num):
    response = requests.get(url + f"?offset={offset_num}")
    data = response.json()
    return data

def parse_constructors(data):
    dataset = []
    for constructor in range(0,int(len(data["MRData"]['ConstructorTable']['Constructors']))):
        row = {
            'constructorId':data['MRData']['ConstructorTable']['Constructors'][constructor]['constructorId'],
            'name':data['MRData']['ConstructorTable']['Constructors'][constructor]['name'],
            'nationality':data['MRData']['ConstructorTable']['Constructors'][constructor]['nationality']
        }
        dataset.append(row)
    return dataset 



def main(url):
    """
    Description: Fetches basic information such as natinality and name of Constructors
    """

    response = requests.get(url)

    get_data = response.json()

    total = float(get_data['MRData']['total'])
    limit = float(get_data['MRData']['limit'])

    calls = int(math.ceil(total/limit))

    finalized_data = []

    for call in range(0,calls):
        offset_num = call*limit
        data = get_constructor_data(url,offset_num)
        parsed_data = parse_constructors(data)
        finalized_data.extend(parsed_data)

    finalized_data = pd.DataFrame(finalized_data)
    finalized_data.to_csv("constructorInformation.csv",index=False)


if __name__ == "__main__":
    main(url)



