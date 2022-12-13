### Mesh area volume
Rekent vloeroppervlak en volume uit per input mesh

### UITLEG
Vanuit de verschillende meshes per kamer wordt een berekening gedaan van het volume en het vloeroppervlak. Hiervoor wordt eerst de mesh gerepareerd op gaten om het volume uit te rekenen.
Daarna wordt met behulp van de normals van de vlakken een selectie gemaakt van de vlakken die vloeroppervlak zijn. Hier wordt tenslotte het oppervlakte van bepaald.

### GEBRUIK
Eerst moet een docker image gemaakt worden en daarna kan deze aangeroepen worden vanuit een lokale map

# Build docker image
docker build -f Dockerfile . -t mesh-area-volume:latest

# Run docker image 
docker run -v {DATA_PATH}:/usr/src/app/data mesh-area-volume:latest --inpath data/ --outpath data/{OUTPUT_PATH}

voorbeeld:
docker run -v $pwd/data:/usr/src/app/data mesh-area-volume:latest --inpath data/ --outpath metrics/
