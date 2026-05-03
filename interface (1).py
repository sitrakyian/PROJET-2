# ============================================================
# INTERFACE - Projet : Organisation de Repas Partagé
# ============================================================
# Design fidèle à la maquette du PDF (Partie II : Interface)
# Toute la logique métier est dans lib/noyau.py
# ============================================================

from tkinter import *
import customtkinter as ctk
from tkinter import ttk
import noyau as N

ctk.set_appearance_mode("Light")

# ============================================================
# PALETTE DE COULEURS (extraite du design PDF)
# ============================================================
BLEU           = "#0080FF"
BLEU_BOISSON   = "#0080FF"
GRIS_FOND      = "#F9FAFB"
GRIS_BORDURE   = "#E5E7EB"
GRIS_TEXTE     = "#6B7280"
NOIR_TITRE     = "#111827"
VERT_OK        = "#CFFFDC"
VERT_ENTREE    = "#04BE36"
ROUGE_PLATS    = "#FF0000"
ROUGE_DESSERTS = "#BE0430"
ROUGE_KO       = "#DC2626"
ROUGE_BG       = "#FFE7E7"
ORANGE_NOTIF   = "#FEF3C7"
ORANGE_TXT     = "#92400E"
VERT_SERVICE   = "#DCFCE7"
VERT_SVC_TXT   = "#166534"
ROUGE_SVC      = "#FEE2E2"
ROUGE_SVC_TX   = "#991B1B"
BLANC          = "#FFFFFF"
NOIR           = "#000000"
FOND_GLOBAL    = "#E7F6F7"

# ============================================================
# TRI GLOBAL
# ============================================================
tri_colonne   = "nom"
tri_croissant = True

# ============================================================
# MISE A JOUR DE L INTERFACE
# ============================================================

def mise_a_jour():
    _maj_compteurs()
    _maj_indicateurs()
    _maj_notification()
    _maj_tableau()


def _maj_compteurs():
    sv_compteurs.set(
        str(N.total_participants()) + " participants  " +
        str(N.total_elements()) + " elements au total"
    )


def _maj_indicateurs():
    ind  = N.calculer_indicateurs()
    nb_s = N.calculer_nb_repas_possible()
    sv_services.set(str(nb_s) + " services possibles")

    if N.verifier_repas_possible():
        lbl_service_badge.configure(text="✓ Service possible",
                                  fg_color=VERT_OK, text_color=VERT_SVC_TXT)
    else:
        lbl_service_badge.configure(text="✗ Service impossible",
                                  fg_color=ROUGE_BG, text_color=ROUGE_SVC_TX)

    for i, cat in enumerate(N.CATEGORIES):
        nb  = ind[cat]
        pct = N.pourcentage_categorie(cat)
        etat = N.etat_categorie(cat)
        if etat == "OK":
            couleur = VERT_OK
            couleur_frame= VERT_ENTREE
        else:
            etat    = "MANQUE"
            couleur = ROUGE_BG
            couleur_frame = ROUGE_KO
        lbl_cat_etat[i].configure(text=etat, fg_color=couleur)
        bloc_etat_list[i].configure(fg_color=couleur, border_color=couleur_frame)
        lbl_cat_nb[i].config(text=str(nb))
        lbl_cat_pct[i].config(text=str(pct) + "%")
        bloc_color[i].configure(border_color=couleur_frame)


def _maj_notification():
    manquants = N.calculer_manquants()
    if manquants:
        noms = ", ".join(manquants)
        sv_notif.set("Il manque (" + noms + ") pour completer un repas")
        frame_notif.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 4))
    else:
        frame_notif.grid_remove()


def _maj_tableau():
    for row in tableau.get_children():
        tableau.delete(row)
    for i, p in enumerate(N.participants):
        tag = "evenrow" if i % 2 else "oddrow"
        tableau.insert("", END, iid=str(i),
                       values=(p["nom"] + " " + p["prenom"],
                               p["categorie"],
                               p["nom_element"],
                               p["quantite"]),
                       tags=(tag,))


# ============================================================
# HELPERS FORMULAIRE
# ============================================================

def _ligne_champ(parent, row_num, libelle, sv):
    Label(parent, text=libelle, font=("Inter", 11),
          bg=BLANC, fg=NOIR_TITRE, anchor="w", width=20
          ).grid(row=row_num, column=0, padx=(24, 8), pady=7, sticky="w")
    e = Entry(parent, textvariable=sv, width=34,
              font=("Inter", 11), relief="solid", bd=1)
    e.grid(row=row_num, column=1, padx=(0, 24), pady=7, sticky="ew")
    return e


