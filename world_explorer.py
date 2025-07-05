import requests
import pandas as pd
from tkinter import ttk
import tkinter as tk


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
    df.to_csv(filename,index = False , quoting=1)

country_info = pd.read_csv("country.csv")



root = tk.Tk()
root.title("WORLD EXPLORER")
root.geometry("750x700")
root.configure(bg="#CCCCCC")

main_frame = tk.Frame(root , bd = 5  , relief="sunken")
main_frame.pack(pady=10 , padx=10 , fill="both" , expand=True)

main_label = tk.Label(root, text = "🌍WORLD EXPLORER🌍" , foreground="#00296A" , background = "#CCCCCC" , font=( "bold" ,20 ))
main_label.pack(pady=10 , padx=20)


style = ttk.Style()
style.configure("Treeview.Heading", font=("Franklin Gothic Medium", 14))
style.configure("Treeview", font=("Calibri", 12))


tree = ttk.Treeview(main_frame , columns=("name") , show="headings" , style="Treeview")

scroll_bar = tk.Scrollbar(main_frame,orient="vertical" , command=tree.yview)
tree.configure(yscrollcommand=scroll_bar.set)

tree.grid(row= 0 , column=0 , sticky="nsew") #scroll bar mechanism
scroll_bar.grid(row=0, column=1, sticky="ns")
main_frame.grid_rowconfigure(0, weight=3)
main_frame.grid_columnconfigure(0, weight=3)

tree.heading("name" , text="NAME")          # tree adjusting 
tree.column("name" , anchor="w")

for _, row in country_info.iterrows(): 
    tree.insert("" , "end" ,values=(row["name"],))

def search_bar():
    search_bar = ttk.Frame(main_frame , )


root.mainloop()