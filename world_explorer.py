import requests
import pandas as pd
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from datetime import date , timedelta
import webbrowser


image_cache = []

def search_for_url(news_box, country_news):
    news_box.config(state="normal")

    # 1) Configure the hyperlink tag once
    news_box.tag_config(
        "hyperlink",
        foreground="blue",
        underline=True
    )
    news_box.tag_bind("hyperlink", "<Button-1>", open_url)
    news_box.tag_bind("hyperlink", "<Enter>",
                      lambda e: news_box.config(cursor="hand2"))
    news_box.tag_bind("hyperlink", "<Leave>",
                      lambda e: news_box.config(cursor=""))

    # 2) Clear and populate
    news_box.delete("1.0", "end")
    if not country_news or not isinstance(country_news, list):
        news_box.insert("end", "⚠️ No news data available.\n")
    else:
        for article in country_news:
            for line in article.strip().splitlines():
                if line.startswith("🔗"):
                    url = line.replace("🔗", "").strip()
                    # Insert URL with hyperlink tag
                    news_box.insert("end", url + "\n", "hyperlink")
                else:
                    news_box.insert("end", line + "\n")
            news_box.insert("end", "\n")

    news_box.config(state="disabled")

def open_url(event):
    text = event.widget
    # get the index of the click
    idx = text.index(f"@{event.x},{event.y}")

    # find the hyperlink tag at that index
    if "hyperlink" not in text.tag_names(idx):
        return

    # get the tag’s full range covering this point
    ranges = text.tag_prevrange("hyperlink", idx)
    if not ranges:
        ranges = text.tag_nextrange("hyperlink", idx)
    if not ranges:
        return

    start, end = ranges
    # extract the exact URL text
    url = text.get(start, end).strip()
    # ensure it really is a web URL
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url
    webbrowser.open(url)
    
def get_country_news(place , language):
    info = []
    today = date.today()
    week_ago = today - timedelta(days=7)
    today_str = today.isoformat()
    week_ago_str = week_ago.isoformat()
    base_news_url =f"https://newsapi.org/v2/everything?q={place}&from={week_ago_str}&to={today_str}&pageSize=5&language={language}&sortBy=popularity&apikey=8c64303a442543089d519e5d5bceb848"
    try:
        response = requests.get(base_news_url , timeout=10)
        r = response.json()     
    except (requests.exceptions.RequestException , ValueError) as e :
      return [f"NEWS API REQUESTS FAILED : \n{e}"]
    if r.get("status") != "ok" : 
            return [f"NEWS API ERROR: {r.get('message','unknown error')}"]   
    for indx , article  in enumerate(r.get("articles",[]) , start=1):
        author =article.get("author") or "N/A"
        summary = (
            
            f"{indx}. 📰 {article['title']}\n"
            f"✍️ Author: {author}\n"
            f"🏢 Source: {article['source']['name']}\n"
            f"📝 {article['description']}\n"
            f"🔗 {article['url']}\n\n"

        )
        info.append(summary)
    return info if info else ["NO ARTICLES YET"]

