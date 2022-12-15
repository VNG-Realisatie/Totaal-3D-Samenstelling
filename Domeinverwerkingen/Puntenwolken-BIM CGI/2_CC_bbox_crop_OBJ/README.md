### Crop de BIM in de bounding box van de PC
Crop de BIM (OBJ) in de bounding box die de PC bevat.

### UITLEG
De BIM (OBJ) wordt gecropped in de bounding box die de PC bevat om de descripanties tussen BIM en PC te kunnen berekenen.

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

Let op: als de file calculate_boundbox.py zonder docker wordt aangeroepen moet bij de parameter --ccpath de locatie van de CloudCompare installatie meegegeven worden.

# Run docker build
Open Powershell in de map 2_CC_bbox_crop_OBJ

`docker build . -t bboxcropobj:latest`

# Run docker image
Zet de .obj en PC bestanden in de map 2_CC_bbox_crop_OBJ/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.
De eerste parameter is de puntenwolk en de tweede parameter is het BIM model in OBJ formaat.

`docker run -v {DATA_PATH}:/data bboxcropobj:latest --pcfile data/{inputfile PC} --objfile data/{inputfile OBJ}`

voorbeeld:

`docker run -v $pwd/data:/data bboxcropobj:latest --pcfile data/inputfile.las --objfile data/inputfile.obj`