def _ligne_menu(parent, row_num, libelle, sv):
    Label(parent, text=libelle, font=("Inter", 11),
          bg=BLANC, fg=NOIR_TITRE, anchor="w", width=20
          ).grid(row=row_num, column=0, padx=(24, 8), pady=7, sticky="w")
    if sv.get() not in N.CATEGORIES:
        sv.set("selectionner une categorie...")
    menu = OptionMenu(parent, sv, *N.CATEGORIES)
    menu.config(font=("Inter", 11), bg=BLANC,
                relief="solid", bd=1, highlightthickness=0, width=28)
    menu.grid(row=row_num, column=1, padx=(0, 24), pady=7, sticky="ew")
    return menu


def _boutons_form(parent, row_num, texte_ok, cmd_ok, cmd_annuler, couleur_ok=None):
    if couleur_ok is None:
        couleur_ok = BLEU
    f = Frame(parent, bg=BLANC)
    f.grid(row=row_num, column=0, columnspan=2, pady=16)
    Button(f, text=texte_ok, bg=couleur_ok, fg=BLANC,
           font=("Inter", 12), width=14, relief="flat", cursor="hand2",
           command=cmd_ok).grid(row=0, column=0, padx=16)
    Button(f, text="Annuler", bg=GRIS_FOND, fg=NOIR_TITRE,
           font=("Inter", 12), width=14, relief="flat", cursor="hand2",
           command=cmd_annuler).grid(row=0, column=1, padx=16)


# ============================================================
# FORMULAIRE D AJOUT
# ============================================================

def ouvrir_formulaire_ajout():
    win = Toplevel(ma_fenetre)
    win.title("Ajouter un participant")
    win.geometry("560x460")
    win.resizable(False, False)
    win.config(bg=BLANC)
    win.minsize(560, 460)
    win.columnconfigure(1, weight=1)

    Label(win, text="Ajouter un participant",
          font=("Inter", 18, "bold"),
          bg=BLANC, fg=NOIR_TITRE
          ).grid(row=0, column=0, columnspan=2, padx=24, pady=(20, 14), sticky="w")

    sv_nom       = StringVar()
    sv_prenom    = StringVar()
    sv_categorie = StringVar()
    sv_element   = StringVar()
    sv_quantite  = StringVar()
    sv_quantite.set("1")
    sv_erreur    = StringVar()

    # ligne 1 : Nom
    _ligne_champ(win, 1, "Nom",                 sv_nom)
    # ligne 2 : Prenom
    _ligne_champ(win, 2, "Prenom",              sv_prenom)
    # ligne 3 : Categorie
    _ligne_menu( win, 3, "Categorie",           sv_categorie)
    # ligne 4 : Nom de l element
    _ligne_champ(win, 4, "Nom de l'element",    sv_element)
    # ligne 5 : Quantite
    _ligne_champ(win, 5, "Quantite a apporter", sv_quantite)

    lbl_err = Label(win, textvariable=sv_erreur,
                    fg=ROUGE_KO, bg=BLANC,
                    font=("Inter", 10), wraplength=500)
    lbl_err.grid(row=6, column=0, columnspan=2, padx=24, pady=(0, 2))

    def _ajouter():
        res = N.ajouter_participant(
            sv_nom.get(), sv_prenom.get(),
            sv_categorie.get(), sv_element.get(), sv_quantite.get()
        )
        if res is True:
            mise_a_jour()
            win.destroy()
        else:
            sv_erreur.set(res)

    _boutons_form(win, 7, "Ajouter", lambda: _ajouter(), lambda: win.destroy())


# ============================================================
# FORMULAIRE DE MODIFICATION
# ============================================================

