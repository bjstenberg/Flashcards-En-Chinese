from tkinter import *
import pandas
import random
# from gtts import gTTS, lang  # Google Text-to-Speech
# from playsound import playsound
# import os

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
targ_lang_code = "zh_cn"
targ_lang_name = "Chinese"
targ_prnc_code = "pinyin"
home_lang_code = "en"
home_lang_name = "English"
new_filepath = f"data/words_to_learn_{targ_lang_code}.csv"


try:
    data = pandas.read_csv(new_filepath)
except FileNotFoundError:
    data = pandas.read_csv("data/412_zh_freq_dict.csv")
finally:
    to_learn = data.to_dict(orient="records")

print(to_learn)


# def audio(text, code):
#     # Play Audio of word using Google Text-to-Speech
#     audio_output = gTTS(text=text, lang=code)
#     audio_output.save("audio.mp3")
#     playsound("audio.mp3", True)
#     os.remove("audio.mp3")


def sel_char_type():
    global targ_lang_code
    char = char_type.get()
    targ_lang_code = char


def sel_roman_type():
    global targ_prnc_code
    roman = roman_type.get()
    targ_prnc_code = roman


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card_canvas.itemconfig(card_background, image=card_front_image)
    card_canvas.itemconfig(card_title, text=targ_lang_name, fill="black")
    card_canvas.itemconfig(card_word, text=current_card[targ_lang_code], fill="black", font=("normal", 108, "bold"))
    card_canvas.itemconfig(card_pronunciation, text=current_card[targ_prnc_code], fill="black")
    # 'zh-CN': 'Chinese', 'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)'
    # window.after(100, func=lambda: audio(text=current_card[targ_lang_code], code="zh"))
    # window.after(5000, func=lambda: audio(text=current_card[home_lang_code], code="en"))

    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    global flip_timer
    window.after_cancel(flip_timer)
    card_canvas.itemconfig(card_background, image=card_back_image)
    card_canvas.itemconfig(card_title, text=home_lang_name, fill="white")
    card_canvas.itemconfig(card_word, text=current_card[home_lang_code], fill="white", font=("Ariel", 72, "bold"))
    card_canvas.itemconfig(card_pronunciation, text=current_card[targ_prnc_code], fill="white")
    # 'zh-CN': 'Chinese', 'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)'

    #window.after(1000, func=lambda: audio(text=current_card[targ_lang_code], code="zh"))
    # window.after(100, func=lambda: audio(text=current_card[home_lang_code], code="en"))
    flip_timer = window.after(5000, func=next_card)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    # new_filepath
    data.to_csv(new_filepath, index=False)
    next_card()


window = Tk()
window.title("Flashy | Chinese 中文")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

char_type = StringVar()
roman_type = StringVar()

# # ---  UI setup ---

card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_background = card_canvas.create_image(400, 263, image=card_front_image)
card_title = card_canvas.create_text(400, 75, text="", font=("Ariel", 24, "italic"))
card_word = card_canvas.create_text(400, 263, text="", font=("Ariel", 72, "bold"))
card_pronunciation = card_canvas.create_text(400, 400, text="", font=("Ariel", 36))
card_canvas.grid(row=0, column=0, columnspan=4)

wrong_button_photo_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_photo_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0, rowspan=3)


char_type_label = Label(fg="black", bg=BACKGROUND_COLOR, text="Characters:", font=("Ariel", 14, "bold"))
char_type_label.grid(row=1, column=1)
char_type_simp  = Radiobutton(window, fg="black", bg=BACKGROUND_COLOR, text="Simplified", variable=char_type, value='zh_cn', command=sel_char_type)
char_type_simp.select()
char_type_simp.grid(row=2, column=1)
char_type_trad = Radiobutton(window, fg="black", bg=BACKGROUND_COLOR, text="Traditional", variable=char_type, value='zh_tw', command=sel_char_type)
char_type_trad.deselect()
char_type_trad.grid(row=3, column=1)


roman_type_label = Label(fg="black", bg=BACKGROUND_COLOR, text="Romanization:", font=("Ariel", 14, "bold"))
roman_type_label.grid(row=1, column=2)
roman_type_piny = Radiobutton(window, fg="black", bg=BACKGROUND_COLOR, text="Pinyin (Mandarin)", variable=roman_type, value="pinyin", command=sel_roman_type)
roman_type_piny.select()
roman_type_piny.grid(row=2, column=2)
roman_type_jyut = Radiobutton(window, fg="black", bg=BACKGROUND_COLOR, text="Jyutping (Cantonese)", variable=roman_type, value="jyutping", command=sel_roman_type)
roman_type_jyut.deselect()
roman_type_jyut.grid(row=3, column=2)

right_button_photo_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_photo_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=3,rowspan=3)


next_card()

window.mainloop()