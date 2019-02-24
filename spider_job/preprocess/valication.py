import json
import pprint

std_url = ("https://search.51job.com/jobsearch/search_result.php?"
           "fromJs=1&"
           "keywordtype=2&"
           "lang=c&"
           "stype=2&"
           "postchannel=0000&"
           "fromType=1&"
           "confirmdate=9&"
           "jobarea=")

with open("./location.json", encoding="utf-8") as f:
    locations = json.load(f)

area_dict = dict()

for key, value in locations.items():
    if key[-4:] == "0000":
        area_dict.setdefault(value, dict())
        top_code = key
        top_area = value
    elif key[-2:] == "00":
        area_dict[top_area].setdefault(value, dict())
        second_code = key
        second_area = value
    else:
        # if key[:]
        area_dict[top_area][second_area].setdefault(value, "")

from copy import deepcopy

temp_dict = deepcopy(area_dict)

for key, value in temp_dict.items():
    if len(value) == 0:
        del area_dict[key]
    else:
        for x, y in temp_dict[key].items():
            if len(y) == 0:
                for a, b in locations.items():
                    if x == b:
                        area_dict[key][x] = std_url + a
                        break
            else:
                for a, b in y.items():
                    for m, n in locations.items():
                        if n == a:
                            area_dict[key][x][a] = std_url + m

with open("jobarea.json", "w", encoding="utf-8") as f:
    json.dump(area_dict, f, ensure_ascii=False)

major_cities = ["北京", "上海", "深圳", "天津", "重庆"]

start_urls = dict()

for key, value in area_dict.items():
    if key in major_cities:
        start_urls.setdefault(key, list())
        for x, y in value.items():
            start_urls[key].append(y)
        start_urls[key].append(std_url + start_urls[key][-1][-6:-4] + "0000")
    else:
        for x, y in value.items():
            if not isinstance(y, dict):
                start_urls.setdefault(x, y)
            else:
                start_urls.setdefault(x, list())
                for m, n in y.items():
                    start_urls[x].append(n)
                start_urls[x].append(std_url + start_urls[x][-1][-6:-2] + "00")

with open("start_urls_by_city.json", "w", encoding="utf-8") as f:
    json.dump(start_urls, f, ensure_ascii=False)

start_urls = dict()

for key, value in area_dict.items():
    start_urls.setdefault(key, list())
    for x, y in value.items():
        if not isinstance(y, dict):
            start_urls[key].append(y)
        else:
            for m, n in y.items():
                start_urls[key].append(n)

    start_urls[key].append(std_url + start_urls[key][-1][-6:-4] + "0000")

with open("start_urls_by_province.json", "w", encoding="utf-8") as f:
    json.dump(start_urls, f, ensure_ascii=False)