def ouvrir_formulaire_modification(index):
    p   = N.participants[index]
    win = Toplevel(ma_fenetre)
    win.title("Modifier le participant")
    win.geometry("560x460")
    win.resizable(False, False)
    win.config(bg=BLANC)
    win.columnconfigure(1, weight=1)

    Label(win, text="Modifier le participant",
          font=("Inter", 18, "bold"),
          bg=BLANC, fg=NOIR_TITRE
          ).grid(row=0, column=0, columnspan=2, padx=24, pady=(20, 14), sticky="w")

    sv_nom       = StringVar(); sv_nom.set(p["nom"])
    sv_prenom    = StringVar(); sv_prenom.set(p["prenom"])
    sv_categorie = StringVar(); sv_categorie.set(p["categorie"])
    sv_element   = StringVar(); sv_element.set(p["nom_element"])
    sv_quantite  = StringVar(); sv_quantite.set(str(p["quantite"]))
    sv_erreur    = StringVar()

    _ligne_champ(win, 1, "Nom",                 sv_nom)
    _ligne_champ(win, 2, "Prenom",              sv_prenom)
    _ligne_menu( win, 3, "Categorie",           sv_categorie)
    _ligne_champ(win, 4, "Nom de l'element",    sv_element)
    _ligne_champ(win, 5, "Quantite a apporter", sv_quantite)

    lbl_err = Label(win, textvariable=sv_erreur,
                    fg=ROUGE_KO, bg=BLANC,
                    font=("Inter", 10), wraplength=500)
    lbl_err.grid(row=6, column=0, columnspan=2, padx=24, pady=(0, 2))

    def _modifier():
        res = N.modifier_participant(
            index,
            sv_nom.get(), sv_prenom.get(),
            sv_categorie.get(), sv_element.get(), sv_quantite.get()
        )
        if res is True:
            mise_a_jour()
            win.destroy()
        else:
            sv_erreur.set(res)

    _boutons_form(win, 7, "Modifier", lambda: _modifier(), lambda: win.destroy())


# ============================================================
# CONFIRMATION DE SUPPRESSION
# ============================================================

def ouvrir_confirmation_suppression(index):
    p          = N.participants[index]
    nom_prenom = p["nom"] + " " + p["prenom"]

    win = Toplevel(ma_fenetre)
    win.title("Confirmer la suppression")
    win.geometry("430x210")
    win.resizable(False, False)
    win.config(bg=BLANC)

    Label(win, text="Confirmer la suppression",
          font=("Inter", 14, "bold"),
          bg=BLANC, fg=NOIR_TITRE
          ).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 8), sticky="w")

    Label(win,
          text="Etes-vous sur de vouloir supprimer\n" + nom_prenom + " de la liste ?",
          font=("Inter", 11), bg=BLANC, fg=GRIS_TEXTE, justify="left"
          ).grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 16), sticky="w")

    def _confirmer():
        N.supprimer_participant(index)
        mise_a_jour()
        win.destroy()

    frame_btn = Frame(win, bg=BLANC)
    frame_btn.grid(row=2, column=0, columnspan=2, pady=8)

    Button(frame_btn, text="Oui, supprimer",
           bg=ROUGE_KO, fg=BLANC, font=("Inter", 12), width=14,
           relief="flat", cursor="hand2",
           command=lambda: _confirmer()
           ).grid(row=0, column=0, padx=12)

    Button(frame_btn, text="Non",
           bg=GRIS_FOND, fg=NOIR_TITRE, font=("Inter", 12), width=10,
           relief="flat", cursor="hand2",
           command=lambda: win.destroy()
           ).grid(row=0, column=1, padx=12)


# ============================================================
# ACTIONS TABLEAU
# ============================================================

def action_modifier():
    sel = tableau.selection()
    if sel:
        ouvrir_formulaire_modification(int(sel[0]))


def action_supprimer():
    sel = tableau.selection()
    if sel:
        ouvrir_confirmation_suppression(int(sel[0]))


# ============================================================
# TRI DES COLONNES
# ============================================================

def trier_colonne(col):
    global tri_colonne, tri_croissant
    if tri_colonne == col:
        tri_croissant = not tri_croissant
    else:
        tri_colonne   = col
        tri_croissant = True
    mapping = {
        "Participants":     "nom",
        "Categorie":        "categorie",
        "Nom de l'element": "nom_element",
        "Quantite":         "quantite"
    }
    N.trier(mapping.get(col, "nom"), tri_croissant)
    mise_a_jour()


# ============================================================
# FENETRE PRINCIPALE
# ============================================================

ma_fenetre = Tk()
ma_fenetre.title("Organisateur de Repas Partage")
ma_fenetre.geometry("840x660")
ma_fenetre.config(bg=FOND_GLOBAL)
ma_fenetre.resizable(True, True)
ma_fenetre.columnconfigure(0, weight=1)
ma_fenetre.minsize(840, 660)

sv_compteurs = StringVar()
sv_compteurs.set("0 participants  0 elements au total")
sv_notif     = StringVar()
sv_services  = StringVar()
sv_services.set("0 services possibles")

# ----------------------------------------------------------
# ROW 0 : En-tete
# ----------------------------------------------------------
frame_entete = ctk.CTkFrame(ma_fenetre,
                            fg_color=BLANC,
                            border_color=GRIS_BORDURE,
                            border_width=1,
                            corner_radius=5)
