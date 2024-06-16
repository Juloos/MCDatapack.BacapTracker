import json
import zipfile
import glob
from math import ceil
import sys
import re
import os
import shutil

PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(f"{PATH}/config.json", "r"))
CONTEXTS = json.load(open(f"{PATH}/category_contexts.json", "r"))

# Config validation
err = None
if CONFIG['Sidebar']['Use custom pages']:
    for page in range(len(CONFIG['Sidebar']['Pages'])):
        if CONFIG['Sidebar']['Pages'][page].count('PAGE_INFO') > 1:
            err = f"Page {page + 1} have more than one PAGE_INFO key"
        if len(CONFIG['Sidebar']['Pages'][page]) > 15:
            err = f"Page {page + 1} have more than 15 keys"

if err is not None:
    raise ValueError(err)


class Progress:
    current_task = -1
    nb_tasks: int
    def __init__(self, nb_tasks):
        self.nb_tasks = nb_tasks
        self()
    def __call__(self):
        self.current_task += 1
        print("\r ", "[?]" if self.current_task <= self.nb_tasks else "[!]", self.current_task, '/', self.nb_tasks, end='')
    def validate(self):
        print("\r ", "[#]" if self.current_task == self.nb_tasks else "[!]", self.current_task, '/', self.nb_tasks)


def get_blank_function():
    current_blank = -1
    def blank_function():
        nonlocal current_blank
        current_blank += 1
        return f"\u00A7{current_blank}"  # '\u00A7' == '§'
    return blank_function


def find_best_count(key_count, slot_count):
    couple = (max(CONFIG['Sidebar']['Tab count per page'], 0), max(CONFIG['Sidebar']['Page count'], 0))
    if 0 not in couple and couple[0] * couple[1] >= key_count:
        return couple
    if couple[0] == 0 and couple[1] >= ceil(key_count / slot_count):
        return (ceil(key_count / couple[1]), couple[1])
    if couple[0] > 0 and couple[1] == 0:
        return (couple[0], ceil(key_count / couple[0]))
    if couple == (0, 0):
        couple = (0, CONFIG['Sidebar']['Fallback']['Max page count'])
    for p in range(1, key_count + 1):
        for s in range(1, slot_count + 1):
            if s * p == key_count and abs(s - p) < abs(couple[0] - couple[1]):
                couple = (s, p)
    if 0 in couple:
        couple = (max(CONFIG['Sidebar']['Fallback']['Tab count per page'], 1), ceil(key_count / slot_count))
    return couple


PACK_FORMAT = 4  # pack format compatibility with BACAP & MC starts at the 1.13.2 release

# MC 1.21 Port by tjthings
FUNCTIONS = "function" # starting in Minecraft 1.21, functions directory renamed to function
ADVANCEMENTS = "advancement" # starting in Minecraft 1.21, advancements directory renamed to just advancement

BACAP_PATH = (input("Enter the path to a BACAP folder or zip\n> ") if len(sys.argv) < 2 else sys.argv[1]).replace('\\', '/').removesuffix('/')
BACAP_ZIP = None

if BACAP_PATH.endswith(".zip"):
    BACAP_ZIP = zipfile.ZipFile(BACAP_PATH, "r")
try:
    if BACAP_ZIP is not None:
        with BACAP_ZIP.open("pack.mcmeta", "r") as packmeta:
            PACK_FORMAT = json.load(packmeta)["pack"]["pack_format"]
            if PACK_FORMAT < 48: # Backwards compatibility with Minecraft 1.20 and below
                FUNCTIONS = "functions"
                ADVANCEMENTS = "advancements"
        aafile = zipfile.Path(BACAP_ZIP, at=f"data/bc_rewards/{FUNCTIONS}/update_score.mcfunction").open(encoding="utf-8")
    else:
        aafile = open(f"{BACAP_PATH}/data/bc_rewards/{FUNCTIONS}/update_score.mcfunction", "r")
        with open(f"{BACAP_PATH}/pack.mcmeta", "r") as packmeta:
            PACK_FORMAT = json.load(packmeta)["pack"]["pack_format"]
except FileNotFoundError:
    print("File not found. Please check your path.")
    input("Press Enter to exit.\n")
    exit(1)
NB_BAR = CONFIG['Sidebar']['Progress bar']['length']

FUNCTIONS_PATH = f"{PATH}/data/bac_tracker/{FUNCTIONS}"

print(f"\nExctracting data from BACAP (pack format {PACK_FORMAT})...")
DATA: dict = {'hidden': list()}
AA = list()
for line in aafile.readlines():
    is_hidden = False
    if line.startswith("#execute"):
        line = line.removeprefix('#')
        is_hidden = True
    line2 = line.removeprefix("execute as @a[advancements={")
    if CONFIG['Terralith']:
        line2 = line2.removeprefix("execute if score terralith_score bac_settings matches 1 as @a[advancements={")
    if line != line2:
        index = line2.find("=true}]")
        if index != -1:
            if not is_hidden:
                AA.append(line2[:index])
            else:
                DATA['hidden'].append(line2[:index])
