### Room detection
Detecteert verschillende kamers uit de puntenwolk (per verdieping)

### UITLEG
Vanuit de puntenwolk per verdieping wordt opnieuw de plafondhoogte bepaald om vervolgens een plakje uit de puntenwolk te knippen 10 centimeter onder dit plafond met een dikte van 20 centimeter.
Deze waardes zijn bepaald om hiermee zoveel mogelijk de muren boven de deuren mee te nemen.
Vanuit dit plakje puntenwolk wordt een 2d weergave gemaakt waar met behulp van de 'distance transform' methode verschillende ruimtes worden gedetecteerd. 
De resulterende 2d splitsing van de ruimtes wordt gebruikt om de puntenwolk op te knippen in verschillende kamers. 

### GEBRUIK
Eerst moet een docker image gemaakt worden en daarna kan deze aangeroepen worden vanuit een lokale map

# Build docker image
Open Powershell in de map 3_room_detection

docker build -f Dockerfile . -t room-detection:latest

# Run docker image 
Zet de .ply bestanden uit stap 2 in de map 3_room_detection/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

docker run -v {DATA_PATH}:/usr/src/app/data room-detection:latest --inpath data/ --outpath data/{OUTPUT_PATH} 

voorbeeld:
docker run -v $pwd/data:/usr/src/app/data room-detection:latest --inpath data/ --outpath data/rooms/ 