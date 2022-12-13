### Split floors
Split puntenwolk in verschillende verdiepingen

### UITLEG
Er wordt gebruik gemaakt van een histogram over de z-as van de puntenwolk. Hiermee worden pieken gedetecteerd die onstaan door de grote hoeveelheid punten op de plafonds en vloeren.
Met de waardes van deze plafonds en vloeren wordt de puntenwolk vervolgens in stukken geknipt.
Bij woningen met schuine daken, plafonds op verschillende hoogtes of vloeren op verschillende hoogtes kan dit in de huidige versie nog problemen opleveren. 

### GEBRUIK
Eerst moet een docker image gemaakt worden en daarna kan deze aangeroepen worden vanuit een lokale map.

# Build docker image
Open Powershell in de map 2_split_floors

docker build -f Dockerfile . -t split-floors:latest

# Run docker image 
Zet het .ply bestand uit stap in de map 2_split_floors/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

docker run -v {DATA_PATH}:/usr/src/app/data split-floors:latest --infile data/{INPUT_FILE} --outpath data/{OUTPUT_PATH}/

voorbeeld:
docker run -v $pwd/data:/usr/src/app/data split-floors:latest --infile data/inputfile.ply --outpath data/floors/ 