aafile.close()

NB_ADV = len(AA)
UPDATE_PROGRESS = Progress(NB_ADV)
for advancement in AA:
    current = advancement
    while not current.startswith("blazeandcave:"):
        try:
            if BACAP_ZIP is not None:
                jsonLike = zipfile.Path(BACAP_ZIP, at=f"data/{current.replace(':', f'/{ADVANCEMENTS}/')}.json").open(encoding="utf-8")
            else:
                jsonLike = open(f"{BACAP_PATH}/data/{current.replace(':', f'/{ADVANCEMENTS}/')}.json", 'r')
        except FileNotFoundError:
            if current in CONTEXTS:
                current = "blazeandcave:" + CONTEXTS[current]
                break
            raise FileNotFoundError(f"Could not find '{current}' in BACAP")
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
UPDATE_PROGRESS.validate()

if BACAP_ZIP is not None:
    BACAP_ZIP.close()

DATA_SUM = {key: len(value) for key, value in DATA.items()}
DATA_SUM['total'] = sum(DATA_SUM.values()) - (DATA_SUM['hidden'] * (not CONFIG['Hidden advancements']))
if not CONFIG['Sidebar']['Use custom pages']:
    PINNED_KEYS = CONFIG['Sidebar']['Pinned tabs']
    TABS_KEYS = sorted(set(DATA_SUM.keys()).difference(PINNED_KEYS, {"hidden"} if not CONFIG['Hidden advancements'] else set()))
    PINNED_KEYS = sorted(set(PINNED_KEYS).intersection(DATA_SUM.keys()), key=lambda k: PINNED_KEYS.index(k))
    SLOT_COUNT = 15 - (3 + 1 + len(PINNED_KEYS))
    KEY_COUNT, PAGE_COUNT = find_best_count(len(TABS_KEYS), SLOT_COUNT)
    tabs_keys = TABS_KEYS.copy()
else:
    TABS_KEYS = [val for page in CONFIG['Sidebar']['Pages'] for val in page]
    PAGE_COUNT = len(CONFIG['Sidebar']['Pages'])


print("\nGenerating datapack...")
UPDATE_PROGRESS = Progress(1 + 1 + (NB_ADV + 1) + len(TABS_KEYS) + 2 * (len(DATA_SUM) + 1))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open(f"{PATH}/pack.mcmeta", "r") as packmeta:
    packjson = json.load(packmeta)
packjson["pack"]["pack_format"] = PACK_FORMAT
with open(f"{PATH}/pack.mcmeta", "w") as packmeta:
    json.dump(packjson, packmeta, indent=2)
UPDATE_PROGRESS()


SETUPF_C1 = 'scoreboard objectives add bac_tracker.%s dummy\n' + \
            'team add bac_tracker.%s\n'                        + \
            'team modify bac_tracker.%s prefix [" "," "]\n'    + \
            'team modify bac_tracker.%s color white\n'         + \
            'team join bac_tracker.%s %s\n'
SETUPF_C2 = 'scoreboard players set page_count'

with open(f"{FUNCTIONS_PATH}/load/setup.mcfunction", "r") as setupf:
    setup = setupf.readlines()
    WAS_PRE_1_18 = re.search("bac_tracker.", ''.join(setup)) is None
    i = 0
    while setup[i] != "## setup_categories {\n":
        i += 1
    i = j = i + 1
    while setup[j] != "## }\n":
        j += 1
    setup = setup[:i] + ['\n'.join(SETUPF_C1 % (key, key, key, key, key, CONFIG['Tabs'][key]) for key in DATA_SUM.keys())] + setup[j:]
with open(f"{FUNCTIONS_PATH}/load/setup.mcfunction", "w") as setupf:
    setupf.write(''.join((f"{SETUPF_C2} bac_tracker.vars {PAGE_COUNT}\n" if line.startswith(SETUPF_C2) else line) for line in setup))
UPDATE_PROGRESS()


PROGRESSF_C = 'execute if score any bac_tracker.total matches %s run scoreboard objectives modify bac_tracker.progress_score displayname [" "," "," ","[",{"text":"%s","color":"green"},{"text":"%s","color":"gray"},"]",{"text":" - ","color":"gray"},{"text":"%s%%","color":"light_purple"}," "," "," "]\n'
with open(f"{FUNCTIONS_PATH}/display/progress_bar.mcfunction", "w") as progressf:
    for i in range(NB_ADV + 1):
        nb_greens = i * NB_BAR // NB_ADV
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
for filename in glob.glob(f"{FUNCTIONS_PATH}/display/page/*.mcfunction"):
    os.remove(filename)  # Would break if re-generating with lesser page count
