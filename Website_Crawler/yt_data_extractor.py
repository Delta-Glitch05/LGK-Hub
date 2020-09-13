import os, sys, subprocess
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


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
        if language == "English":
            url = input("Insert the URL of the video --> ")
        else:
            url = input("Inserisci l'URL del video --> ")
        if url.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        data = yt_data_extractor(url, language)
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
                        subprocess.Popen("Website_Crawler\\yt_data_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def yt_data_extractor(url, language):
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    soup = bs(response.html.html, "html.parser")
    result = {}
    classe = "title style-scope ytd-video-primary-info-renderer"
    result["title"] = soup.find("h1").text.strip()
    digits = "1234567890,."
    # result["views"] = int(''.join([i for i in soup.find("span", attrs={"class": "view-count"}).text if i.isdigit()]))
    result["views"] = ''.join([i for i in soup.find("span", attrs={"class": "view-count"}).text if i in digits])
    # result["published"] = soup.find().text.strip()
    result["publication_date"] = soup.find("div", {"id": "date"}).text[1:]
    
    en_months = ["jan", "feb", "mar", "apr", "may", "june", "july", "aug", "sept", "oct", "nov", "dec"]
    it_months = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]

    if language == "English":
        for month in it_months:
            if month in result["publication_date"]:
                i = it_months.index(month)
                lista = result["publication_date"].split(" ")
                lista[1] = en_months[i]
                result["publication_date"] = ' '.join(lista)
    if language == "Italiano":
        for month in en_months:
            if month in result["publication_date"]:
                i = it_months.index(month)
                lista = result["publication_date"].split(" ")
                lista[1] = en_months[i]
                result["publication_date"] = ' '.join(lista)

    result["video_duration"] = soup.find("span", attrs={"class": "ytp-time-duration"}).text
    #result["video_tags"] = soup.find("a", attrs={"class": "yt-simple-endpoint style-scope yt-formatted-string"}).text
    result["video_tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
    text_yt_formatted_strings = soup.find_all("yt-formatted-string", {"id": "text", "class": "ytd-toggle-button-renderer"})
    result["likes"] = text_yt_formatted_strings[0].text
    result["dislikes"] = text_yt_formatted_strings[1].text
    result["description"] = soup.find("yt-formatted-string", attrs={"class": "content"}).text
    channel_tag = soup.find("yt-formatted-string", attrs={"class": "ytd-channel-name"}).find("a")
    channel_name = channel_tag.text
    channel_url = f"https://youtube.com/user/{channel_tag['href']}"
    channel_subscribers = soup.find("yt-formatted-string", attrs={"id": "owner-sub-count"}).text.strip()
    sub_num = ''.join([i for i in channel_subscribers if i in digits])
    if "Mln" in channel_subscribers:
        sub_num += " Mln"
    elif "Mld" in channel_subscribers:
        sub_num += " Mld"
    channel_subscribers = sub_num
    result["channel"] = {"name": channel_name, "url": channel_url, "subscribers": channel_subscribers}
    display_data(result, language)


def display_data(result, language):
    if language == "English":    
        print(f"Title: {result['title']}")
        print(f"Views: {result['views']}")
        print(f"Publication date: {result['publication_date']}")
        print(f"Video duration: {result['video_duration']}")
        print(f"Video tags: {result['video_tags']}")
        print(f"Likes: {result['likes']}")
        print(f"Dislikes: {result['dislikes']}")
        print(f"\nDescription: {result['description']}\n")
        print(f"\nChannel name: {result['channel']['name']}")
        print(f"Channel URL: {result['channel']['url']}")
        print(f"Channel subscribers: {result['channel']['subscribers']}")
    else:   
        print(f"Titolo: {result['title']}")
        print(f"Visualizzazioni: {result['views']}")
        print(f"Data di pubblicazione: {result['publication_date']}")
        print(f"Durata del video: {result['video_duration']}")
        print(f"Tag del video: {result['video_tags']}")
        print(f"Mi piace: {result['likes']}")
        print(f"Non mi piace: {result['dislikes']}")
        print(f"\nDescrizione: {result['description']}\n")
        print(f"\nNome del canale: {result['channel']['name']}")
        print(f"URL del canale: {result['channel']['url']}")
        print(f"Iscritti del canale: {result['channel']['subscribers']}")


if __name__ == "__main__":
    main()
