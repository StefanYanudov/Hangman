#                                        Libraries

from tkinter import *
import random
import sys

#                                     Defining globals

word = ''
hidden_word = ''
start_window = 0
entry = 0
entry_frame = 0
letter = ''
count = 0
lost_game_window = 0
won_game_window = 0


#                               Choosing a word from the list

def choose_word():
    global word, hidden_word
    with open("hangman words.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))

        word = random.choice(words)
        print(word)
        list_of_hidden_word = []
        for i in range(len(word)):
            list_of_hidden_word.append('_')
        hidden_word = ''.join(str(e) for e in list_of_hidden_word)


#                      If a window is closed, the program will end

def close_window(closed_window):
    closed_window.destroy()
    end_program()


#                                     Starting the game

def start_a_game():
    choose_word()
    global hidden_word
    global start_window
    start_window = Tk()
    start_window.geometry("620x720")
    start_window.config(background='orange')
    start_window.title("Hangman")
    start_window.protocol("WM_DELETE_WINDOW", lambda: close_window(start_window))
    window.withdraw()
    #                                         Entry box design

    global entry
    global entry_frame
    entry_frame = Frame(start_window)
    entry_frame.config(bg='orange')
    entry_frame.pack(side=BOTTOM)
    entry = Entry(entry_frame,
                  font=('Arial', 30),
                  relief=RAISED,
                  bd=5
                  )
    entry.grid(row=1, column=0)

    #                   When a letter is submitted, the entry box will be cleared

    def clear_entrybox():
        entry.delete(0, END)

    #                                       Hangman drawing
    def draw_hangman():
        hangman_parts = {
            1: (384, 485, 512, 485),  # 1
            2: (449, 484, 449, 124),  # 2
            3: (292, 124, 452, 124),  # 3
            4: (294, 124, 294, 163),  # 4
            5: (261, 163, 330, 228),  # 5
            6: (294, 228, 294, 352),  # 6
            7: (244, 412, 294, 350),  # 7
            8: (344, 412, 294, 350),  # 8
            9: (293, 277, 244, 285),  # 9
            10: (293, 277, 344, 285)  # 10
        }
        if count == 5:
            canvas.create_oval(261, 163, 330, 228, fill="black")

        if count > 0:
            for i in range(1, count + 1):
                if i != 5:
                    coordinates = hangman_parts.get(i)
                    if coordinates:
                        canvas.create_line(coordinates, fill="black", width=5)

    #                                       Submit button design
    def submit():
        get_a_letter = entry.get()
        global letter
        letter = get_a_letter
        if len(letter) > 1:
            return
        guess = letter.lower()
        global hidden_word
        hidden_word_list = list(hidden_word)
        if guess in word:
            for l in range(len(word)):
                if word[l] == guess:
                    hidden_word_list[l] = guess
                    hidden_word = "".join(hidden_word_list)
        else:
            global count
            count += 1
            print(count)
            draw_hangman()
        if count == 10:
            endgame()
        elif '_' not in hidden_word:
            endgame()
        ingame_hidden_word.config(text=' '.join(hidden_word))

    submit_button = Button(entry_frame,
                           text='Submit',
                           font=('Arial', 15),
                           command=lambda: [submit(), clear_entrybox()],
                           padx=20,
                           pady=7,
                           relief=RAISED,
                           bd=5
                           )
    submit_button.grid(row=1, column=1)

    def on_enter(event):
        submit()
        clear_entrybox()

    start_window.bind("<Return>", on_enter)
    #                                       Hidden word design

    ingame_hidden_word = Label(entry_frame,

                               text=' '.join(hidden_word),
                               font=('Arial', 20, 'bold'),
                               padx=10,
                               pady=10,
                               relief=RAISED,
                               bd=5
                               )
    ingame_hidden_word.grid(row=0, column=0, columnspan=2)
    canvas = Canvas(start_window, height=720, width=620, highlightthickness=0)
    canvas.config(bg='orange')
    canvas.pack()


#                                           End of the game

def end_program():
    sys.exit()


#                                         Restart the lost game
def restart_lost_game():
    global start_window, count
    count = 0
    if start_window:
        start_window.destroy()
    start_a_game()
    lost_game_window.withdraw()


#                                         Restart the won game
def restart_won_game():
    global start_window, count
    count = 0
    if start_window:
        start_window.destroy()
    start_a_game()
    won_game_window.withdraw()


#                                    The two possible ends of the game
def endgame():
    global hidden_word
    if count == 10:
        global lost_game_window
        lost_game_window = Tk()
        lost_game_window.geometry("320x200")
        lost_game_window.title("Hangman")
        lost_game_window.protocol("WM_DELETE_WINDOW", lambda: close_window(lost_game_window))
        lost_game_window_frame = Frame(lost_game_window)
        lost_game_window_frame.pack(side=TOP)
        lost_game_label_1 = Label(lost_game_window_frame,
                                  text="You lost!",
                                  font=('Arial', 20)
                                  ).grid(row=0, column=0, columnspan=2)
        lost_game_label_2 = Label(lost_game_window_frame,
                                  text=f"The word was '{word}'?",
                                  font=('Arial', 20)
                                  ).grid(row=1, column=0, columnspan=2)
        lost_game_label_3 = Label(lost_game_window_frame,
                                  text="Do you want to try again?",
                                  font=('Arial', 20)
                                  ).grid(row=2, column=0, columnspan=2)
        lost_reset_button = Button(lost_game_window_frame,
                                   text="Restart",
                                   font=('Arial', 10),
                                   fg="black",
                                   bg="orange",
                                   relief=RAISED,
                                   pady=5,
                                   width=6,
                                   height=4,
                                   command=restart_lost_game
                                   )
        lost_reset_button.grid(row=3, column=0)
        lost_game_exit_button = Button(lost_game_window_frame,
                                       text="Exit",
                                       font=('Arial', 10),
                                       fg="white",
                                       bg="red",
                                       relief=RAISED,
                                       pady=5,
                                       width=6,
                                       height=4,
                                       command=end_program
                                       )
        lost_game_exit_button.grid(row=3, column=1)
    elif '_' not in hidden_word:
        global won_game_window
        won_game_window = Tk()
        won_game_window.geometry("320x200")
        won_game_window.title("Hangman")
        won_game_window.protocol("WM_DELETE_WINDOW", lambda: close_window(lost_game_window))
        won_game_window_frame = Frame(won_game_window)
        won_game_window_frame.pack(side=TOP)
        won_game_label_1 = Label(won_game_window_frame,
                                 text="You won!",
                                 font=('Arial', 20)
                                 ).grid(row=0, column=0, columnspan=2)
        won_game_label_2 = Label(won_game_window_frame,
                                 text="Do you want to try again?",
                                 font=('Arial', 20)
                                 ).grid(row=1, column=0, columnspan=2)
        won_reset_button = Button(won_game_window_frame,
                                  text="Restart",
                                  font=('Arial', 10),
                                  fg="black",
                                  bg="orange",
                                  relief=RAISED,
                                  pady=5,
                                  width=6,
                                  height=4,
                                  command=restart_won_game
                                  )
        won_reset_button.grid(row=2, column=0)
        won_game_exit_button = Button(won_game_window_frame,
                                      text="Exit",
                                      font=('Arial', 10),
                                      fg="white",
                                      bg="red",
                                      relief=RAISED,
                                      pady=5,
                                      width=6,
                                      height=4,
                                      command=end_program
                                      )
        won_game_exit_button.grid(row=2, column=1)


#                                 Start Window

window = Tk()
window.geometry("620x720")
window.config(background='orange')
#                                 Program Icon
window.title("Hangman")
icon = PhotoImage(file='hangman.png')
window.iconphoto(True, icon)

#                                  Start Frame

frame = Frame(window)
frame.pack()

#                                   Label

photo = PhotoImage(file='Hangman-0.png')
label = Label(frame,
              text="Hangman",
              font=('Arial', 20, 'bold'),
              fg='black',
              relief=RAISED,
              bd=10,
              padx=20,
              pady=20,
              image=photo,
              compound='bottom',
              height=280,
              width=200)
label.pack()

#                              Starting buttons

start_button = Button(frame,
                      text="Start Game",
                      font=('Arial', 20, 'bold'),
                      fg='black',
                      relief=RAISED,
                      bd=10,
                      padx=37,
                      pady=20,
                      command=start_a_game
                      )

exit_button = Button(frame,
                     text="Exit",
                     font=('Arial', 20, 'bold'),
                     fg='black',
                     relief=RAISED,
                     bd=10,
                     padx=86,
                     pady=20,
                     command=end_program
                     )
exit_button.pack(side='bottom')
start_button.pack(side='bottom')

#                               Program initializing
window.mainloop()
