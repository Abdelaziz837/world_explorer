import requests
import pandas as pd


def get_all_country_info():
    
    info = []
    fields = "name,capital,region,subregion,population,flags,languages,currencies"
    url = f"https://restcountries.com/v3.1/all/?fields={fields}"
    r = requests.get(url)
    data = r.json()

    if r.status_code != 200:
        print("ERROR: ", r.status_code)
        return []
    for item in data:
        try: 
            common = item["name"]["common"]
            capital = item.get("capital" , ["N/A"])[0]
            region = item.get("region" , "N/A")
            subregion = item.get("subregion" , "N/A")
            population = item.get("population" , 0)
            flag = item["flags"]["png"]
            language = list(item["languages"].values())[0] if "languages" in item else "N/A"
            if "currencies" in item:
                currency_data = list(item["currencies"].values())[0]
                currency_name = currency_data.get("name" , "N/A")
                currency_sympol = currency_data.get("symbol" , "N/A")
                currency = f"{currency_name} ({currency_sympol})" if currency_sympol else currency_name 
            else:
                currency = "N/A"
            
            info.append( { 
                  "name" : common ,
                  "capital" : capital , 
                  "region" : region , 
                  "subregion" : subregion ,
                  "population" : population , 
                  "flag"  : flag ,
                  "language" : language ,
                  "currency" : currency , 
                  
        })
        except Exception as e:
               print(f"ERROR : {item.get('name' , {}).get('commonname' , 'unknown')} - {e}")
    return info

def save_to_cvs(data , filename): #take the data and create a dataframe that saves in a csv file in the same folder
    df = pd.DataFrame(data)
    df.to_csv(filename,index = False)

save_to_cvs(get_all_country_info(), "countries.csv")    