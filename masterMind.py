#auto : BOURRE MAXIME
#date : 27/05/2022
#!/usr/bin/env python3
# Path: masterMind.py

import numpy as np, tkinter as tk
#Variables globales

global code
global couleurs
global grille
global coups

indicators = []
code = []
couleurs = [
    "red", "blue", "green", "yellow", "orange", "pink", "white", "grey"
]
turn = 0
grille = []

global Co_event
Co_event = (0, 0)

#TKinter
root = tk.Tk()
root.title('MasterMind')
root.geometry('300x700')
root.resizable(True, False)
root.minsize(width=300, height=700)

tkprops = tk.Canvas(root, width=300, height=700, bg='gray', bd=2)
#definie la grille de proposition

#definition du menu de couleur
selectColor = tk.Menu(tkprops, background="black", tearoff=0, relief=tk.SOLID)
for c in couleurs:
    selectColor.add_command(command=lambda c=c: colorAffect(c), background=c)

proposition = dict()


def colorAffect(c):  #affecte la couleur choisie au rond cliqué
    """
    Affect the color to the cell
    :param c: la couleur choisie
    """
    if Co_event != (-1, -1):  #si le rond cliqué est valide
        if Co_event[0] == 11 - turn:  #si le rond cliqué est sur la bonne ligne
            tkprops.itemconfig(f"rond{Co_event[0]}{Co_event[1]}", fill=c)
            grille[Co_event[0]][Co_event[1]] = c


def findCell(x, y):  #retourne les coordonées de la cellule cliqué
    """
    Find the cell where the click is
    :param x: x coordinate
    :param y: y coordinate
    """
    for i in range(12):
        for j in range(6):
            if (x > 45 + j * 45 and x < 80 + j * 45 and y > 150 + i * 45
                    and y < 185 + i * 45):
                return i, j
    return -1, -1


def do_popup(event):
    """
    Popup menu
    :param event: event
    """
    try:
        selectColor.tk_popup(event.x_root, event.y_root)
    finally:
        selectColor.grab_release()
    global Co_event
    Co_event = findCell(event.x, event.y)


def indication():
    """
    Indication about proposition of player
    """
    props = grille[11 - turn]
    bon = 0  #nombre de bonne couleur
    bienP = 0  #nombre de bonne position et couleur
    tmp = [[0, 0], [0, 1], [1, 0], [1, 1]]
    np.random.shuffle(tmp)
    for i in range(4):
        if props[i] == code[i]:
            bienP += 1
            indicators[11 - turn].itemconfig(f"ind{tmp[i][0]}{tmp[i][1]}",
                                             fill="red")
        elif code.count(props[i]) > 0:
            bon += 1
            indicators[11 - turn].itemconfig(f"ind{tmp[i][0]}{tmp[i][1]}",
                                             fill="white")
    indicators[11 - turn].config(bg="lightgreen")


def reveal():
    """
    Reveal the code
    """
    for i in range(4):
        tkprops.itemconfig(f"code{i}", fill=code[i])


def validprops():  #fonction pour valider les propositions
    """
    Validate the proposition
    """
    global turn
    if grille[11 - turn].count("") == 0:  #la ligne est remplie
        if turn < 12:  #si c'est pas le dernier tour
            if grille[11 - turn] == code:  #si la porpsition est bonne
                indication()
                reveal()
            else:
                indication()
            turn += 1
        else:
            reveal()


def Defcode():
    """
    Generate the code
    """
    global code
    code = []
    for i in range(4):
        code.append(np.random.choice(couleurs))


def reset():
    """
    Reset the game
    """
    global turn
    global grille
    Defcode()
    tmp = [[0, 0], [0, 1], [1, 0], [1, 1]]
    turn = 0
    grille = []
    for i in range(12):
        grille.append(["", "", "", ""])
        indicators[i].config(bg="grey")
        for j in range(4):
            if i == 0:
                tkprops.itemconfig(f"code{j}", fill="black")
            tkprops.itemconfig(f"rond{i}{j}", fill="black")
        for t in tmp:
            indicators[i].itemconfig(f"ind{t[0]}{t[1]}", fill="black")


def init_game():  # Initialize the game
    """
    Initialize the game
    """
    Defcode()

    def indicateur(x, y):  # x,y coordoné de l'indicateur
        #fonction pour crée un indicateur
        indic = tk.Canvas(
            tkprops,
            width=34,
            height=34,
            bg='gray',
            highlightthickness=0,
        )
        indic.place(x=x, y=y)
        indicators.append(indic)
        for i in range(2):
            for j in range(2):
                indic.create_oval(4 + j * 15,
                                  4 + i * 15,
                                  14 + j * 15,
                                  14 + i * 15,
                                  fill='black',
                                  outline='black',
                                  tags=f"ind{i}{j}")

    tkprops.place(x=0, y=0)
    valid = tk.Button(tkprops,
                      text="OK",
                      command=validprops,
                      width=7,
                      bg="lightgreen")
    valid.place(x=5 + 5 * 45, y=100)
    resetB = tk.Button(tkprops,
                       text="RESET",
                       command=reset,
                       width=7,
                       bg="#f00020")
    resetB.place(x=5, y=100)
    for i in range(4):  #crée les 4 ronds du code secret
        tkprops.create_oval(
            10 + i * 75,  #cree le rond a la position x,y	
            10,
            70 + i * 75,
            70,
            fill='black',
            outline='black',
            tags=f"code{i}")

    for i in range(12):
        grille.append(["" for i in range(4)])
        for j in range(5):
            if j == 4:  #création de l'indicateur
                indicateur(45 + j * 45, 150 + i * 45)
            else:  #crée les 4 ronds de la grille
                tkprops.create_oval(
                    45 + j * 45,  #cree le rond a la position x,y	
                    150 + i * 45,
                    80 + j * 45,
                    185 + i * 45,
                    fill='black',
                    outline='black',
                    tags=f"rond{i}{j}")
    tkprops.bind("<Button-3>", do_popup)
    tkprops.pack()


init_game()
root.mainloop()