frame_entete.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 5))
frame_entete.columnconfigure(1, weight=1)

Label(frame_entete,
        text="Organisateur de Repas Partage",
        font=("Inter", 15, "bold"),
        bg=BLANC, fg=NOIR_TITRE
        ).grid(row=0, column=0, pady=(15,2),padx=14, sticky="w")

Label(frame_entete,
        textvariable=sv_compteurs,
        font=("Inter", 9),
        bg=BLANC, fg=GRIS_TEXTE
        ).grid(row=1, column=0, padx=14,pady=2, sticky="w")

ctk.CTkButton(frame_entete,
        text="+ Nouveau",
        fg_color=BLEU, text_color=BLANC,corner_radius=5,
        font=("Inter", 16, "bold"),
        cursor="hand2",command=lambda: ouvrir_formulaire_ajout()
        ).grid(row=0, column=2, padx=14,pady=5, rowspan=2)

# ----------------------------------------------------------
# ROW 0 : Bandeau d'alerte (masque par defaut)
# ----------------------------------------------------------
frame_notif = ctk.CTkFrame(frame_entete, fg_color=ROUGE_BG, border_width=2, border_color=ROUGE_KO, corner_radius=5)
Label(frame_notif,
        textvariable=sv_notif,
        bg=ROUGE_BG, fg=NOIR,
        font=("Inter", 10)
        ).grid(row=2, column=0, padx=12, pady=6,  sticky="w")

# ----------------------------------------------------------
# ----------------------------------------------------------
# ROW 1 : Rajout de'espace entre le bandeau d'alerte et le bloc services
# ----------------------------------------------------------
Frame(frame_entete, height=0, bg=BLANC
      ).grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 10))

# ----------------------------------------------------------
# ROW 3 : Bloc services
# ----------------------------------------------------------
frame_services = Frame(ma_fenetre, bg=FOND_GLOBAL)
frame_services.grid(row=3, column=0, sticky="ew", padx=12, pady=(6, 2))
frame_services.columnconfigure(1, weight=1)

frame_services_span = ctk.CTkFrame(frame_services, fg_color=BLANC ,corner_radius=5, border_color=GRIS_BORDURE, border_width=2)
frame_services_span.grid(row=0, column=0, sticky="ew", padx=12,pady=0)
ctk.CTkLabel(frame_services_span,
      textvariable=sv_services,
      font=("Inter", 11), text_color=NOIR_TITRE
      ).grid(row=0, column=0, padx=16, pady=2, sticky="w")

lbl_service_badge = ctk.CTkLabel(frame_services,
                           text="Service impossible",
                           fg_color=ROUGE_BG, text_color=ROUGE_SVC_TX,
                           font=("Inter", 10, "bold"),
                           padx=10, pady=2, corner_radius=5,height=24)
lbl_service_badge.grid(row=0, column=1, padx=12, pady=3, sticky="w",)

# ----------------------------------------------------------
# ROW 4 : Blocs indicateurs par categorie
# ----------------------------------------------------------
frame_cats = ctk.CTkFrame(ma_fenetre,fg_color=FOND_GLOBAL)
frame_cats.grid(row=4, column=0, sticky="ew", padx=12, pady=4)

lbl_cat_point = []
lbl_cat_etat  = []
lbl_cat_nb    = []
lbl_cat_pct   = []
bloc_etat_list = []
bloc_color = []
lbl_pt_couleur = [VERT_ENTREE,ROUGE_PLATS,ROUGE_DESSERTS, BLEU_BOISSON]

