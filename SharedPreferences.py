import json
import os

PREF_FILE = "prefs.json"

# Load preferences from the file (or return empty dict)
def load_prefs():
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE, "r") as file:
            return json.load(file)
    return {}

# Save the entire preference dictionary
def save_prefs(prefs):
    with open(PREF_FILE, "w") as file:
        json.dump(prefs, file, indent=4)

def set_pref(key, value):
    prefs = load_prefs()
    prefs[key] = value
    save_prefs(prefs)

def get_pref(key, default=None):
    prefs = load_prefs()
    return prefs.get(key, default)

def delete_pref(key):
    prefs = load_prefs()
    if key in prefs:
        del prefs[key]
        save_prefs(prefs)

def loginUser(studentID):
    set_pref("is_logged_in", True)
    set_pref("last_user", studentID)


def logoutUser():
    set_pref("is_logged_in", False)
    delete_pref("last_user")

# loginUser("2023301607")

# print(get_pref("is_logged_in"))
# print(get_pref("last_user"))
# logoutUser()