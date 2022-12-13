### Preprocessing puntenwolk
Voorbewerking stappen voor de puntenwolk om geschikt te maken als input

### UITLEG
De voorbewerking bestaat uit het subsamplen van de puntenwolk om de hoeveelheid datapunten te reduceren voor verdere verwerking.
Daarnaast wordt er Statistical Outlier Removal (SOR) uitgevoerd. 

### GEBRUIK
Eerst moet een docker image gemaakt worden. Daarna kan deze aangeroepen worden vanuit een lokale map.

# Docker installeren
Installeer docker. De windows installer is hier te vinden: https://docs.docker.com/desktop/windows/install/
Start docker desktop. De daemon runt als het balkje linksonder groen is.

# Run docker build
Open Powershell in de map 1_preprocessing.

docker build . -t cloudcompare:latest

De build is succesvol als er "Building x.x s (20/20) FINISHED" staat. 
Let op: Deze build kan een momentje duren (ongeveer half uur).
# Run docker image 
docker run -v {DATA_PATH}:/data -v cloudcompare:latest /data/{INPUT_FILE}

voorbeeld:
docker run -v ${pwd}/pipeline_data:/data cloudcompare:latest /data/PointCloud_cs2_dec_x-y-z-unixtime12precision.txt

De run is succesvol als dit resultaat te zien is:
File '/data//{INOUT_FILE}.ply' saved successfully
Processed finished in xxx.xx s.

Het resultaat is te vinden in dezelfde map als het inputbestand.

# Note
de scripts (*.sh) files moeten LF in plaats van CRLF zijn. Git slaat ze op in CRLF