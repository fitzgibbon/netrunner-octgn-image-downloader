import argparse
import pathlib
import os
import xml.etree.ElementTree as et
import urllib.request

def name_convert(card_name):
    tmp = card_name
    tmp = tmp.replace(" ", "-")
    tmp = tmp.replace(".", "-")
    tmp = tmp.replace("*", "")
    tmp = tmp.replace("!", "")
    tmp = tmp.replace(":", "")
    tmp = tmp.replace("@", "")
    tmp = tmp.replace("'", "")
    tmp = tmp.replace("\"", "")
    tmp = tmp.replace("&", "and")
    tmp = tmp.replace("---", "-")
    tmp = tmp.replace("--", "-")
    tmp = tmp.replace("randd", "r-d")
    tmp = tmp.replace("joshua-b-", "joshua-b")
    tmp = tmp.replace("alix-t4lb07", "alix-t4lbo7")
    return tmp.lower()

def get_pic_url_map(set_path):
    print(set_path)
    set_xml = et.parse(set_path + "/set.xml")
    root = set_xml.getroot()
    set_name = root.attrib["name"]
    print(set_name)
    if set_name == "Markers" or set_name == "Promos":
        next
    for cards in root.iter("cards"):
        for card in cards.iter("card"):
            subtitle = None
            for prop in card.iter("property"):
                if prop.attrib["name"] == "Subtitle":
                    subtitle = prop.attrib["value"]
            print("{} ({}): {}".format(card.attrib["name"], subtitle, card.attrib["id"]))
            target_dir = set_path + "/Cards"
            target_filename = target_dir + "/" + card.attrib["id"] + ".png"
            url_base = "http://imgnetrunner.meteor.com/cards/"
            url_set_name = name_convert(set_name)
            url_card_name = name_convert(card.attrib["name"])
            non_sub_sets = set(["core", "humanitys-shadow", "what-lies-ahead", "cyber-exodus"])
            if subtitle and name_convert(set_name) not in non_sub_sets:
                url_card_name += "-" + name_convert(subtitle)
            url_full = url_base + url_card_name + "-" + url_set_name + ".png"
            print(url_full)
            with urllib.request.urlopen(url_full) as u:
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                with open(target_filename, "wb") as f:
                    f.write(u.read())

def main():
    "Download and install card images for the OCTGN Netrunner plugin."
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("gamepath",
        type=str,
        help="OCTGN Netrunner game folder.")
    args = parser.parse_args()
    game_path = pathlib.Path(args.gamepath)
    set_paths = game_path.glob("Sets/*")
    #print(list(set_paths))
    pic_maps = [get_pic_url_map(str(x)) for x in list(set_paths)]

if __name__ == "__main__":
    main()
