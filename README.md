# ITH Snake

För att använda programmet. 1) spara hem projektet i en fil, 
2) Genom terminalen navigera till projektmappen var du sparade 
projektet. 3) Kör projektet genom py Game.py (Main-filen ligger sparad
i Game.py).

När du startar spelet, så möts du av en meny. 
Här kan du ändra svårighetsgrad, bestämma om du vill spela med eller utan 
väggar eller hypotetiskt kolla highscore-listan(inte implementerad, palla xD).

När du väl är redo, så kan du starta spelet genom att trycka på "start. 
Du kommer då till spelplanen, men allt är står stilla. Det är för att spelet
väntar på input från spelaren före masken drar iväg. 

Du styr masken med WASD(är du inte bekant med dessa tangenter så beklagar jag
men nu är det så). W = Norr, A=Väster, S=Söder.

Spelet går ut på att göra ormen så stor som möjligt. Detta genom att äta. 
Där finns två olika sorters mat -- grön och röd. 

Den gröna maten ger spelaren 1 poäng(justerat enligt svårighetsgrad och nivå) 
samt ökar maskens längd.

För var 5:e "vanlig" mat man äter kommer att öka spelhastigheten. Men även "spawna"
röd specialmat. Denna ger mycket mera poäng(skalar med svårighetsgrad) men om man 
väljer att äta denna maten så kommer spelet även att bli svårare på andra oförutsägbara
sätt. 

Specialmaten försvinner också efter en viss tid ifall man inte hinner äta den, så 
bestäm dig snabbt! ;) 

Är det så att man inte riktigt vill spela, men ändå inte riktigt vill spela. Så kan man bara test 
trycka på "G" när man är inne i spelet för att se vad som händer. :> 
