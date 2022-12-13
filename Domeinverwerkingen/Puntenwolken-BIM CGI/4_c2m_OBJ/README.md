### Discrepanties tussen PC en IFC als OBJ.
De gedetecteerde discrepanties tussen PC en BIM (IFC) worden omgezet in objecten.

### UITLEG
De discrepanties tussen PC en BIM (IFC) zijn geïdentificeerd als punten in de PC. 
Die discrepanties worden eerst gesegmenteerd en voor elke segment punten wordt de convex hull berekend en geexporteerd als mesh. 

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

Let op: als de file c2m_obj.py zonder docker wordt aangeroepen moet bij de parameter --ccpath de locatie van de CloudCompare installatie meegegeven worden.

# Run docker build
Open Powershell in de map 4_c2m_OBJ

`docker build . -t c2m-obj:latest`

# Run docker image
Zet de PC bestand in de map 4_c2m_OBJ/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

`docker run -v {DATA_PATH}:/data c2m-obj:latest --pcfile data/{inputfile PC}

voorbeeld:

`docker run -v $pwd/data:/data c2m-obj:latest --pcfile data/inputfile.las
