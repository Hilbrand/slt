import json
import sys
import os
from datetime import date
import subprocess

LB = 'Toegankelijk voor mensen met een lichamelijke beperking'
legacyToilet = False

toegankelijkheids_categorieen = [
    LB,
    'Toegankelijke ov-halte',
    'Gehandicaptentoilet',  # Dit was naam voor gr2026, voor ODS versie 1.7
    'Toilet',
    'Host',
    'Prikkelarm',
    'Geleidelijnen',
    'Kandidatenlijst in braille',
    'Kandidatenlijst met grote letters',
    'Stemmal met audio-ondersteuning',
    'Gebarentolk (NGT)',
    'Gebarentalig stembureaulid (NGT)',
    'Akoestiek geschikt voor slechthorenden',
    'Prokkelduo',
    # Aanvullend
#    'Niet verplichte toegankelijkheden',
]

toegankelijkheids_categorieen_kort = {
    LB                                                       : 'lb',
    'Toegankelijke ov-halte'                                 : 'ov',
    'Gehandicaptentoilet'                                    : 'tt',
    'Toegankelijk Toilet'                                    : 'tt',
    'Genderneutraal Toilet'                                  : 'gt',
    'Toilet'                                                 : 'to',
    'Host'                                                   : 'ho',
    'Prikkelarm'                                             : 'pa',
    'Geleidelijnen binnen'                                   : 'gi',
    'Geleidelijnen buiten'                                   : 'gu',
    'Kandidatenlijst in braille'                             : 'kb',
    'Kandidatenlijst met grote letters'                      : 'kg',
    'Stemmal met audio-ondersteuning'                        : 'sa',
    'Gebarentolk'                                            : 'gtolk',
    'Gebarentolk (NGT) op locatie'                           : 'gl',
    'Gebarentolk (NGT) op afstand'                           : 'ga',
    'Gebarentalig stembureaulid (NGT)'                       : 'gs',
    'Akoestiek geschikt voor slechthorenden'                 : 'as',
    'Prokkelduo'                                             : 'pd',
     'Niet verplichte toegankelijkheden'                     : 'nv',
}

# lb is verplicht
# Voor toilet wordt alleen toilet (to) of voor 2026 (tt) meegeteld omdat tt en gt overlappen met to.
# Voor gebarentolk (gl) en (ga) worden geteld via 'gtolk'. gtolk telt of op locatie of op afstand samengevoegd.
niet_verplichte_niet_meetellen = set(['lb', 'tt', 'gt', 'gl', 'ga'])
niet_verplichte_niet_meetellen_voor_2026 = set(['lb', 'to', 'gt', 'gl', 'ga'])

uitzonderingen = {
  'binnen',
  'buiten',
}

def set_aanwezigheid(gemeente, categorie, aanwezigheid):
  stc = toegankelijkheids_categorieen_kort[categorie]
  if stc not in gemeente:
      gemeente[stc] = {}
  if aanwezigheid not in gemeente[stc]:
      gemeente[stc][aanwezigheid] = 0
  gemeente[stc][aanwezigheid] += 1

def data_aanwezigheid(aanwezigheid):
  match aanwezigheid:
    case 'ja':
      v = 'j'
    case 'nee':
      v = 'n'
    case _:
      v = aanwezigheid
  return v

