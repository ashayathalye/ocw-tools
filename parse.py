import json
import requests

open_learning_rooms = {
    "2-131",
    "2-142",
    "2-190",
    "6-120",
    "34-101",
    "35-225",
    "E25-111",
    "E25-117"
}

is_and_t_rooms = {
    "1-135",
    "1-150",
    "1-190",
    "2-105",
    "3-270",
    "3-333",
    "4-145",
    "4-149",
    "4-153",
    "4-159",
    "4-163",
    "4-231",
    "4-237",
    "4-261",
    "4-265",
    "4-270",
    "4-370",
    "5-134",
    "9-354",
    "24-115",
    "24-121",
    "26-100",
    "32-124",
    "32-141",
    "32-144",
    "32-155",
    "37-212",
    "56-114",
    "56-154",
    "66-144",
    "66-168"
}


term = '2022SP'

url = f'http://coursews.mit.edu/coursews/?term={term}'

raw_text = requests.get(url).text
# hilariously, the json is invalid thanks to one class
fixed_text = raw_text.replace('"Making"', '&quot;Making&quot;')
raw_classes = json.loads(fixed_text)['items']

def parse_name(name):
    if name[0] == "null":
        return "null"
    else:
        first = name[1]
        last = name[0][:-1]
        return first + " " + last

def course_to_int(course_number_string):
    prefix = course_number_string.split(".")[0]
    try:
        num = int(prefix)
        return num
    except ValueError:
        return 25 # rank last, highest integer course number is 24

def parse_interval(interval):
    if "-" not in interval:
        if "." in interval:
            start_hour = int(interval.replace(".", ":").split(":")[0])
            end_hour = int(start_hour) + 1
            return str(start_hour) + ":30" + "-" + str(end_hour) + ":30"
        else:
            start_hour = int(interval)
            end = start_hour + 1
            return str(start_hour) + "-" + str(end)
    else:
        return interval.replace(".", ":")

def parse_time(time):
    if "EVE" in time:
        days = time[0]
        interval = time[2][1:]
        return days + interval + "PM"
    else:
        return time[0]

def main():
    by_class = {}

    for c in raw_classes:
        t = c["type"]
        if t == "LectureSession":
            course_number = c["section-of"]
            room = c["timeAndPlace"].split(" ")[-1]
            time = c["timeAndPlace"].split(" ")[:-1]
            time = parse_time(time)

            if course_number not in by_class and room in open_learning_rooms:
                by_class[course_number] = {
                    "room": room,
                    "time": time,
                    "setup": "OPEN_LEARNING"
                }
            if course_number not in by_class and room in is_and_t_rooms:
                by_class[course_number] = {
                    "room": room,
                    "time": time,
                    "setup": "IS&T"
                }

    for c in raw_classes:
        t = c["type"]
        if t == "Class":
            course_number = c["id"]
            if course_number in by_class:
                in_charge = c["in-charge"].split(" ")
                name = parse_name(in_charge)
                by_class[course_number]["in-charge"] = name

    open_learning = []
    is_and_t = []
    for k, v in by_class.items():
        if v["setup"] == "OPEN_LEARNING":
            open_learning.append((k, v["room"], v["time"], v["in-charge"]))
        elif v["setup"] == "IS&T":
            is_and_t.append((k, v["room"], v["time"], v["in-charge"]))

    open_learning.sort(key=lambda x: course_to_int(x[0]))
    is_and_t.sort(key=lambda x: course_to_int(x[0]))

    print("Classes in Open Learning's auto-capture rooms:")
    for c in open_learning:
        num, loc, time, prof = c
        print(f"{num : <10}{loc : <10}{time : <15}{prof : <30}")
    print()
    print("Classes in IS&T's auto-capture rooms:")
    for c in is_and_t:
        num, loc, time, prof = c
        print(f"{num : <10}{loc : <10}{time : <15}{prof : <30}")

if __name__ == "__main__":
    main()
