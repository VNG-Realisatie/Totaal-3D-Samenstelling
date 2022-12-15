# Introductie
Data orkestratie is een proces waarbij gegevens van verschillende gegevensopslaglocaties worden gehaald, gecombineerd en georganiseerd. In deze repository vindt u de implementatie van data orkestratie toepassingen in Azure Data Factory binnen het programma Totaal-3D. 
# Afhankelijkheden
Binnen Azure:
* Azure Blob Storage: data opslag en structuur ivm triggers
* Azure Key Vault: inloggegevens opslag (mogelijk om links zelf te vervangen)

Herbruikbaar vanuit het programma (stuur een email naar [geodesk@denhaag.nl](mailto:geodesk@denhaag.nl) voor tokens):
* Azure Functions: maatwerk code voor validatie, ingestie en doorsturing van data naar externe services
* Data verwerking API's: BIM, LiDAR, LiDAR&BIM
* Rioned API 
# Aan de slag
Voordat u begint met adoptie van deze scripts, adviseren wij om deze gratis [leerpad van Microsoft te volgen](https://learn.microsoft.com/en-us/training/paths/data-integration-scale-azure-data-factory/).
Daarna is het mogelijk om deze bestaande repository rechtstreeks in Azure Data Factory te importeren. Hiervoor volg [deze tutorial](https://craigporteous.com/how-to-move-your-git-repo-to-another-azure-data-factory-and-vice-versa/).

# Opmerkingen
Deze repository is een mogelijke startpunt voor eigen implementaties van data orkestratie/workflow automatie. De logica achter elke data pipeline kan ook in andere software reproduceerd worden (b.v. FME server, Apache Airflow). Hierbij verwijzen wij u graag naar onze marktanalyse en product documentatie op Alchemio.