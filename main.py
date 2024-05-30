import pandas as pd
from random import choice
from tkinter import *

# Constants & Variables
BACKGROUND_COLOR = "#B1DDC6"
WORDS_TO_LEARN_CSV = "./data/words_to_learn.csv"
PORTUGUESE_WORDS = "./data/portuguese_words.csv"
CARD_FRONT_IMG = "./images/card_front.png"
CARD_BACK_IMG = "./images/card_back.png"
WRONG_IMG = "./images/wrong.png"
RIGHT_IMG = "./images/right.png"
card = {}
flip_timer = None


# Functions
def load_data():
    """
    Loads data from a CSV file. If 'WORDS_TO_LEARN_CSV' is not found, it loads from 'FRENCH_WORDS_CSV'.
    Returns a list of dictionaries representing the data.
    """
    try:
        data = pd.read_csv(WORDS_TO_LEARN_CSV)
    except FileNotFoundError:
        data = pd.read_csv(PORTUGUESE_WORDS)
    return data.to_dict(orient="records")


def new_card():
    """
    This function selects a new card from the data dictionary list and updates the canvas with the new card's
    information. It also sets a timer to flip the card after 3000 milliseconds.
    """
    global flip_timer, card
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    card = choice(data_dict_list)
    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.itemconfig(card_title, fill="black", text=lang_in)
    canvas.itemconfig(card_word, fill="black", text=card[lang_in])
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """
    This function flips the card on the canvas, changing the image to the back of the card and updating the text to the
    translation of the word in the other language.
    """
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(card_title, fill="white", text=lang_out)
    canvas.itemconfig(card_word, fill="white", text=card[lang_out])


def word_known():
    """
    This function removes the current card from the data dictionary list, writes the updated list to a CSV file, and
    selects a new card.
    """
    data_dict_list.remove(card)
    new_data = pd.DataFrame(data_dict_list)
    new_data.to_csv(WORDS_TO_LEARN_CSV, index=False)
    new_card()


if __name__ == "__main__":
    # Data Import
    data_dict_list = load_data()
    lang_in = list(data_dict_list[0].keys())[0]
    lang_out = list(data_dict_list[0].keys())[1]

    # --------------- UI Setup ------------------
    # Creating the main window
    window = Tk()
    window.title("Flashcard App")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    # Creating the canvas
    canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

    card_front_img = PhotoImage(file=CARD_FRONT_IMG)
    card_back_img = PhotoImage(file=CARD_BACK_IMG)

    canvas_img = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
    card_word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
    canvas.grid(column=0, row=0, columnspan=2)

    # Creating the buttons
    cross_img = PhotoImage(file=WRONG_IMG)
    cross_button = Button(image=cross_img, highlightthickness=0, command=new_card)
    cross_button.grid(column=0, row=1)

    tick_img = PhotoImage(file=RIGHT_IMG)
    tick_button = Button(image=tick_img, highlightthickness=0, command=word_known)
    tick_button.grid(column=1, row=1)

    new_card()

    # Starting the main loop
    window.mainloop()
