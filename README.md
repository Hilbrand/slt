# Stemlokalentoegankelijkheid

Deze repository bevat de broncode van de webpagina waarop inzicht wordt gegeven in de toegankelijkheid van stemlokalen informatie
zoals door gemeenten is aangeleverd aan de website https://WaarIsMijnStemlokaal.nl

De webpagina is te bezoeken op https://hilbrand.github.io/slt

De webpagina maakt gebruik van voorbewerkte gegevens, zodat de website zonder backend kan werken.
Deze repository bevat ook de scripts om deze bestanden aan te maken.
Voor de geometrieën van de gemeenten is gebruik gemaakt van de CBS data.
Het script om het gemeenten.geojson bestand te maken ontbreekt nog in deze repository.

## Nieuwe verkiezing toevoegen

Om een nieuwe verkiezing toe te voegen dienen in principe 2 aanpassingen gemaakt te worden.
In de typescript moet de verkiezing in [src/types.ts](src/types.ts) worden toegevoegd.
Bij voorkeur wordt ook `DEFAULT_VERKIEZING` aangepast naar de nieuwste verkiezing.

Daarnaast moet de GitHub action geconfigureerd en geactiveerd worden.
Voor activatie moet de regel van de cron in [./github/workflows/ververs.yaml](./github/workflows/ververs.yaml) uit commentaar worden gehaald.
Daarnaast dienen de volgende env variable in het `ververs.yaml` bestand aangepast te worden:

| variable naam                | omschrijving                                                                |
|------------------------------|-----------------------------------------------------------------------------|
| `VERKIEZING`                 | code voor de verkiezing, zoals in de typescript ook gebruikt. b.v. `tk2025` |
| `RESOURCE_ID`                | naam van het data bestand van https://WaarIsMijnStemlokaal.nl               |
| `NIET_DEELNEMENDE_GEMEENTEN` | Bestand met niet deelnemende gemeenten van https://WaarIsMijnStemlokaal.nl  |

Na de verkiezingen moet de cron job in de GitHub action weer in commentaar gezet, anders blijft deze data ophalen.

## Ontwikkelen en bouwen van de broncode

### Aanbevolen ontwikkelomgeving (IDE)

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Project opzet

```sh
npm install
```

### Compileer en automatisch herladen tijdens ontwikkelen

```sh
npm run dev
```

### Compileren en verkleinen voor productie

```sh
npm run build
```

### Code stijl controle met Lint [ESLint](https://eslint.org/)

```sh
npm run lint
```

### Code stijl automatisch aanpassen

```sh
npx prettier -w src test
```

### Test draaien

```sh
npx vitest
```

## Licentie

Copyright 2025 Stemlokalentoegankelijkheid bijdragers

In licentie gegeven krachtens de EUPL, Versie 1.2 of – zodra ze zullen worden goedgekeurd door de
Europese  Commissie - latere versies van de EUPL (De "Licentie");

U mag dit werk alleen gebruiken in overeenstemming met de licentie.
U kunt een kopie van de licentie verkrijgen op:

https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

Tenzij vereist door de toepasselijke wetgeving of schriftelijk overeengekomen, wordt software die onder de Licentie wordt gedistribueerd, gedistribueerd op een "AS IS"-basis,
ZONDER GARANTIES OF VOORWAARDEN VAN WELKE AARD DAN OOK, expliciet of impliciet.
Zie de Licentie voor de specifieke taal waarin de machtigingen en beperkingen onder de Licentie van toepassing zijn.
