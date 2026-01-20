#the minimal source code of the executable in order to keep file size small enough to upload

import tkinter as tk
import tkinter.font as tkf
import keyboardlayout as kl
import keyboardlayout.tkinter as klt
from pynput.keyboard import Key, Listener
from collections import Counter


LAYOUT_NAME = kl.LayoutName.QWERTY
key_counts = Counter()
key_size = 60


window = tk.Tk()
window.title("Live Heatmap")

font = tkf.Font(family="Arial", size=10, weight="bold")

key_info_dict = {
    "margin": 5,
    "txt_color": "white",
    "txt_font": font,
    "txt_padding": (key_size // 6, key_size // 10)
}

keyboard_layout = klt.KeyboardLayout(
    LAYOUT_NAME,
    kl.KeyboardInfo(position=(0, 0), padding=2),
    (key_size, key_size),
    kl.KeyInfo(**key_info_dict, color="black"),
    master=window
)


def heat_color(count, min_c=0, max_c=20):
    count = min(max(count, min_c), max_c)
    ratio = (count - min_c) / max(1, (max_c - min_c))
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"


def perKey(key):
    k_str = str(key).replace("'", "").replace("Key.", "").upper()
    key_counts[k_str] += 1

def start_listener():
    listener = Listener(on_press=perKey)
    listener.start()

start_listener()


def update_gui():
    if key_counts:
        counts_snapshot = dict(key_counts)
        for k_name, count in counts_snapshot.items():
            try:
                key_obj = getattr(kl.Key, k_name)
                color = heat_color(count)
                keyboard_layout.update_key(key_obj, kl.KeyInfo(**key_info_dict, color=color))
            except AttributeError:
                continue
    window.after(100, update_gui)


update_gui()
window.mainloop()

