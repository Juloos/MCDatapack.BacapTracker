import json
import zipfile
import glob
from math import floor, ceil
import sys
import os


def get_progress_update_function(nb_tasks):
    current_task = -1
    def progress_update_function():
        nonlocal current_task
        current_task += 1
        if current_task == nb_tasks:
            print("\r ", nb_tasks, '/', nb_tasks)
        elif current_task < nb_tasks:
            print("\r ", current_task, '/', nb_tasks, end='')
        else:
            print("\nToo many tasks.")
    return progress_update_function


def get_blank_function():
    current_blank = -1
    def blank_function():
        nonlocal current_blank
        current_blank += 1
        return f"\u00A7{current_blank}"  # '\u00A7' == '§'
    return blank_function


def find_best_count(key_count, slot_count, page_count):
    couple = (0, page_count)
    for p in range(1, page_count + 1):
        for s in range(1, slot_count + 1):
            if s * p == key_count and abs(s - p) < abs(couple[0] - couple[1]):
                couple = (s, p)
    if couple == (0, page_count):
        couple = (None, ceil(key_count / slot_count))
    return couple


# All the up-to-now known categories that are in BACAP (+ "total")
KEY2NAME = {
    "total": "Total",
    "adventure": "Adventure",
    "animal": "Animal",
    "bacap": "BlazeandCave",
    "beginning": "Beginning",
    "biomes": "Biomes",
    "building": "Building",
    "challenges": "Challenges",
    "combat": "Combat",
    "enchanting": "Enchanting",
    "end": "End",
    "farming": "Farming",
    "mining": "Mining",
    "monsters": "Monsters",
    "nether": "Nether",
    "potion": "Potion",
    "redstone": "Redstone",
    "statistics": "Statistics",
    "weaponry": "Weaponry"
}

PACK_FORMAT = 4  # pack format compatibility with BACAP & MC starts at the 1.13.2 release
FUNCTIONS_PATH = "data/bac_tracker/functions"
BACAP_PATH = (input("Enter the path to a BACAP folder or zip\n> ") if len(sys.argv) < 2 else sys.argv[1]).replace('\\', '/').removesuffix('/')
BACAP_ZIP = None
if BACAP_PATH.endswith(".zip"):
    BACAP_ZIP = zipfile.ZipFile(BACAP_PATH, "r")
try:
    if BACAP_ZIP is not None:
        aafile = zipfile.Path(BACAP_ZIP, at="data/bc_rewards/functions/update_score.mcfunction").open(encoding="utf-8")
        with BACAP_ZIP.open("pack.mcmeta", "r") as packmeta:
            PACK_FORMAT = json.load(packmeta)["pack"]["pack_format"]
    else:
        aafile = open(f"{BACAP_PATH}/data/bc_rewards/functions/update_score.mcfunction", "r")
        with open(f"{BACAP_PATH}/pack.mcmeta", "r") as packmeta:
            PACK_FORMAT = json.load(packmeta)["pack"]["pack_format"]
except FileNotFoundError:
    print("File not found. Please check your path.")
    input("Press Enter to exit.\n")
    exit(1)
NB_BAR = int((input("Number of bars in the scoreboard title (default is 40)\n> ") or 40) if len(sys.argv) < 3 else sys.argv[2])

print(f"\nExctracting data from BACAP (pack format {PACK_FORMAT})...")
AA = list()
for line in aafile.readlines():
    line2 = line.removeprefix("execute as @a[advancements={")  # Terralith version is ignored
    if line != line2:
        index = line2.find("=true}]")
        if index != -1:
            AA.append(line2[:index])
aafile.close()

