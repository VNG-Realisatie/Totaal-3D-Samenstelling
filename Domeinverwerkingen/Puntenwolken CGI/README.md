### Introductie
In deze repository staan alle scripts die zijn ontwikkeld voor het project Puntenwolken verwerking voor de Gemeente Den Haag. 
Het puntenwolken zijn afkomstig uit het vergunningsverleningsproces. 
Het doel van deze scripts is het effectief kunnen werken met de puntenwolken bestanden, met focus op puntenwolken van bestaande gebouwen m.b.t. onroerende zaken en het beoordelen van een aanvraag voor een bouwvergunning

De ontwikkelde verwerking bestaat uit vijf verschillende stappen:
- Het preprocessing van de puntenwolk om deze geschikt te maken voor de verschillende algoritmes om de ruimtes te identificeren en oppervlakten te berekenen
- Het splitsen van verschillende verdiepingen vanuit de puntenwolken
- Het splitsen van verschillende kamers per verdiepingen
- Het construeren van objecten per kamer door middel van surface reconstruction
- Het uitrekenen van vloeroppervlak en volume per kamer

### Gebruik
Deze repository bestaat uit vijf verschillende mappen per stap en dienen achtereenvolgens uitgevoerd te worden.

# Installatie
Voor het uitvoeren van de stappen is docker nodig. 
Voor het visualiseren van puntenwolken wordt CloudCompare aangeraden en voor het visualiseren van de resultaten meshes wordt Meshlab aangeraden. 

# Input
Input is een puntenwolk bestand (.las/.laz/.ply) bestaanden uit een ingescande woning. Eisen aan de puntenwolk staan beschreven in het onderzoeksrapport van het project.
Belangrijkste is dat de kamers volledig zijn ingescand met vier muren, een plafond en een vloer en dat er geen punten in de puntenwolk zitten die zich buiten de woning bevinden (bijvoorbeeld gescand door de ramen naar buiten). 

# Output
TBD:
output is een .obj file van de geconstrueerde kamers uit de puntenwolk. Daarnaast meerdere text bestandjes van de afmetingen per kamer.



