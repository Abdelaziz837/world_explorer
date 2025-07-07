import requests

def get_current_weather(place):
    weather_info =[]
    base_weather_url =f"http://api.weatherapi.com/v1/current.json?key=0e15f7bf18614926944122416250707&q={place}" 
    try:
      response = requests.get(base_weather_url)
      r = response.json()
    except (requests.exceptions.RequestException , ValueError) as e:
      print("WEATHER API REQUEST FAILED : " , e)
      return None
    
    r = response.json()
    info = {
             "localtime" : r["location"]['localtime'] ,
             "lastupdated" : r['current']['last_updated'] ,
             "tempreature" : r['current']['temp_c'] ,
             "condition" : r["current"]['condition']['text'] , 
             "wind speed" : r["current"]['wind_kph'] , 
             "feels like" : r["current"]['feelslike_c'] 
    }     
    weather_info.append(info)
    
    return weather_info


print(get_current_weather("paris"))