def get_current_weather(place):
    base_weather_url =f"http://api.weatherapi.com/v1/current.json?key=0e15f7bf18614926944122416250707&q={place}" 
    try:
      response = requests.get(base_weather_url)
      r = response.json()
    except (requests.exceptions.RequestException , ValueError) as e:
      return f"WEATHER API REQUEST FAILED :\n{e}"
    
    info = (
        f"🕒 Local Time: {r['location']['localtime']}\n"
        f"📅 Last Updated: {r['current']['last_updated']}\n"
        f"🌡 Temperature: {r['current']['temp_c']}°C\n"
        f"🥵 Feels Like: {r['current']['feelslike_c']}°C\n"
        f"🌥 Condition: {r['current']['condition']['text']}\n"
        f"💨 Wind Speed: {r['current']['wind_kph']} km/h"
    )  
      
      
    return info
    
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
        data = load_country_data()
    else:
        data = load_country_data()[load_country_data().apply(
            lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]

    for _, row in data.iterrows():
        tree.insert("", "end", values=(row["name"],))

def show_main_page():
    country_frame.pack_forget()
    main_frame.pack(fill="both" , expand=True)
        
def show_country_page(country_data):
    # hide main page, show country page
    main_frame.pack_forget()
    country_frame.pack(fill="both", expand=True)

    # clear out old widgets
    for w in country_frame.winfo_children():
        w.destroy()

    # back button
    back_btn = tk.Button(country_frame, text="← Back",
                         font=("Calibri", 12),
                         command=show_main_page)
    back_btn.pack(anchor="nw", pady=10, padx=10)

    # top-level container for info + content
    info_frame = tk.Frame(country_frame)
    info_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # left side (info + weather + news)
    left = tk.Frame(info_frame)
    left.pack(side="left", fill="both", expand=True)

    # right side (flag)
    right = tk.Frame(info_frame)
    right.pack(side="right", fill="y")

    # --- COUNTRY INFO ---
    country_info = (
        f"🌍 {country_data['name']}\n"
        f"🏛 Capital: {country_data['capital']}\n"
        f"🌐 Region: {country_data['region']} / {country_data['subregion']}\n"
        f"🗣 Language: {country_data['language']}\n"
        f"💰 Currency: {country_data['currency']}\n"
        f"👥 Population: {country_data['population']:,}"
    )
    info_lbl = ttk.Label(left, text=country_info,
                         font=("Calibri", 16),
                         justify="left")
    info_lbl.pack(fill="x", pady=(0, 15))

    # --- FLAG IMAGE ---
    img_url = country_data["flag"]
    resp = requests.get(img_url)
    img = Image.open(BytesIO(resp.content))
    img = img.resize((250, 300), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    image_cache.append(tk_img)

    flag_lbl = tk.Label(right, image=tk_img, bd=2, relief="solid")
    flag_lbl.pack(pady=(0, 20), padx=10)

    # --- WEATHER ---
    weather_title = ttk.Label(left, text="🌦 WEATHER",
                              font=("Calibri", 18),
                              justify="left")
    weather_title.pack(fill="x", pady=(0, 5))

    weather_text = get_current_weather(country_data["capital"])
    weather_lbl = ttk.Label(left, text=weather_text,
                            font=("Calibri", 12),
                            justify="left")
    weather_lbl.pack(fill="x", pady=(0, 20))

    # --- NEWS ---
    news_title = ttk.Label(left, text="🗞 TOP HEADLINES",
                           font=("Calibri", 18),
                           justify="left")
    news_title.pack(fill="x", pady=(0, 5))

    country_news = get_country_news(country_data["name"], country_data["code"])
    


    # frame to hold Text + Scrollbar
    news_frame = tk.Frame(left)
    news_frame.pack(fill="both", expand=True)

# Create the Text widget only once
    news_box = tk.Text(news_frame,
                   wrap="word",
                   font=("Calibri", 12),
                   bg="white",  
                   fg="black",
                   bd=1, relief="sunken")
    news_box.pack(side="left", fill="both", expand=True)
    news_box.insert("end", "🧪 News box loaded.\n")

# Add the scrollbar
    scrollbar = tk.Scrollbar(news_frame, command=news_box.yview)
    scrollbar.pack(side="right", fill="y")
    news_box.config(yscrollcommand=scrollbar.set)
    print("News box created:", news_box)

    # insert and tag URLs
    search_for_url(news_box, country_news)

def on_country_select():
    df = load_country_data()
    selected_item = tree.selection()
    if not selected_item:
        return
    country_name = tree.item(selected_item[0])["values"][0]
    country_data = df[df["name"] == country_name].iloc[0]
    show_country_page(country_data)



#gui

    
root = tk.Tk()
root.title("WORLD EXPLORER")
root.geometry("900x800")
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
search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(10,1200) ,  pady=(10,0))

search_label = tk.Label(search_frame, text="SEARCH : " , font = ("Calibri", 12))
search_label.grid(row=0, column=0, padx=(0, 10), sticky="w")

search_frame.columnconfigure(1, weight=1)

searchVar = tk.StringVar()
searchEntry = tk.Entry(search_frame , textvariable=searchVar , font =("Calibri" , 12) , width=40)
searchEntry.grid(row=0, column=1, sticky="ew")

searchVar.trace_add("write" , lambda*args: filter_tree(searchVar.get()))


if __name__ == "__main__":
    root.mainloop()