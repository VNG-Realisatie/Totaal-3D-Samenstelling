# Introductie
Deze repository bevat twee JSON bestanden met de configuratie van de voorbeeld dashboards, één voor een procesmanager en één voor een beheerder.

# Afhankelijkheden
De configuratie van de dashboards die in deze JSON bestanden voorkomen zijn afhankelijk van de configuratie van de volgende andere resources in een Azure omgeving:

- Log Analytics-werkruimte.
- Data factory (V2) met geconfigureerd diagnostic settings gekoppeld aan de Log Analytics-werkruimte.
- De pipelines en triggers aangemaakt in de Data factory (V2) resource.
- Applicion Insights voor de Functie-app resource.
- De maatwerk functies zelf moeten ook gepubliceerd zijn.
- Gedeeld dashboard één voor de procesmanager en één voor de beheerder.

# Opmerkingen

Deze JSON bestanden zijn direct uit een Azure dashboard geexporteerd en kunnen alleen in een dashboard resource binnen Azure ook weer worden geimporteerd.

De JSON bestanden zijn niet generiek opgesteld. Benamingen die voorkomen in het JSON bestand moeten overeenkomen met benamingen van resources, pipelines, activiteiten in pipelines, triggers en functies in de Azure omgeving, om goed te kunnen functioneren.

Het is niet nodig om de queries eerst in een Log Analytics-werkruimte te maken, op te slaan en dan toe te voegen aan het dashboard. Het JSON bestand bevat de query die de tabel of grafiek mogelijk maakt in het dashboard.