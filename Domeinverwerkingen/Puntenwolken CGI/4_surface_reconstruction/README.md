### Surface reconstruction
Detecteert vlakken en polygonen vanuit puntenwolken naar een mesh

### UITLEG
De reconstructie van het polygoon wordt gedaan met een functie uit het library pakket van CGAL. De functie heet "Polygonal Surface Reconstruction". 
Dit algoritme gaat eerst vlakken detecteren uit de puntenwolk met behulp van RANSAC. Daarna worden al deze vlakken met elkaar gekruist zodat er snijlijnen tussen de vlakken ontstaan. 
Van al deze snijlijnen worden vervolgens de segmenten geselecteerd die het beste voldoen aan de waarden van de puntenwolk. De beste segmenten worden geselecteerd tot een sluitend 3d model. 
Hier kan aan drie parameters gesleuteld worden namelijk fitting, coverage en complexity. We hebben deze waarden nu empirisch vastgesteld op 0.25, 0.45 en 0.3 respectievelijk.

Voor meer informatie over het algoritme zie: https://doc.cgal.org/latest/Polygonal_surface_reconstruction/index.html

### GEBRUIK
Eerst moet een docker image gemaakt worden en daarna kan deze aangeroepen worden vanuit een lokale map

# Build docker image
Open Powershell in de map 4_surface_reconstruction

docker build -f Dockerfile . -t surface-reconstruction:latest

# Run docker image 
Zet de .ply bestanden uit stap 3 in de map 4_surface_reconstruction/data en gebruik het voorbeeld, of pas de locatie in onderstaand commando aan.

docker run -v {DATA_PATH}:/usr/myapp/data surface-reconstruction:latest {inputfile} {outputdir} {outputfilename} var1 var2 var3

voorbeeld:
docker run -v $pwd/data:/usr/myapp/data surface-reconstruction:latest data/inputfile.ply data/out inputfile.ply 0.25 0.45 0.3

voorbeeld voor meerdere rooms:
For ($i=1; $i -le 16; $i++){ docker run -d -v $pwd/data:/usr/myapp/data surface-reconstruction:latest data/room_${i}.ply data/ room_${i}_out 0.25 0.45 0.3 }