for i, cat in enumerate(N.CATEGORIES):
    frame_cats.columnconfigure(i, weight=1)

    bloc = ctk.CTkFrame(frame_cats, fg_color=BLANC, border_width=1, border_color=GRIS_BORDURE, corner_radius=5)
    bloc.grid(row=0, column=i, padx=8, pady=8, sticky="nsew")
    bloc.columnconfigure(1, weight=1)
    bloc_color.append(bloc)

    lbl_pt = Label(bloc, text="●", fg=lbl_pt_couleur[i],
                   font=("Inter", 14), bg=BLANC)
    lbl_pt.grid(row=0, column=0, sticky="w",padx=2,pady=(2,0))
    lbl_cat_point.append(lbl_pt)

    bloc_etat = ctk.CTkFrame(bloc, fg_color=ROUGE_BG, corner_radius=5,width=80)
    lbl_et = ctk.CTkLabel(bloc_etat, text="MANQUE", text_color=NOIR, fg_color=ROUGE_BG,
                   font=("Inter", 9, "bold"),width=40,height=20)
    lbl_et.grid(row=0, column=0, sticky="ew",padx=6,pady=0)
    bloc_etat.grid(row=0, column=1, sticky="e", padx=2, pady=5)
    lbl_cat_etat.append(lbl_et)
    bloc_etat_list.append(bloc_etat)

    Label(bloc, text=cat, font=("Inter", 10, "bold"),
          bg=BLANC, fg=NOIR_TITRE, anchor="w"
          ).grid(row=1, column=0, columnspan=2, sticky="w", padx=2, pady=(0, 0))

    lbl_nb = Label(bloc, text="0",
                   font=("Inter", 12), fg=GRIS_TEXTE,
                   bg=BLANC, anchor="w")
    lbl_nb.grid(row=2, column=0, columnspan=2, sticky="w", padx=2, pady=2)
    lbl_cat_nb.append(lbl_nb)

    lbl_pct = Label(bloc, text="0.0%",
                     font=("Inter", 9), fg=GRIS_TEXTE,
                     bg=BLANC, anchor="w")
    lbl_pct.grid(row=2, column=1, columnspan=2, sticky="w", padx=2, pady=(4,2))
    lbl_cat_pct.append(lbl_pct)

# ----------------------------------------------------------
# ROW 5 : Tableau des participants
# ----------------------------------------------------------
frame_tableau = ctk.CTkFrame(ma_fenetre, fg_color=GRIS_FOND,corner_radius=5, border_color=GRIS_BORDURE, border_width=1)
frame_tableau.grid(row=5, column=0, sticky="nsew", padx=12, pady=(4, 10))
frame_tableau.columnconfigure(0, weight=1)
frame_tableau.rowconfigure(1, weight=1)
ma_fenetre.rowconfigure(5, weight=1)

Label(frame_tableau,
      text="Liste des Participants",
      font=("Inter", 11, "bold"),
      bg=GRIS_FOND, fg=NOIR_TITRE
      ).grid(row=0, column=0, sticky="w",padx=12, pady=(6, 4))

style = ttk.Style()
style.theme_use("default")
style.configure("Repas.Treeview",
                background=BLANC,
                foreground=NOIR_TITRE,
                rowheight=28,
                fieldbackground=BLANC,
                font=("Inter", 10))
style.configure("Repas.Treeview.Heading",
                font=("Inter", 10, "bold"),
                background="#F2F2F2",
                foreground=NOIR_TITRE,
                relief="flat",
                padding=(5, 10))
style.map("Repas.Treeview",
          background=[("selected", "#DBEAFE")],
          foreground=[("selected", NOIR_TITRE)])


colonnes = ("Participants", "Categorie", "Nom de l'element", "Quantite", "Actions")
tableau  = ttk.Treeview(frame_tableau, columns=colonnes,
                        show="headings", height=10,
                        style="Repas.Treeview",)
tableau.tag_configure("oddrow", background=BLANC)
tableau.tag_configure("evenrow", background="#F3F4F6")

largeurs = {"Participants": 200, "Categorie": 120,
            "Nom de l'element": 200, "Quantite": 90, "Actions": 90}
for col in colonnes:
    tableau.heading(col, text=col,command=lambda c=col: trier_colonne(c))
    tableau.column(col, width=largeurs[col], anchor="center", minwidth=60)

tableau.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

scrollbar_v = Scrollbar(frame_tableau, orient="vertical",
                        command=tableau.yview)
tableau.configure(yscrollcommand=scrollbar_v.set)
scrollbar_v.grid(row=1, column=1, sticky="ns")

# ----------------------------------------------------------
# ROW 6 : Boutons Modifier / Supprimer
# ----------------------------------------------------------
frame_actions = Frame(frame_tableau, bg=GRIS_FOND)
frame_actions.grid(row=6, column=0, sticky="w", padx=12, pady=(4,10))

Button(frame_actions, text="Modifier",
       font=("Inter", 10), bg=BLANC, fg=NOIR_TITRE,
       relief="solid", bd=1, padx=12, pady=5, cursor="hand2",
       command=lambda: action_modifier()
       ).grid(row=0, column=0, padx=(0, 8))

Button(frame_actions, text="Supprimer",
       font=("Inter", 10), bg=BLANC, fg=ROUGE_KO,
       relief="solid", bd=1, padx=12, pady=5, cursor="hand2",
       command=lambda: action_supprimer()
       ).grid(row=0, column=1)

# ============================================================
# DEMARRAGE
# ============================================================
mise_a_jour()
ma_fenetre.mainloop()