def set_value(gemeente, categorie, value):
  if value in uitzonderingen:
    tc =  categorie + ' ' + value
    v = 'j'
    if value == 'binnen':
      set_value(gemeente, categorie + ' buiten', 'nee')
    if value == 'buiten':
      set_value(gemeente, categorie + ' binnen', 'nee')
  elif value == 'buiten en binnen':
    set_value(gemeente, categorie + ' binnen', 'ja')
    set_value(gemeente, categorie + ' buiten', 'ja')
    return
  elif categorie == 'Geleidelijnen':
    set_value(gemeente, categorie + ' binnen', value)
    set_value(gemeente, categorie + ' buiten', value)
    return
  elif categorie == 'Gebarentolk (NGT)':
    aanwezigheid = data_aanwezigheid(value)
    ol = value == 'op locatie'
    oa = value == 'op afstand'
    set_aanwezigheid(gemeente, 'Gebarentolk (NGT) op locatie', 'j' if ol else 'n' if oa else aanwezigheid)
    set_aanwezigheid(gemeente, 'Gebarentolk (NGT) op afstand', 'j' if oa else 'n' if ol else aanwezigheid)
    set_aanwezigheid(gemeente, 'Gebarentolk', 'j' if oa or ol else aanwezigheid)
    return
  elif value == 'ja, toegankelijk toilet' or value == 'Gehandicaptentoilet':
    set_aanwezigheid(gemeente, 'Toegankelijk Toilet', 'j')
    set_aanwezigheid(gemeente, 'Genderneutraal Toilet', 'j')
    set_aanwezigheid(gemeente, 'Toilet', 'j')
    return
  elif value == 'ja, genderneutraal toilet':
    set_aanwezigheid(gemeente, 'Toegankelijk Toilet', 'n')
    set_aanwezigheid(gemeente, 'Genderneutraal Toilet', 'j')
    set_aanwezigheid(gemeente, 'Toilet', 'j')
    return
  elif categorie == 'Toilet':
    aanwezigheidToilet = data_aanwezigheid(value)
    aanwezigheidAndere = 'n' if value == 'ja' else aanwezigheidToilet
    set_aanwezigheid(gemeente, 'Toegankelijk Toilet', aanwezigheidAndere)
    set_aanwezigheid(gemeente, 'Genderneutraal Toilet', aanwezigheidAndere)
    set_aanwezigheid(gemeente, 'Toilet', aanwezigheidToilet)
    return
  else:
    tc = categorie
    v = data_aanwezigheid(value)
  set_aanwezigheid(gemeente, tc, v)

#
# Telt de toegankelijkheden en groepeert per gemeente.
#
def tel_toegankelijkheden(json_data):
  try:
    # Extract the records array
    records = json_data['result']['records']

    # Groepeer records op CBS gemeentecode
    data = { 'resource_id': json_data['result']['resource_id'], 'data' : {} }
    gemeentecode_groups = data['data']
    keys = {}
    for record in records:
      code = record.get('CBS gemeentecode')[2:]

      if code not in gemeentecode_groups:
        gemeentecode_groups[code] = {'g': record.get('Gemeente')}

      for tc in toegankelijkheids_categorieen:
        if tc in record:
          value = record.get(tc, '')
          set_value(gemeentecode_groups[code], tc, value)
          keys[value] = 1
    print("Alle records geteld.")
    return data
  except Exception as e:
      return f'Error processing the JSON: {str(e)}'

#
# Transformeer data van map naar gemeente naam, totaal en toegankelijkeden in array per gemeente code.
#
def transform(json):
  gemeenten = {}
  data = json['data']
  for code in data:
    gem = ""
    toegs = {}
    totaal = 0
    # {'gemeente code': values}
    for c in data[code]:
       if c == 'g':
         gem = data[code][c]
       else:
         toegs[c] = data[code][c]
         cat_totaal = sum(toegs[c].values())
         if cat_totaal > totaal:
           totaal = cat_totaal
    gemeenten[code] = [gem, totaal, toegs]
  print("Gegevens getransformeerd en totalen per gemeente geteld.")
  json['data'] = gemeenten

#
# Tel per gemeente van de niet verplichte toegankelijkheden de totalen.
#
def niet_verplicht_totaal(json):
  gemeenten = json['data']
  niet_meetellen = niet_verplichte_niet_meetellen_voor_2026 if legacyToilet else niet_verplichte_niet_meetellen
  for code in gemeenten:
    gemeente = gemeenten[code]
    allTgStates = gemeente[2]
    totalTg = {}
    for tgName in allTgStates:
      if not tgName in niet_meetellen:
        for state in allTgStates[tgName]:
          bewaarState = state
          if bewaarState not in totalTg:
            totalTg[bewaarState] = 0
          totalTg[bewaarState] += allTgStates[tgName][state]
    if totalTg == 0:
      print(gemeente[0])
    allTgStates['nv'] = totalTg
  print("Niet verplichte toegankelijkheden totalen geteld.")

def filter_gtolk(json):
  gemeenten = json['data']
  for code in gemeenten:
    # ['<gemeente naam>', 'stemlokalen', {'<tg>': {}}]
    gemeente = gemeenten[code]
    del gemeente[2]['gtolk']

