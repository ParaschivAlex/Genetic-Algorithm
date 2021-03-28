# Genetic-Algorithm
A genetic algorithm for determining the maximum of a positive function

Enunt: https://docs.google.com/document/d/1kU-W9St2Ac26ngh7eKq7ym1Vk2EN0PYEVlKUL1pOCGg/edit

Implementaţi un algoritm genetic pentru determinarea maximului unei funcţii pozitive pe un domeniu dat (funcţia se va fixa în cod) 
Date de intrare:
dimensiunea populaţiei
domeniul de definiţie al funcţiei
parametri pentru functia de maximizat (coeficientii polinomului de grad 2)
precizia cu care se lucrează (cu care se discretizează intervalul)
probabilitatea de recombinare (crossover, încrucişare)
probabilitatea de mutaţie
numărul de etape ale algoritmului

Ieşire:
Un fişier text sugestiv care evidenţiază operaţiile din prima etapă a algoritmului, (de exemplu fişierului Evolutie.txt (obţinut pentru funcţia –x2+x+2, domeniul [-1, 2], dimensiunea populaţiei 20, precizia 6, probabilitatea de recombinare 0.25, probabilitatea de mutaţie 0.01 şi 50 de etape))
Bonus: Interfaţă grafică sugestivă, care evidenţiază evoluţia algoritmului

În fişier sunt scrise 
populaţia iniţială sub forma 
i: reprezentare cromozom x = valoarea corespunzătoare cromozomului în domeniul de definiţie al funcţiei f =valoarea corespunzătoare cromozomului (f(Xi)) 
probabilităţile de selecţie pentru fiecare cromozom

probabilităţile cumulate care dau intervalele pentru selecţie 
evidenţierea procesul de selecţie, care constă în generarea unui număr aleator u uniform pe [0,1) şi determinarea intervalului [qi, qi+1) căruia aparține acest număr; corespunzător acestui interval se va selecta cromozomul i+1. Procesul se repetă până se selectează numărul dorit de cromozomi. Cerinţă: căutarea intervalului corespunzător lui u se va face folosind căutarea binară. 
evidenţierea cromozomilor care participă la recombinare 
pentru recombinările care au loc se evidenţiază perechile care participă la recombinare, punctul de rupere generat aleator precum şi cromozomii rezultaţi în urma recombinării (sau, după caz, se evidenţiază tipul de încrucişare ales)
populaţia rezultată după recombinare
populaţia rezultată după mutaţii
pentru restul generaţiilor (populaţiilor din etapele următoare) se vor afişa doar valoarea maximă  și valoarea medie a performanței .
