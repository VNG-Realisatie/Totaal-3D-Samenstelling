# Introductie
Dit project creëert koppelingen tussen systeem onderdelen van de T3D Keten, waar standaard functionaliteit van Azure Data Factory niet toereikend is. 
Dit project is geschreven specifiek voor Azure Functions, maar onderdelen hiervan kunnen hergebruikt worden voor andere doeleinden.

# Afhankelijkheden
* Azure Opslag (Alle functies): deze dient u zelf op te zetten
* OGC CityGML XSD specificatie (Validatie)
Mogelijk om toegang te krijgen: 
* FutureInsight API voor BIM verwerking (TransformBIM)
* FutureInsight S3 bucket (SendDataToBeheertool)


# Overzicht functionaliteiten
* SendDataToBeheertool (POST) - verstuurt data naar proefomgeving database bij Future Insight
* TransformBIM (POST)- verstuurt BIM modellen naar BIM transformatie service en slaat modellen op bij de BIM service van Future Insight
* UploadData (POST, PUT) - ontvangt data en slaat het op met een serie van metadata velden
* Validatie (POST) - valideert data 
# Aan de slag
1. Volg [deze handleiding](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?source=recommendations&tabs=csharp) om je ontwikkelomgeving te voorbereiden
    - Er is een opslag (Azure Storage) nodig om data te versturen. 
2. Maak een copie van deze repository met git (git clone) en open folder _MaatwerkcodeAzureFunctions_ als Visual Studio project
3. Neem contact op met [Geodesk den Haag](mailto:geodesk@denhaag.nl) voor toegangstokens (zie ook kopje Toegangstokens)
4. Voor lokale tests, dient u om de opgevraagde toegangstokens toe te voegen aan een bestand local.settings.json