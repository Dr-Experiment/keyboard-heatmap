import tkinter as tk
import tkinter.font as tkf
import keyboardlayout as kl
import keyboardlayout.tkinter as klt
import matplotlib
from matplotlib import cm
from pynput.keyboard import Key, Listener
from collections import Counter

CMAP_NAME = cm.spring
LAYOUT_NAME = kl.LayoutName.QWERTY


key_counts = Counter()
key_size = 60


def perKey(key):
    k_str = str(key).replace("'", "").replace("Key.", "").upper()
    key_counts[k_str] += 1

def start_listener():
    listener = Listener(on_press=perKey)
    listener.start()

window = tk.Tk()
window.title("Live Heatmap")

key_info_dict = {
    "margin": 5,
    "txt_color": "white",
    "txt_font": tkf.Font(family="Arial", size=10, weight="bold"),
    "txt_padding": (key_size // 6, key_size // 10)
}

keyboard_layout = klt.KeyboardLayout(
    LAYOUT_NAME,
    kl.KeyboardInfo(position=(0, 0), padding=2),
    (key_size, key_size),
    kl.KeyInfo(**key_info_dict, color="black"),
    master=window
)

def rgba_to_hex(rgba):
    return "#" + "".join(f"{int(c*255):02x}" for c in rgba[:3])


def update_gui():
    if key_counts:
        counts_snapshot = dict(key_counts) 
        
        vals = list(counts_snapshot.values())
        norm = matplotlib.colors.Normalize(vmin=min(vals), vmax=max(vals) + 1)
        mapper = cm.ScalarMappable(norm=norm, cmap=CMAP_NAME)

        for k_name, count in counts_snapshot.items():
            try:
                key_obj = getattr(kl.Key, k_name)
                color = rgba_to_hex(mapper.to_rgba(count))
                keyboard_layout.update_key(key_obj, kl.KeyInfo(**key_info_dict, color=color))
            except AttributeError:
                continue 
    
    window.after(100, update_gui)

start_listener()
update_gui()
window.mainloop()
