# PARASCHIV ALEXANDRU-ANDREI
# GRUPA 243
# tema 2 algoritm genetic pentru determinarea maximului unei functii pozitive


# ---------------------------------------------------------------------------------------------------------
# ------------------------------------------Importuri si functii:------------------------------------------
# ---------------------------------------------------------------------------------------------------------

from random import randint, random, randrange, choice
from math import log2, floor, sqrt
from copy import deepcopy
# from numpy import mean


def get_domeniu_defintie(a, b, c):
    delta = pow(b, 2) - 4 * a * c
    return (-b + sqrt(delta)) / 2 * a, (-b - sqrt(delta)) / 2 * a


def get_lg_cromozom():  # l = [log2((b-a)*10^p)]
    return floor(log2((domeniu_de_definitie[1] - domeniu_de_definitie[0]) * (10 ** precizie))) + 1


def get_fitness(x):
    return parametri_functie_maximizat[0] * (x ** 3) + parametri_functie_maximizat[1] * (x ** 2) + parametri_functie_maximizat[2] * x + parametri_functie_maximizat[3]
    # ax^2 + bx +c


def populate():
    return [[randint(0, 1) for _ in range(lungime_cromozom)] for _ in range(dimensiune_populatie)]  # creez populatia initiala
    # cu lungimea_cromozomului coloane si dimensiunea_populatiei linii, fiecare linie avand valori 0 sau 1


def binary_to_decimal(x):
    return int(x, 2)


def get_x(x):
    return round(((binary_to_decimal(x) * (domeniu_de_definitie[1] - domeniu_de_definitie[0])) / (2 ** lungime_cromozom - 1) + domeniu_de_definitie[0]), int(precizie))


def get_select_rate(x):
    return x / suma_totala_fitness  # se obtine impartind fitnessul unui x la suma tuturor valorilor de fitness


def caut_bin(lst, elem):
    stg = 0
    dr = len(lst) - 1
    while stg < dr:
        mid = (stg + dr) // 2  # intreg
        if lst[mid] <= elem < lst[mid + 1]:
            return mid
        elif elem >= lst[mid]:
            stg = mid + 1
        else:
            dr = mid
    return -1


def cross2(c1, c2, poz1, poz2):
    return c1[:poz1] + c2[poz1:poz2] + c1[poz2:], c2[:poz1] + c1[poz1:poz2] + c2[poz2:]


def cross3(c1, c2, c3, poz):
    return c1[poz:] + c2[:poz], c2[poz:] + c3[:poz], c3[poz:] + c1[:poz]

def flip(c, poz1, poz2):
    return c[:poz1] + c[poz2:poz1:-1] + c[poz2:]

# ---------------------------------------------------------------------------------------------------------
# ------------------------------------------Citire date initiale:------------------------------------------
# ---------------------------------------------------------------------------------------------------------

f = open("date.in", "r")
g = open("date.out", "w")

dimensiune_populatie = int(f.readline())
# print(dimensiune_populatie)

parametri_functie_maximizat = tuple(map(int, f.readline().split()))  # creez un tuplu si fac fiecare valoare sa fie int
# print(parametri_functie_maximizat)
print(parametri_functie_maximizat)

domeniu_de_definitie = (-4, 4)
# calculez intervalul pentru functia data

precizie = float(f.readline())
# print(precizie)

probabilitate_recombinare = float(f.readline())
# print(probabilitate_recombinare)

probabilitate_mutatie = float(f.readline())
# print(probabilitate_mutatie)

nr_etape = int(f.readline())
# print(nr_etape)

lungime_cromozom = get_lg_cromozom()
# print(lungime_cromozom)

# ---------------------------------------------------------------------------------------------------------
# ------------------------------------------Programul principal:-------------------------------------------
# ---------------------------------------------------------------------------------------------------------

max_fitness = []  # vector cu fitnesurile celor elitisti
val_medie_perform = []  # si cu media fitnesurilor

populatie_initiala = populate()