for page in range(PAGE_COUNT):
    blank = get_blank_function()
    sidebar = list()
    if CONFIG['Sidebar']['Use custom pages']:
        for key in CONFIG['Sidebar']['Pages'][page]:
            match key:
                case 'BLANK':
                    sidebar.append(blank())
                case 'PAGE_INFO':
                    sidebar.append("\u00A7p")
                case _:
                    sidebar.append(CONFIG['Tabs'][key])
            UPDATE_PROGRESS()
    else:
        sidebar.append(blank())
        sidebar += [CONFIG['Tabs'][key] for key in PINNED_KEYS]
        sidebar.append(blank())
        for _ in range(KEY_COUNT):
            if tabs_keys:
                sidebar.append(CONFIG['Tabs'][tabs_keys.pop(0)])
                UPDATE_PROGRESS()
            else:
                break
        sidebar.append(blank())
        sidebar.append("\u00A7p")
    sidebar.reverse()
    with open(f"{FUNCTIONS_PATH}/display/page/{page}.mcfunction", "w", encoding="utf-8") as pagef:
        pagef.write(PAGESF_C1 % (','.join(['" "'] * (ceil(NB_BAR / 2) - 2)), page + 1, PAGE_COUNT))
        for i in range(len(sidebar) - 1, -1, -1):
            pagef.write(PAGESF_C2 % (sidebar[i], i))


ALLF_C1 = 'function bac_tracker:display/refresh_scores/%s\n'
KEYF_C1 = 'execute if score any bac_tracker.%s matches %s run team modify bac_tracker.%s suffix [{"text":": ","color":"gray"},{"text":"%s","color":"yellow"},{"text":"/","color":"gold"},{"text":"%s","color":"yellow"}]\n'
KEYF_C2 = '\nexecute if score any bac_tracker.%s matches %s.. run team modify bac_tracker.%s color green\n'
KEYF_C3 = 'execute unless score any bac_tracker.%s matches %s.. run team modify bac_tracker.%s color white\n'
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


ALLF_C1 = 'function bac_tracker:refresh_adv_counts/%s\n'
ALLF_C2 = '\nfunction bac_tracker:refresh_adv_counts/total\n'
TOTALF_C1 = 'scoreboard players set any bac_tracker.total 0\n'
TOTALF_C2 = 'scoreboard players operation any bac_tracker.total += any bac_tracker.%s\n'
KEYF_C1 = 'scoreboard players set any bac_tracker.%s 0\n'
KEYF_C2 = 'execute if entity @a[advancements={%s=true}] run scoreboard players add any bac_tracker.%s 1\n'
with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/all.mcfunction", "w") as allf:
    with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/total.mcfunction", "w") as totalf:
        totalf.write(TOTALF_C1)
        UPDATE_PROGRESS()
        for key, value in DATA.items():
            allf.write(ALLF_C1 % key)
            if key != 'hidden' or not CONFIG['Hidden advancements']:
                totalf.write(TOTALF_C2 % key)
            with open(f"{FUNCTIONS_PATH}/refresh_adv_counts/{key}.mcfunction", "w") as keyf:
                keyf.write(f"# Total: {len(value)}\n")
                keyf.write(KEYF_C1 % key)
                for v in value:
                    keyf.write(KEYF_C2 % (v, key))
            UPDATE_PROGRESS()
    allf.write(ALLF_C2)
UPDATE_PROGRESS()
UPDATE_PROGRESS.validate()


if PACK_FORMAT < 8 or WAS_PRE_1_18:
    print("\nModifying datapack for pre-1.18 compatibility... " + (WAS_PRE_1_18 and PACK_FORMAT >= 8) * "(was previously generated with pre-1.18)")
    files = glob.glob(f"{FUNCTIONS_PATH}/**/*.mcfunction", recursive=True)
    UPDATE_PROGRESS = Progress(len(files) + 3)

    for filename in files:
        filename = filename.replace('\\', '/')
        with open(filename, "r") as file:
            content = file.read()
        with open(filename, "w") as file:
            file.write(content.replace("bac_tracker.", ''))
        UPDATE_PROGRESS()

    # There is no bac_advfirst scoreboard until BACAP 1.13.3 (pack format 8)
    # We thus remove the leaderboard feature
    if os.path.exists(f"{PATH}/data/bac_leaderboard/"):
        shutil.rmtree(f"{PATH}/data/bac_leaderboard/")
    UPDATE_PROGRESS()
    for filename in ("load", "tick"):
        with open(f"{PATH}/data/minecraft/tags/{FUNCTIONS}/{filename}.json", "r") as file:
            filejson = json.load(file)
        filejson['values'] = [val for val in filejson['values'] if not val.startswith("bac_leaderboard:")]
        with open(f"{PATH}/data/minecraft/tags/{FUNCTIONS}/{filename}.json", "w") as file:
            json.dump(filejson, file, indent=4)
        UPDATE_PROGRESS()

    # TODO: teams (starting from 1.13.3, pack format 8)

    UPDATE_PROGRESS.validate()


input("\nPress Enter to exit.\n")
exit(0)