DATA = dict()
NB_ADV = len(AA)
UPDATE_PROGRESS = get_progress_update_function(NB_ADV)
UPDATE_PROGRESS()
for advancement in AA:
    current = advancement
    while not current.startswith("blazeandcave:"):
        if BACAP_ZIP is not None:
            jsonLike = zipfile.Path(BACAP_ZIP, at=f"data/{current.replace(':', '/advancements/')}.json").open(encoding="utf-8")
        else:
            jsonLike = open(f"{BACAP_PATH}/data/{current.replace(':', '/advancements/')}.json", 'r')
        jsonData = json.load(jsonLike)
        if 'parent' in jsonData:
            current = jsonData["parent"]
        else:
            break
        jsonLike.close()
    if current.startswith("blazeandcave:"):
        category = current.removeprefix("blazeandcave:").split('/', 1)[0]
    else:
        category = jsonData['rewards']['function'].removeprefix("bc_rewards:").split('/', 1)[0]
    if category not in DATA:
        DATA[category] = list()
    DATA[category].append(advancement)
    UPDATE_PROGRESS()

if BACAP_ZIP is not None:
    BACAP_ZIP.close()

DATA_SUM = {key: len(value) for key, value in DATA.items()}
DATA_SUM['total'] = sum(DATA_SUM.values())
PINNED_KEYS = ("total", "bacap")
OTHER_KEYS = sorted(set(DATA_SUM.keys()).difference(PINNED_KEYS))
PINNED_KEYS = sorted(set(PINNED_KEYS).intersection(DATA_SUM.keys()), key=lambda k: PINNED_KEYS.index(k))
SLOT_COUNT = 15 - (3 + 1 + len(PINNED_KEYS))
KEY_COUNT, PAGE_COUNT = find_best_count(len(OTHER_KEYS), SLOT_COUNT, 5)  # 5 is the max number of pages
KEY_COUNT = KEY_COUNT or 5


print("\nGenerating datapack...")
UPDATE_PROGRESS = get_progress_update_function(1 + NB_ADV + 1 + len(OTHER_KEYS) + 1 + 2 * (len(DATA_SUM) + 1))
UPDATE_PROGRESS()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("pack.mcmeta", "r") as packmeta:
    packjson = json.load(packmeta)
packjson["pack"]["pack_format"] = PACK_FORMAT
with open("pack.mcmeta", "w") as packmeta:
    json.dump(packjson, packmeta, indent=2)
UPDATE_PROGRESS()


PROGRESSF_C = 'execute if score @p bac_tracker.total matches %s run scoreboard objectives modify bac_tracker.progress_score displayname [" "," "," ","[",{"text":"%s","color":"green"},{"text":"%s","color":"gray"},"]",{"text":" - ","color":"gray"},{"text":"%s%%","color":"light_purple"}," "," "," "]\n'
with open(f"{FUNCTIONS_PATH}/display/progress_bar.mcfunction", "w") as progressf:
    for i in range(NB_ADV + 1):
        nb_greens = floor(i * NB_BAR / NB_ADV)
        nb_grays = NB_BAR - nb_greens
        progressf.write(
            PROGRESSF_C % (
                str(i) + (".." * (i == NB_ADV)), 
                '|' * nb_greens, 
                '|' * nb_grays, 
                str(round(i / NB_ADV * 100, 1) if i != NB_ADV else 100)
                )
            )
        UPDATE_PROGRESS()

PAGESF_C1 = 'team modify bac_tracker.page prefix [%s,{"text":"Page %d of %d","color":"gray","italic":true}]\n\n'
PAGESF_C2 = 'scoreboard players set %s bac_tracker.progress_score %d\n'
other_keys = OTHER_KEYS.copy()
for page in range(1, PAGE_COUNT + 1):
    blank = get_blank_function()
    sidebar = list()
    sidebar.append(blank())
    sidebar += [KEY2NAME[key] for key in PINNED_KEYS]
    sidebar.append(blank())
    for i in range(1, KEY_COUNT + 1):  # if None is given, place 5 keys per page by defaut
        if other_keys:
            sidebar.append(KEY2NAME[other_keys.pop(0)])
            UPDATE_PROGRESS()
        else:
            break
    sidebar.append(blank())
    sidebar.append("\u00A7p")
    sidebar.reverse()
    with open(f"{FUNCTIONS_PATH}/display/page_{page}.mcfunction", "w", encoding="utf-8") as pagef:
        pagef.write(PAGESF_C1 % (','.join(['" "'] * (ceil(NB_BAR / 2) - 2)), page, PAGE_COUNT))
        for i in range(len(sidebar) - 1, -1, -1):
            pagef.write(PAGESF_C2 % (sidebar[i], i))