#
# Tel de toegankelijkheden op landelijk nivo.
#
def landelijke_totalen(json):
  gemeenten = json['data']
  totaalStemlokalen = 0
  toegsTotaal = {}
  for code in gemeenten:
    # ['<gemeente naam>', 'stemlokalen', {'<tg>': {}}]
    gemeente = gemeenten[code]
    totaalStemlokalen += gemeente[1]
    # {'<tgName>': {}}}
    allTgStates = gemeente[2]
    for tgName in allTgStates:
      # Negeer samengetelde gtolk, wordt alleen gebruikt om som te bepalen
      if tgName == 'gtolk':
        continue
      if tgName not in toegsTotaal:
         toegsTotaal[tgName] = {}
      totalTg = toegsTotaal[tgName]
      # { 'state': <number>, ....}
      for state in allTgStates[tgName]:
        if state not in totalTg:
          totalTg[state] = 0
        totalTg[state] += allTgStates[tgName][state]
  json['nationaal'] = ['nationaal', sum(toegsTotaal['lb'].values()), toegsTotaal]
  print("Gegevens op landelijk nivo verzameld.")

#
# Test of key in values en zo ja of de waarde > 0 is.
#
def groter_nul(values, key):
  return key in values and values[key] > 0

#
# Als key niet in values set 1, ander verhoog waarde in values met 1.
#
def increment(values, key):
  if (key not in values):
    values[key] = 1
  else:
    values[key] += 1

#
# Maakt json object met per toegankelijkheid geteld bij hoeveel gemeenten deze tenminste 1 keer
# voor komt.
#
def tenminste_een(json):
  gemeenten = json['data']
  totaalGemeenten = 0
  toegsTotaal = {}
  for code in gemeenten:
    # ['<gemeente naam>', 'stemlokalen', {'<tg>': {}}]
    gemeente = gemeenten[code]
    totaalGemeenten += 1
    # {'<tgName>': {}}}
    allTgStates = gemeente[2]
    for tgName in allTgStates:
      # Als nv gebruik dan totaal * aantal toegankelijkheden - 2 (lb en nv tellen niet mee).
      if tgName == 'nv':
        noCount = gemeente[1] * (len(allTgStates) - 2)
      else:
        noCount = gemeente[1]
      if tgName not in toegsTotaal:
          toegsTotaal[tgName] = {}
      states = allTgStates[tgName]
      if groter_nul(states, 'j'):
        increment(toegsTotaal[tgName], 'j')
      elif 'n' in states and states['n'] == noCount:
        increment(toegsTotaal[tgName], 'n')
      else:
        increment(toegsTotaal[tgName], '')
  json['atLeastOne'] = ['atLeastOne', sum(toegsTotaal['lb'].values()), toegsTotaal]
  print("Gegevens van tenminste 1 aangemaakt.")

#
# Voeg gemeenten waar geen verkiezing is toe aan de data met als tekst 'geen verkiezing'.
#
def verwerk_geen_verkiezingen(verkiezing, json):
  bestand = verkiezing + '/geen_verkiezingen.csv'
  gemeenten = {}

  if os.path.exists(bestand):
    print("Verwerk bestand met gemeenten die niet meedoen met deze verkiezing")
    with open(bestand, 'r', encoding='utf-8') as file:
      for regel in file:
        if not regel.strip():
          continue
        code, naam = regel.strip().split(',')
        json['data'][code] = [naam,'geen verkiezing']

#
# Maakt een gesorteerd array met tuple [gemeente code, gemeente naam]
# op basis van gegevens die in WaarIsMijnStemlokaal data bestand zijn verwerkt.
#
def converteer_gemeenten(data):
  gemeenten = []
  for code in data:
    gemeenten.append([code, data[code][0]])

  return sorted(gemeenten, key=lambda item: item[1])

#
# Schrijf het aantal aangeleverde gemeenten naar het voortgang.csv bestand.
#
def schrijf_voortgang(verkiezing, data):
  bestand = verkiezing + "/voortgang.csv"

  if not os.path.exists(bestand):
    with open(bestand, "w") as f:
      f.write("datum,aantal\n")
  with open(verkiezing + '/voortgang.csv', 'a', encoding='utf-8') as voortgangBestand:
    datum = date.today().strftime('%d-%m-%Y')
    #Gebruik volgende regels als een eerdere commit datum moet worden opgehaald.
    #Check de slt repo in andere directory uit, pass directory hieronder aan, checkout de specifieke commit
    #en run dit script.
    #datum = subprocess.run(['git', 'show', '-s', '--format=%cd', '--date=format:%d-%m-%Y'],
    #      cwd='<directory naar andere repo waar specifieke commit is uitgecheckt>',
    #      capture_output=True, text=True)
    #    .stdout.strip()
    voortgangBestand.write(datum + ',' + str(len(data)) + '\n')

