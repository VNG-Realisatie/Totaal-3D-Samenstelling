### Bereken de descripanties tussen de PC en de BIM.
Bereken de afstanden (descripanties) tussen de PC en de BIM (OBJ).

### UITLEG
De afstanden tussen de PC en de BIM (OBJ) worden berekend om te worden geïnterpreteerd als de descripanties ertussen.

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

# Run docker build
Open Powershell in de map 3_CC_c2mdist

`docker build . -t c2mdist:latest`

# Run docker image
Zet de .obj en PC bestanden in de map 3_CC_c2mdist/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.
De eerste parameter is de puntenwolk en de tweede parameter is het BIM model in OBJ formaat.

`docker run -v {DATA_PATH}:/data c2mdist:latest data/{inputfile PC} data/{inputfile OBJ}`

voorbeeld:

`docker run -v $pwd/data:/data c2mdist:latest data/inputfile.las data/inputfile.obj`