#  MAINUL SI CU RULAREA
for etapa in range(nr_etape):  # rulez pentru un numar de etape dat
    suma_totala_fitness = 0
    x_codificat = []
    fitness = []
    cromozomi = []

    if etapa == 0:
        g.write("Populatia initiala:\n")  # incep sa modelez fisierul ca si evolutie.txt   https://drive.google.com/file/d/18nmiIlpkGTz3QGxRV5HPSal0wWKK0onj/view

    for i in range(dimensiune_populatie):
        cromozom = ""  # initializez un sir vid pentru a crea un cromozom sub forma de string pentru output
        for j in range(lungime_cromozom):  # sau cu join dar imi dadea eroare si am trecut peste "".join(populatie_initiala[i].split())
            cromozom += str(populatie_initiala[i][j])  # "".join(str(ch) for ch in populatie_initiala[i])

        cromozomi.append(cromozom)
        x_codificat.append(get_x(cromozom))
        fitness.append(get_fitness(x_codificat[i]))
        if etapa == 0:
            g.write(f"{i + 1}: {cromozomi[i]} x= {x_codificat[i]} f= {fitness[i]}\n")

    max_fitness.append(max(fitness))
    # val_medie_perform.append(mean(fitness))
    val_medie_perform.append(sum(fitness) / dimensiune_populatie)

    elitist_indice = fitness.index(max(fitness))
    elitist_cromozom = populatie_initiala[elitist_indice].copy()  # salvez cromozomul
    print(elitist_indice, elitist_cromozom)
    populatie_initiala.remove(populatie_initiala[elitist_indice])  # si il sterg, urmeaza sa il adaug din nou la final pentru etapa urmatoare
    fitness.remove(fitness[elitist_indice])
    x_codificat.remove(x_codificat[elitist_indice])
    cromozomi.remove(cromozomi[elitist_indice])

    suma_totala_fitness = sum(fitness)  # suma totala de fitness
    dimensiune_populatie -= 1

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Populatia fara elitist:------------------------------------------
    # -----------------------------------------------------------------------------------------------------------

    if etapa == 0:
        g.write("\nPopulatia fara cromozomul elitist:\n")
        for i in range(dimensiune_populatie):
            g.write(f"{i + 1}: {cromozomi[i]} x= {x_codificat[i]} f= {fitness[i]}\n")

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Calculare probabilitate selectie:--------------------------------
    # -----------------------------------------------------------------------------------------------------------

    probabilitati_selectie = []

    if etapa == 0:
        g.write("\nProbabilitati selectie:\n")
    for i in range(dimensiune_populatie):  # afisez probabilitatile de selectie
        probabilitati_selectie.append(get_select_rate(fitness[i]))
        if etapa == 0:
            g.write(f"Cromozom {i + 1} probabilitate {probabilitati_selectie[i]}\n")

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Definire intervale de selectie:----------------------------------
    # -----------------------------------------------------------------------------------------------------------

    if etapa == 0:
        g.write("\nIntervale probabilitati selectie:\n")

    intervale_de_selectie = [0]
    suma_partiala = 0

    for i in range(dimensiune_populatie):  # afisez intervalele de selectie
        intervale_de_selectie.append(intervale_de_selectie[i] + probabilitati_selectie[i])
        if etapa == 0:
            g.write(str(intervale_de_selectie[i]) + " ")
        # dau append la interval+probabilitatea de selectie
    if etapa == 0:
        g.write(str(intervale_de_selectie[-1]))  # afisarea intervalelor ca in fisierul Evolutie.txt
        g.write('\n')

    # ------------------------------------------------------------------------------------------------------------
    # ------------------------------------------Aflu in ce interval se afla fiecare u:----------------------------
    # ------------------------------------------------------------------------------------------------------------

    gasit_u_interval = []
    populatie_noua = []
    cromozomi_noi = []
    for i in range(dimensiune_populatie):  # cautarea binara a "u"-ului pe intervale
        u = random()  # generez valorile pentru u cu random [0.0,1.0)
        gasit_u_interval.append(caut_bin(intervale_de_selectie, u))  # retin in vector cromozomii gasiti
        populatie_noua.append(populatie_initiala[gasit_u_interval[i]])
        if etapa == 0:
            g.write(f"u= {u}  selectam cromozomul {gasit_u_interval[i] + 1}\n")
    if etapa == 0:
        g.write('\n')

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Afisez populatia noua, dupa ce a fost selectata:-----------------
    # -----------------------------------------------------------------------------------------------------------

    for i in range(dimensiune_populatie):
        cromozom_nou = ""
        for j in range(lungime_cromozom):
            cromozom_nou += str(populatie_noua[i][j])
        cromozomi_noi.append(cromozom_nou)

    if etapa == 0:
        g.write("Dupa selectie:\n")
        for i in range(dimensiune_populatie):  # evidentierea cromozomilor care participa la recombinare
            g.write(f"{i + 1}: {cromozomi_noi[i]} x= {x_codificat[gasit_u_interval[i]]} f= {fitness[gasit_u_interval[i]]}\n")
        g.write('\n')

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Afisez ce cromozomi sunt aleasi cu rata de selectie data:--------
    # -----------------------------------------------------------------------------------------------------------

    if etapa == 0:
        g.write(f"Probabilitatea de recombinare/incrucisare {probabilitate_recombinare}:\n")

    recombinare_indici = []

    for i in range(dimensiune_populatie):
        u = random()  # uniform(0,1) sau asa daca trebuie ca in slideurile de la curs cu [0,1]
        if etapa == 0:
            g.write(f"{i + 1}: {cromozomi_noi[i]} u= {u}")
        if u < probabilitate_recombinare:
            if etapa == 0:
                g.write(f" < {probabilitate_recombinare} participa")
            recombinare_indici.append(i)  # retin indicii celor care merg mai departe
        if etapa == 0:
            g.write('\n')

    lg = len(recombinare_indici)

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Recombinarea:----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------

    # iau cromozomii la rand de la capat la inceput pt recombinare

    if lg % 2 == 0:  # lungime para deci ii luam cate 2 pe toti
        while lg != 0:
            cr1 = deepcopy(choice(recombinare_indici))
            recombinare_indici.remove(cr1)
            cr2 = deepcopy(choice(recombinare_indici))
            recombinare_indici.remove(cr2)
            lg -= 2
            punct_de_rupere = randint(0, lungime_cromozom // 2)  # generez punct de rupere random de la 0 la lungimea cromozomului
            punct_de_rupere2 = randint(lungime_cromozom // 2, lungime_cromozom)
            if etapa == 0:
                g.write(f"\nRecombinare dintre cromozomul {cr1 + 1} si cromozomul {cr2 + 1}:\n{cromozomi_noi[cr1]}  {cromozomi_noi[cr2]} si punct de rupere {punct_de_rupere, punct_de_rupere2}\n")
            cromozomi_noi[cr1], cromozomi_noi[cr2] = cross2(cromozomi_noi[cr1], cromozomi_noi[cr2], punct_de_rupere, punct_de_rupere2)
            if etapa == 0:
                g.write(f"Rezultat   {cromozomi_noi[cr1]}  {cromozomi_noi[cr2]}\n")

    else:  # lungime impara deci luam pe toti cate 2 si pe ultimii 3 toti odata
        if lg != 1:
            while lg != 3:  # daca e 1 nu face nimic
                cr1 = deepcopy(choice(recombinare_indici))
                recombinare_indici.remove(cr1)
                cr2 = deepcopy(choice(recombinare_indici))
                recombinare_indici.remove(cr2)
                lg -= 2
                punct_de_rupere = randint(0, lungime_cromozom // 2)  # generez punct de rupere random de la 0 la lungimea cromozomului
                punct_de_rupere2 = randint(lungime_cromozom // 2, lungime_cromozom)
                if etapa == 0:
                    g.write(f"\nRecombinare dintre cromozomul {cr1 + 1} si cromozomul {cr2 + 1}:\n{cromozomi_noi[cr1]}  {cromozomi_noi[cr2]} si punct de rupere {punct_de_rupere, punct_de_rupere2}\n")
                cromozomi_noi[cr1], cromozomi_noi[cr2] = cross2(cromozomi_noi[cr1], cromozomi_noi[cr2], punct_de_rupere, punct_de_rupere2)
                if etapa == 0:
                    g.write(f"Rezultat   {cromozomi_noi[cr1]}  {cromozomi_noi[cr2]}\n")
            else:  # aici se termina whileul si trebuie sa iau o pereche de 3
                cr1 = recombinare_indici.pop()
                cr2 = recombinare_indici.pop()
                cr3 = recombinare_indici.pop()
                punct_de_rupere = randint(0, lungime_cromozom)
                if etapa == 0:
                    g.write(f"\nRecombinare dintre cromozomul {cr1 + 1} si cromozomul {cr2 + 1} si cromozomul {cr3 + 1}:\n{cromozomi_noi[cr1]}  {cromozomi_noi[cr2]}   {cromozomi_noi[cr3]} si punct de rupere {punct_de_rupere}\n")
                cromozomi_noi[cr1], cromozomi_noi[cr2], cromozomi_noi[cr3] = cross3(cromozomi_noi[cr1], cromozomi_noi[cr2], cromozomi_noi[cr3], punct_de_rupere)
                if etapa == 0:
                    g.write(f"Rezultat   {cromozomi_noi[cr1]}  {cromozomi_noi[cr2]} {cromozomi_noi[cr3]}\n")

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Populatia dupa recombinare:--------------------------------------
    # -----------------------------------------------------------------------------------------------------------

    if etapa == 0:
        g.write("Dupa recombinare:\n")

    x_codificat_nou = []
    fitness_nou = []  # pot sa renunt sa ii calculez aici, e nevoie doar pentru afisare sa fie ca in evolutie.txt

    for i in range(dimensiune_populatie):  # iau x si fitness noi pentru populatia dupa recombinare
        x_codificat_nou.append(get_x((cromozomi_noi[i])))
        fitness_nou.append(get_fitness(x_codificat_nou[i]))

    if etapa == 0:
        for i in range(dimensiune_populatie):
            g.write(f"{i + 1}: {cromozomi_noi[i]} x= {x_codificat_nou[i]} f= {fitness_nou[i]}\n")
        g.write('\n')

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Mutatia:----------------------------------------------
    # -----------------------------------------------------------------------------------------------------------

    if etapa == 0:
        g.write(f"Probabilitate de mutatie pentru fiecare gena {probabilitate_mutatie}\n")
        #g.write("Au fost modificati cromozomii:\n")

    indice_cromozom_mutat = []
    #
    # for i in range(dimensiune_populatie):
    #     for j in range(lungime_cromozom):  # mutatia regulata, iterez prin fiecare gena si am sansa foarte mica sa o schimb
    #         u = random()
    #         if u < probabilitate_mutatie:
    #             populatie_noua[i][j] = abs(populatie_noua[i][j] - 1)
    #             if i not in indice_cromozom_mutat:
    #                 indice_cromozom_mutat.append(i)

    for i in range(dimensiune_populatie):
        u = random()
        if u < probabilitate_mutatie:
            indice_cromozom_mutat.append(i)
    #print(indice_cromozom_mutat)

    for i in range(len(indice_cromozom_mutat)):
        u = randrange(0, lungime_cromozom)
        populatie_noua[indice_cromozom_mutat[i]][u] = abs(populatie_noua[indice_cromozom_mutat[i]][u] - 1)

    #print(indice_cromozom_mutat)
    #f etapa == 0:
        #for i in range(len(indice_cromozom_mutat)):
            #g.write(f"{indice_cromozom_mutat[i] + 1}\n")
        #g.write('\n')

    # -----------------------------------------------------------------------------------------------------------
    # ------------------------------------------Populatia dupa mutatie:----------------------------------
    # -----------------------------------------------------------------------------------------------------------

    # for i in range(dimensiune_populatie):
    #     u = random()
    #     if u < 0.25:
    #         g.write(f"\nModific cromozomul {i}\n")
    #         g.write(f"Valoarea initiala: {populatie_noua[i]} \n")
    #         punct_de_rupere = randint(0, lungime_cromozom // 2)
    #         punct_de_rupere2 = randint(lungime_cromozom // 2, lungime_cromozom)
    #         print(populatie_noua[i])
    #         populatie_noua[i] = flip(populatie_noua[i], punct_de_rupere, punct_de_rupere2)
    #         print(populatie_noua[i])
    #         g.write(f"Pozitiile {punct_de_rupere} si {punct_de_rupere2}\n")
    #         g.write(f"Dupa flip: {populatie_noua[i]}\n")
    # if etapa == 0:
    #     g.write("Dupa mutatie:\n")

    cromozomi_noi = []
    x_codificat_nou = []
    fitness_nou = []

    for i in range(dimensiune_populatie):
        cromozom_nou = ""
        for j in range(lungime_cromozom):
            cromozom_nou += str(populatie_noua[i][j])

        cromozomi_noi.append(cromozom_nou)
        x_codificat_nou.append(get_x((cromozomi_noi[i])))
        fitness_nou.append(get_fitness(x_codificat_nou[i]))

    if etapa == 0:
        for i in range(dimensiune_populatie):
            g.write(f"{i + 1}: {cromozomi_noi[i]} x= {x_codificat_nou[i]} f= {fitness_nou[i]}\n")
        g.write('\n')





    populatie_noua.append(elitist_cromozom)
    populatie_initiala = populatie_noua.copy()
    dimensiune_populatie += 1

    elitist = "".join(str(ch) for ch in elitist_cromozom)
    x_elitst = get_x(elitist)
    fitness_elitist = get_fitness(x_elitst)

    print(elitist, x_elitst, fitness_elitist)
# -----------------------------------------------------------------------------------------------------------
# ------------------------------------------Maximul fitnessului si media pentru fiecare generatei:-----------
# -----------------------------------------------------------------------------------------------------------

g.write("\nEvolutia maximului si valoarea medie a performantei:\n")
for i in range(len(max_fitness)):
    g.write(f"Generatia {i + 1}: Maximul de fitness {max_fitness[i]} <--- --- ---> valoarea medie a generatiei {val_medie_perform[i]}\n")

f.close()
g.close()
