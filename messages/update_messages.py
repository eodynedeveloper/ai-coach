import json 
import pandas as pd
import os

def main():
    msgs = pd.read_csv('../messages.csv')

    languages = list(set([i[3:] for i in msgs.columns[2:]]))

    for language in languages:
        print(f"updating {language} messages...")
        msgs_dict = {}
        columns = ["Use Case", f"v1_{language}", f"v2_{language}", f"v3_{language}"]
        msgs_lang = msgs[columns]

        for i, u in enumerate(msgs_lang["Use Case"]):
            row = msgs_lang[msgs_lang['Use Case'] == u]
            msgs_dict[u] = {}
            for v in  [f'v1_{language}', f'v2_{language}', f'v3_{language}']:
                for msg in msgs_lang[v][i].split("\n"):
                    if v[:2] not in msgs_dict[u]:
                        msgs_dict[u][v[:2]] = []
                    if len(msg.split("\"")) < 3:
                        continue
                    msgs_dict[u][v[:2]].append(msg.split("\"")[1])

        with open(f"msgs_{language}.json", "w") as fp:
            json.dump(msgs_dict , fp, ensure_ascii=True) 

if __name__ == "__main__":

    # set current dir to messages for paths to work properly
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    main()