import sys, subprocess, requests, json, time
from pprint import pprint


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
            url = input("Insert the URL of the YouTube video --> ")
        else:
            url = input("Inserisci l'URL del video di YouTube --> ")
        if url.lower() == "exit":
            if language == "English":
                print("Goodbye!\n")
            else:
                print("Arrivederci!\n")
            loop = False
            break
        ytc_extractor(url, language)
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
                        subprocess.Popen("Website_Crawler\\ytc_extractor.bat", shell=True)
                        sys.exit()
                    else:
                        break


def ytc_extractor(url, language):
    for count, comment in enumerate(get_comments(url)):
        if count == 3:
            break
        pprint(comment)
        print("="*50)


def search_dict(partial, key):
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        for i in partial:
            for o in search_dict(i, key):
                yield o


def find_value(html, key, num_sep_chars=2, separator='"'):
    start_pos = html.find(key) + len(key) + num_sep_chars
    end_pos = html.find(separator, start_pos)
    return html[start_pos:end_pos]


def get_comments(url):
    session = requests.Session()
    res = session.get(url)
    xsrf_token = find_value(res.text, "XSRF_TOKEN", num_sep_chars=3)
    data_str = find_value(res.text, 'window["ytInitialData"] = ', num_sep_chars=0, separator="\n").rstrip(";")
    data = json.loads(data_str)
    for r in search_dict(data, "itemSectionRenderer"):
        pagination_data = next(search_dict(r, "nextContinuationData"))
        if pagination_data:
            break
    continuation_tokens = [(pagination_data['continuation'], pagination_data['clickTrackingParams'])]
    while continuation_tokens:
        continuation, itct = continuation_tokens.pop()
        params = {
            "action_get_comments": 1,
            "pbj": 1,
            "ctoken": continuation,
            "continuation": continuation,
            "itct": itct,
        }
        data = {
            "session_token": xsrf_token,
        }
        headers = {
            "x-youtube-client-name": "1",
            "x-youtube-client-version": "2.20200731.02.01"
        }
        response = session.post("https://www.youtube.com/comment_service_ajax", params=params, data=data, headers=headers)
        comments_data = json.loads(response.text)
        for comment in search_dict(comments_data, "commentRenderer"):
            yield{
                "commentId": comment["commentId"],
                "text": ''.join([c['text'] for c in comment['contentText']['runs']]),
                "time": comment['publishedTimeText']['runs'][0]['text'],
                "isLiked": comment["isLiked"],
                "likeCount": comment["likeCount"],
                # "replyCount": comment["replyCount"],
                'author': comment.get('authorText', {}).get('simpleText', ''),
                'channel': comment['authorEndpoint']['browseEndpoint']['browseId'],
                'votes': comment.get('voteCount', {}).get('simpleText', '0'),
                'photo': comment['authorThumbnail']['thumbnails'][-1]['url'],
                "authorIsChannelOwner": comment["authorIsChannelOwner"],
            }
        continuation_tokens = [(next_cdata['continuation'], next_cdata['clickTrackingParams'])
                        for next_cdata in search_dict(comments_data, "nextContinuationData")] + continuation_tokens
        time.sleep(0.1)


if __name__ == "__main__":
    main()
