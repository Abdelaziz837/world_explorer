import requests
import pandas as pd
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

image_cache = []


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

def load_country_data():
    try:
        country_info = pd.read_csv("country.csv")
    except FileNotFoundError:
        save_to_cvs(get_all_country_info() , "country.csv")
        country_info = pd.read_csv("country.csv")
    return country_info       

def filter_tree(query):
    query = query.strip().lower()
    tree.delete(*tree.get_children())

    if not query:
        data = country_info
    else:
        data = country_info[country_info.apply(
            lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]

    for _, row in data.iterrows():
        tree.insert("", "end", values=(row["name"],))

def show_main_page():
    country_frame.pack_forget()
    main_frame.pack(fill="both" , expand=True)
    
def show_country_page(country_data):
    
    main_frame.pack_forget()
    country_frame.pack(fill="both" , expand=True)

    for widget in country_frame.winfo_children():
        widget.destroy()
    back_btn = tk.Button(country_frame, text="← Back", font=("Calibri", 12), command=show_main_page)
    back_btn.pack(anchor="nw" , pady=10 , padx = 10)

    info = (
        f"🌍 {country_data['name']}\n"
        f"🏛 Capital: {country_data['capital']}\n"
        f"🌐 Region: {country_data['region']} / {country_data['subregion']}\n"
        f"🗣 Language: {country_data['language']}\n"
        f"💰 Currency: {country_data['currency']}\n"
        f"👥 Population: {country_data['population']:,}"
    )
    info_frame = tk.Frame(country_frame)
    info_frame.pack(fill="both", expand=True, padx=20, pady=20)

    label = ttk.Label(info_frame, text=info , font=("Calibri", 25), justify="left" , anchor="n")
    label.pack(side="left", anchor="n" , padx=(0 , 20))

    img_url = country_data["flag"]  # This is the direct PNG URL
    response = requests.get(img_url)
    img_data = response.content
 
    image = Image.open(BytesIO(img_data))
    image = image.resize((450,350) , Image.Resampling.LANCZOS)
    
    tk_image = ImageTk.PhotoImage(image)
      
    flag_label = tk.Label(info_frame, image=tk_image)
    image_cache.append(tk_image)
  
    flag_label.pack(side="left" , padx=(500,20) , anchor="n")


def on_country_select():
    df = load_country_data()
    selected_item = tree.selection()
    if not selected_item:
        return
    country_name = tree.item(selected_item[0])["values"][0]
    country_data = df[df["name"] == country_name].iloc[0]
    show_country_page(country_data)
    
root = tk.Tk()
root.title("WORLD EXPLORER")
root.geometry("750x700")
root.configure(bg="#CCCCCC")

main_frame = tk.Frame(root , bd = 5  , relief="sunken")
main_frame.pack(pady=10 , padx=10 , fill="both" , expand=True)
country_frame = tk.Frame(root , bd=5 , relief="sunken" )


main_label = tk.Label(root, text = "🌍WORLD EXPLORER🌍" , foreground="#00296A" , background = "#CCCCCC" , font=( "bold" ,20 ))
main_label.pack(pady=10 , padx=20)


style = ttk.Style()
style.configure("Treeview.Heading", font=("Franklin Gothic Medium", 14))
style.configure("Treeview", font=("Calibri", 12) , rowheight = 28)



tree = ttk.Treeview(main_frame , columns=("name",) , show="headings" , style="Treeview")
tree.bind("<<TreeviewSelect>>" , lambda event : on_country_select() )


scroll_bar = tk.Scrollbar(main_frame,orient="vertical" , command=tree.yview)
tree.configure(yscrollcommand=scroll_bar.set)

tree.grid(row= 0 , column=0 , sticky="nsew") #scroll bar mechanism
scroll_bar.grid(row=0, column=1, sticky="ns")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

tree.heading("name" , text="NAME")          # tree adjusting 
tree.column("name" , anchor="w")

for _, row in load_country_data().iterrows(): 
    tree.insert("" , "end" ,values=(row["name"],))

search_frame = ttk.Frame(main_frame )
search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10 ,  pady=(10,0))

search_label = tk.Label(search_frame, text="SEARCH : " , font = ("Calibri", 12))
search_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

search_frame.columnconfigure(1, weight=1)

searchVar = tk.StringVar()
searchEntry = tk.Entry(search_frame , textvariable=searchVar , font =("Calibri" , 12) , width=40)
searchEntry.grid(row=0, column=1, sticky="ew")

searchVar.trace_add("write" , lambda*args: filter_tree(searchVar.get()))


root.mainloop()