### Discrepanties tussen IFC en PC.
Objecten identificeren die in BIM (IFC) zijn maar missen in PC.

### UITLEG
De PC wordt gesubsampled om het proces te versnellen.
Dan wordt de BIM (IFC) gecropped en alleen de objecten worden bewaard die in BIM (IFC) zijn maar missen in PC om de descripanties tussen BIM en PC te identificeren.

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

Let op: als de file ifc_discrep.py zonder docker wordt aangeroepen moet bij de parameter --ccpath de locatie van de CloudCompare installatie meegegeven worden.

# Run docker build
Open Powershell in de map 6_IFC_discrep

`docker build . -t ifcdiscrep:latest`

# Run docker image
Zet de .ifc en PC bestanden in de map 6_IFC_discrep/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.
De eerste parameter is de puntenwolk en de tweede parameter is het BIM model in IFC formaat.

`docker run -v {DATA_PATH}:/data ifcdiscrep:latest --pcfile data/{inputfile PC} --ifcfile data/{inputfile IFC}`

voorbeeld:

`docker run -v $pwd/data:/data ifcdiscrep:latest --pcfile data/inputfile.las --ifcfile data/inputfile.ifc`