SETUPF_C = 'scoreboard players set page_count'
with open(f"{FUNCTIONS_PATH}/load/setup.mcfunction", "r", encoding="utf-8") as setupf:
    setup = setupf.readlines()
with open(f"{FUNCTIONS_PATH}/load/setup.mcfunction", "w", encoding="utf-8") as setupf:
    setupf.write(''.join((f"{SETUPF_C} bac_tracker.vars {PAGE_COUNT}\n" if line.startswith(SETUPF_C) else line) for line in setup))
UPDATE_PROGRESS()


ALLF_C1 = 'function bac_tracker:display/refresh_scores/%s\n'
KEYF_C1 = 'execute if score @p bac_tracker.%s matches %s run team modify bac_tracker.%s suffix [{"text":": ","color":"gray"},{"text":"%s","color":"yellow"},{"text":"/","color":"gold"},{"text":"%s","color":"yellow"}]\n'
KEYF_C2 = '\nexecute if score @p bac_tracker.%s matches %s.. run team modify bac_tracker.%s color green\n'
KEYF_C3 = 'execute unless score @p bac_tracker.%s matches %s.. run team modify bac_tracker.%s color white\n'
with open(f"{FUNCTIONS_PATH}/display/refresh_scores/all.mcfunction", "w") as allf:
    for key, value in DATA_SUM.items():
        if key != 'total':
            allf.write(ALLF_C1 % key)
        with open(f"{FUNCTIONS_PATH}/display/refresh_scores/{key}.mcfunction", "w") as keyf:
            for i in range(value + 1):
                keyf.write(KEYF_C1 % (key, str(i) + (".." * (i == value)), key, str(i), str(value)))
            keyf.write(KEYF_C2 % (key, str(value), key))
            keyf.write(KEYF_C3 % (key, str(value), key))
        UPDATE_PROGRESS()
    allf.write('\n' + ALLF_C1 % "total")
UPDATE_PROGRESS()


ALLF_C1 = "function bac_tracker:refresh_adv_counts/%s\n"
ALLF_C2 = "\nfunction bac_tracker:refresh_adv_counts/total\n"
TOTALF_C1 = "scoreboard players set @p bac_tracker.total 0\n"
TOTALF_C2 = "scoreboard players operation @p bac_tracker.total += @p bac_tracker.%s\n"
KEYF_C1 = "scoreboard players set @p bac_tracker.%s 0\n"
KEYF_C2 = "execute if entity @p[advancements={%s=true}] run scoreboard players add @p bac_tracker.%s 1\n"
with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/all.mcfunction", "w") as allf:
    with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/total.mcfunction", "w") as totalf:
        totalf.write(TOTALF_C1)
        UPDATE_PROGRESS()
        for key, value in DATA.items():
            allf.write(ALLF_C1 % key)
            totalf.write(TOTALF_C2 % key)
            with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/{key}.mcfunction", "w") as keyf:
                keyf.write(f"# Total: {len(value)}\n")
                keyf.write(KEYF_C1 % key)
                for v in value:
                    keyf.write(KEYF_C2 % (v, key))
            UPDATE_PROGRESS()
    allf.write(ALLF_C2)
UPDATE_PROGRESS()


if PACK_FORMAT >= 8:
    input("\nPress Enter to exit.\n")
    exit(0)


print("\nModifying datapack for pre-1.18 compatibility...")
files = glob.glob(f"{FUNCTIONS_PATH}/**/*.mcfunction", recursive=True)
UPDATE_PROGRESS = get_progress_update_function(len(files))
UPDATE_PROGRESS()
for filename in files:
    filename = filename.replace('\\', '/')
    with open(filename, "r") as file:
        content = file.read()
    with open(filename, "w") as file:
        file.write(content.replace("bac_tracker.", ''))
    UPDATE_PROGRESS()


input("\nPress Enter to exit.\n")
