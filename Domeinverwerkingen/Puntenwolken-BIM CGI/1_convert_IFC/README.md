### Converteer IFC naar OBJ
Converteer BIM van .ifc naar .obj-bestand.

### UITLEG
De BIM in .ifc wordt geconverteerd naar .obj om te gebruiken als invoer voor CloudCompare.

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

# Run docker build
Open Powershell in de map 1_convert_IFC

`docker build . -t ifcconvert:latest`

# Run docker image
Zet de .ifc bestand in de map 1_convert_IFC/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

`docker run -v {DATA_PATH}:/data ifcconvert:latest data/{inputfile}`

voorbeeld:

`docker run -v $pwd/data:/data ifcconvert:latest data/inputfile.ifc`
