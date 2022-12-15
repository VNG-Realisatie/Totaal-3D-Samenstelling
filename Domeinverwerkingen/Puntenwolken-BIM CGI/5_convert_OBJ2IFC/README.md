### Converteer OBJ naar IFC
Converteer .obj naar .ifc-bestand.

### UITLEG
De discrepantie vlakken als meshes tussen PC en BIM (IFC) worden omgezet van .obj naar .ifc-bestand.  

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

Let op: als de file obj2ifc.py zonder docker wordt aangeroepen moet bij de parameter --ccpath de locatie van de CloudCompare installatie meegegeven worden.

# Run docker build
Open Powershell in de map 5_convert_OBJ2IFC

`docker build . -t obj2ifc:latest`

# Run docker image
Zet de OBJ bestand in de map 5_convert_OBJ2IFC/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

`docker run -v {DATA_PATH}:/data obj2ifc:latest --objfile data/{inputfile OBJ}

voorbeeld:

`docker run -v $pwd/data:/data obj2ifc:latest --objfile data/inputfile.obj