#
# lees gemeenten bestand in.
#
def lees_gemeenten(directory, jsonBestand):
  bestand = directory + jsonBestand

  with open(bestand, 'r') as vorigeB:
    jsonGegevens = json.load(vorigeB)

    return {item[0]: tuple(item) for item in jsonGegevens}
#
# Maakt een bestand aan met gemeenten alle gemeenten die nog niet hun gegevens aan hebben geleverd.
# Dit wordt gedaan aan de hand van de lijst alle gemeenten.
# Als het bestand van alle gemeenten nog niet bestaat dan wordt het gekopieerd van de meegegeven vorige verkiezing.
#
def ontbrekende_gemeenten(verkiezing, vorige_verkiezing, ontbrekendeGemeentenBestand):
  gemeentenVerkiezingen = verkiezing + '/gemeenten.json'
  if not os.path.exists(gemeentenVerkiezingen):
    print ("Kopieer gemeenten.json bestand gemeenten van vorige verkiezingen.")
    with open(gemeentenVerkiezingen, 'w', encoding='utf-8') as gnb, open(vorige_verkiezing + '/gemeenten.json', 'r', encoding='utf-8') as gvb:
      gnb.write(gvb.read())

  vorigeDict = lees_gemeenten(verkiezing, '/gemeenten.json')
  nieuweDict = lees_gemeenten(verkiezing, '/aangeleverde_gemeenten.json')
  ontbrekendeGemeenten = [vorigeDict[num] for num in vorigeDict if num not in nieuweDict]

  for gemeente in ontbrekendeGemeenten:
      ontbrekendeGemeentenBestand.write(gemeente[1] + '\n')
  os.remove(verkiezing + '/aangeleverde_gemeenten.json')
  print("Ontbrekende gemeenten gegevens bestand aangemaakt.")

#
# Hoofd proces. Laad bestand van WaarIsMijnStemlokaal en converteert naar de verschillende bestanden.
#
def laad_en_verwerk_json_bestand(filename, verkiezing, vorige_verkiezing):
  try:
    with open(filename, 'r', encoding='utf-8') as file:
      data = json.load(file)
      stemlokalen = tel_toegankelijkheden(data)
      transform(stemlokalen)
      niet_verplicht_totaal(stemlokalen)
      filter_gtolk(stemlokalen)
      landelijke_totalen(stemlokalen)
      tenminste_een(stemlokalen)
      # schrijf voortang voor verwerk_geen_verkiezingen omdat anders gemeenten die niet meedoen met de verkiezing worden meegeteld.
      schrijf_voortgang(verkiezing, stemlokalen['data'])
      verwerk_geen_verkiezingen(verkiezing, stemlokalen)
      with open(verkiezing + '/stemlokalen.json', 'w', encoding='utf-8') as output:
        json.dump(stemlokalen, output, separators=(',', ':'))
      with open(verkiezing + '/aangeleverde_gemeenten.json', 'w', encoding='utf-8') as output:
        json.dump(converteer_gemeenten(stemlokalen['data']), output, separators=(',', ':'))
      with open(verkiezing + '/ontbrekende_gemeenten.csv', 'w', encoding='utf-8') as output:
        ontbrekende_gemeenten(verkiezing, vorige_verkiezing, output)

  except Exception as e:
      return f'Error loading or processing file: {str(e)}'

def main():
  global legacyToilet
  # Check if a filename was provided as command line argument
  if len(sys.argv) != 4:
      print('Gebruik: python converteer.py [stemlokalen json bestand] [verkiezing] [vorige verkiezing]')
      sys.exit(1)

  # Get the filename from command line arguments
  filename = sys.argv[1]
  verkiezing = "public/" + sys.argv[2]
  vorige_verkiezing = "public/" + sys.argv[3]
  # Voor oudere gegevens interpreteer toilet als een toegankelijk toilet.
  legacyToilet = int(sys.argv[2][2:]) < 2026
  
  # Process the file
  result = laad_en_verwerk_json_bestand(filename, verkiezing, vorige_verkiezing)

  # Check if there was an error
  if isinstance(result, str):
      print(result)
      sys.exit(1)

  # Print the results
  print('Conversie opgeslagen in: ' + verkiezing + '/stemlokalen.json')
  print('Conversie gemeenten opgeslagen in: ' + verkiezing + '/gemeenten.json')

if __name__ == '__main__':
    main()
