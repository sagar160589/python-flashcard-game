from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
french_learn_list = []
english_learn_list = []
words_to_learn_dict = {"English": "French"}
french_text = ''
en_translated_text = ''

#Checking if words_to_learn file exist else read from french_words.csv.
try:
    data_french = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    print("File doesn't exist yet....")
    data_french = pandas.read_csv("data/french_words.csv")
data_french_list = data_french["French"].to_list()

#Translate french to english.
def get_en_translated_text(word):
    row_d = data_french[data_french["French"] == word]
    return row_d['English'].values[0]


def get_french_random_words_start():
    global french_text
    french_text = random.choice(data_french_list)
    canvas.itemconfig(french_text_pc, text=french_text)
    return get_en_translated_text(french_text)


def get_french_random_words(word):
    global french_text, en_translated_text,words_to_learn_dict
    if word is not True:
        if french_text not in french_learn_list:
            french_learn_list.append(french_text)
        if en_translated_text not in english_learn_list:
            english_learn_list.append(en_translated_text)
    else:
        data_french_list.remove(french_text)
    french_text = random.choice(data_french_list)
    canvas.itemconfig(french_text_pc, text=french_text, fill='black')
    canvas.itemconfig(canvas_image, image=my_image_fr)
    canvas.itemconfig(french_canvas, text='French', fill='black')
    en_translated_text = get_en_translated_text(french_text)
    window.after(3000, flip_card, en_translated_text)


def flip_card(en_translated_text):
    canvas.itemconfig(canvas_image, image=my_image_en)
    canvas.itemconfig(french_canvas, text="English", fill='white', font=('Ariel', 40, 'italic'))
    canvas.itemconfig(french_text_pc, text=en_translated_text, fill='white', font=('Ariel', 60, 'bold'))


#creating UI for flash cards
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)


#creating a canvas for flashcard image for french
canvas = Canvas()
canvas.config(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
my_image_fr = PhotoImage(file = "images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=my_image_fr)

french_canvas = canvas.create_text(400,150, text='French', fill='black', font=('Ariel',40,'italic'))
french_text_pc = canvas.create_text(400, 263, text="", fill='black', font=('Ariel', 60, 'bold'))
en_translated_text = get_french_random_words_start()
my_image_en = PhotoImage(file= "images/card_back.png")
canvas.grid(column=1, row=0, columnspan=2)

#Creating Buttons
my_image_yes = PhotoImage(file="images/right.png")
button = Button(image=my_image_yes, highlightthickness=0, command=lambda: get_french_random_words(True) )
button.grid(column=2, row=1)

my_image_no = PhotoImage(file="images/wrong.png")
button = Button(image=my_image_no, highlightthickness=0, command=lambda: get_french_random_words(False))
button.grid(column=1, row=1)

window.after(3000, flip_card, en_translated_text)

window.mainloop()
words_to_learn_dict = {"French":french_learn_list,"English":english_learn_list}
words_to_learn = pandas.DataFrame(words_to_learn_dict).to_csv("words_to_learn.csv")

