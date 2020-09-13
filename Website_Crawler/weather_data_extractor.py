import sys, os, subprocess, requests, re
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm


def get_lang_and_mode(mode):
    with open("lang.txt","r") as lang_file:
        list_ = lang_file.readlines()
        language = list_[0]
        if mode == "":
            if len(list_) == 2:
                mode = list_[1]
            else:
                mode = "terminal"
        lang_list = list(language)
        if lang_list[-1] == "\n":
            lang_list.pop()
        language = "".join(lang_list)
        if len(list_) >= 2:
            mode = list_[1]
            with open("lang.txt","w") as lang_file:
                lang_file.write(language)
    return language, mode


def main():
    mode = ""
    language, mode = get_lang_and_mode(mode)
    # print(f"{language}, {mode}")
    loop = True
    while loop == True:
        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
        if language == "English":
            region = input("Insert the region --> ")
        else:
            region = input("Inserisci la regione --> ")
        if region.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        if region:
            region = region.replace(" ", "+")
            URL += f"+{region}" 
        data = weather_data_extractor(URL, region, language)
        display_data(data)
        if loop == True:
            while True:
                if language == "English":
                    exit_choice = input("Do you want to exit the program? [Y/n]: ")
                else:
                    exit_choice = input("Vuoi uscire dal programma? [Y/n]: ")
                exit_choice = exit_choice.lower()
                if exit_choice == "y" or exit_choice == "yes":
                    if language == "English":
                        print("Goodbye!\n")
                    else:
                        print("Arrivederci!\n")
                    loop = False
                    break
                elif exit_choice != "n" or exit_choice != "no":
                    if language == "English":
                        print("Returning to the menu!\n")
                    else:
                        print("Ritorno al menù!\n")
                    if mode == "menu":
                        with open("lang.txt", "a") as lang_file:
                            lang_file.write("\nmenu")
                        subprocess.Popen("Website_Crawler\\weather_data_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def weather_data_extractor(url, region, language):
    session = requests.Session()
    session.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    session.headers['Accept-Language'] = "en-US,en;q=0.5"
    session.headers['Content-Language'] = "en-US,en;q=0.5"
    soup = bs(session.get(url).text, "html.parser")
    result = {}
    result["region"] = soup.find("div", attrs={"id": "wob_loc"}).text
    result["temp_now"] = soup.find("span", attrs={"id": "wob_tm"}).text
    result["dayhour"] = soup.find("div", attrs={"id": "wob_dts"}).text
    result["weather_now"] = soup.find("span", attrs={"id": "wob_dc"}).text
    result["precipitation"] = soup.find("span", attrs={"id": "wob_pp"}).text
    result["humidity"] = soup.find("span", attrs={"id": "wob_hm"}).text
    result["wind"] = soup.find("span", attrs={"id": "wob_ws"}).text
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        day_name = day.find("div", attrs={"class": "QrNVmd"}).attrs["aria-label"]
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class", "wob_t"})
        max_temp = temp[0].text
        min_temp = temp[2].text
        if language == "English":
            if day_name == "lunedì":
                day_name = "monday"
            elif day_name == "martedì":
                day_name = "tuesday"
            elif day_name == "mercoledì":
                day_name = "wednesday"
            elif day_name == "giovedì":
                day_name = "thursday"
            elif day_name == "venerdì":
                day_name = "friday"
            elif day_name == "sabato":
                day_name = "saturday"
            elif day_name == "domenica":
                day_name = "sunday"
        elif language == "Italiano":
            if day_name == "monday":
                day_name = "lunedì"
            elif day_name == "tuesday":
                day_name = "martedì"
            elif day_name == "wednesday":
                day_name = "mercoledì"
            elif day_name == "thursday":
                day_name = "giovedì"
            elif day_name == "friday":
                day_name = "venerdì"
            elif day_name == "saturday":
                day_name = "sabato"
            elif day_name == "sunday":
                day_name = "domenica"
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    result["next_days"] = next_days
    print(next_days)
    return result


def display_data(data):
    print("Weather for:", data["region"])
    print("Now:", data["dayhour"])
    print(f"Temperature now: {data['temp_now']}°C")
    print("Description:", data['weather_now'])
    print("Precipitation:", data["precipitation"])
    print("Humidity:", data["humidity"])
    print("Wind:", data["wind"])
    print("Next days:")
    for dayweather in data["next_days"]:
        print(dayweather)
        print("="*40, dayweather["name"], "="*40)
        print("Description:", dayweather["weather"])
        print(f"Max temperature: {dayweather['max_temp']}°C")
        print(f"Min temperature: {dayweather['min_temp']}°C")

if __name__ == "__main__":
    main()
