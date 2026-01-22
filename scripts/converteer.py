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

toegankelijkheids_categorieen_short = {
    LB                                                       : 'lb',
    'Toegankelijke ov-halte'                                 : 'ov',
    'Gehandicaptentoilet'                                    : 'to',
    'Toilet'                                                 : 'to',
    'Host'                                                   : 'ho',
    'Prikkelarm'                                             : 'pa',
    'Geleidelijnen binnen'                                   : 'gi',
    'Geleidelijnen buiten'                                   : 'gu',
    'Kandidatenlijst in braille'                             : 'kb',
    'Kandidatenlijst met grote letters'                      : 'kg',
    'Stemmal met audio-ondersteuning'                        : 'sa',
    'Gebarentolk (NGT)'                                      : 'gt',
    'Gebarentalig stembureaulid (NGT)'                       : 'gs',
    'Akoestiek geschikt voor slechthorenden'                 : 'as',
    'Prokkelduo'                                             : 'pd',
     'Niet verplichte toegankelijkheden'                     : 'nv',
}

uitzonderingen = {
  'binnen',
  'buiten',
}

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
    else:
      tc = categorie
      match value:
        case 'ja':
          v = 't' if tc == 'Gehandicaptentoilet' and legacyToilet else 'j'
        case 'nee':
          v = 'n'
        # gebarentolk
        case 'op afstand':
          v = 'a'
        case 'op locatie':
          v = 'l'
        # toilet
        case 'ja, toegankelijk toilet':
          v = 't'
        case 'ja, genderneutraal toilet':
          v = 'g'
        case _:
          v = value

    stc = toegankelijkheids_categorieen_short[tc]
    if stc not in gemeente:
        gemeente[stc] = {}
    if v not in gemeente[stc]:
        gemeente[stc][v] = 0
    gemeente[stc][v] += 1

#
# Telt de toegankelijkheden en groepeert per gemeente.
#
def telToegankelijkheden(json_data):
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
def nietVerplichtTotaal(json):
  gemeenten = json['data']
  for code in gemeenten:
    gemeente = gemeenten[code]
    allTgStates = gemeente[2]
    totalTg = {}
    for tgName in allTgStates:
      if tgName != 'lb':
        for state in allTgStates[tgName]:
          if state == 'a' or state == 'l' or state == 't' or state == 'g':
            bewaarState = 'j'
          else:
           bewaarState = state
          if bewaarState not in totalTg:
            totalTg[bewaarState] = 0
          totalTg[bewaarState] += allTgStates[tgName][state]
    if totalTg == 0:
      print(gemeente[0])
    allTgStates['nv'] = totalTg
  print("Niet verplichte toegankelijkheden totalen geteld.")

#
# Tel de toegankelijkheden op landelijk nivo.
#
def nationalTotals(json):
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
def greaterZero(values, key):
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
def atLeastOne(json):
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
      if greaterZero(states, 'j'):
        increment(toegsTotaal[tgName], 'j')
      elif greaterZero(states, 'a'):
        increment(toegsTotaal[tgName], 'a')
      elif greaterZero(states, 'l'):
        increment(toegsTotaal[tgName], 'l')
      elif greaterZero(states, 't'):
        increment(toegsTotaal[tgName], 't')
      elif greaterZero(states, 'g'):
        increment(toegsTotaal[tgName], 'g')
      elif 'n' in states and states['n'] == noCount:
        increment(toegsTotaal[tgName], 'n')
      else:
        increment(toegsTotaal[tgName], '')
  json['atLeastOne'] = ['atLeastOne', sum(toegsTotaal['lb'].values()), toegsTotaal]
  print("Gegevens van tenminste 1 aangemaakt.")

#
# Maakt een gesorteerd array met tuple [gemeente code, gemeente naam]
# op basis van gegevens die in WaarIsMijnStemlokaal data bestand zijn verwerkt.
#
def converteerGemeenten(data):
  gemeenten = []
  for code in data:
    gemeenten.append([code, data[code][0]])

  return sorted(gemeenten, key=lambda item: item[1])

#
# Schrijf het aantal aangeleverde gemeenten naar het voortgang.csv bestand.
#
def schrijfVoortgang(verkiezing, data):
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
# Maakt een bestand aan met gemeenten die nog niet hun gegevens aan hebben geleverd.
# Dit wordt gedaan aan de hand van de lijst gemeenten van de vorige verkiezing.
#
def ontbrekendeGemeenten(verkiezing, vorige_verkiezing, ontbrekendeGemeentenBestand):
  vorigeVerkiezingBestand = vorige_verkiezing + '/gemeenten.json'
  nieuweVerkiezingBestand = verkiezing + '/gemeenten.json'

  with open(vorigeVerkiezingBestand, 'r') as f1, open(nieuweVerkiezingBestand, 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

  dict1 = {item[0]: tuple(item) for item in data1}
  dict2 = {item[0]: tuple(item) for item in data2}
  ontbrekendeGemeenten = [dict1[num] for num in dict1 if num not in dict2]

  for gemeente in ontbrekendeGemeenten:
      ontbrekendeGemeentenBestand.write(gemeente[1] + '\n')
  print("Ontbrekende gemeenten gegevens bestand aangemaakt.")

#
# Hoofd proces. Laad bestand van WaarIsMijnStemlokaal en converteert naar de verschillende bestanden.
#
def load_and_process_json_file(filename, verkiezing, vorige_verkiezing):
  try:
    with open(filename, 'r', encoding='utf-8') as file:
      data = json.load(file)
      counted = telToegankelijkheden(data)
      transform(counted)
      nietVerplichtTotaal(counted)
      nationalTotals(counted)
      atLeastOne(counted)
      with open(verkiezing + '/stemlokalen.json', 'w', encoding='utf-8') as output:
        json.dump(counted, output, separators=(',', ':'))
      with open(verkiezing + '/gemeenten.json', 'w', encoding='utf-8') as output:
        json.dump(converteerGemeenten(counted['data']), output, separators=(',', ':'))
      schrijfVoortgang(verkiezing, counted['data'])
      with open(verkiezing + '/ontbrekende_gemeenten.csv', 'w', encoding='utf-8') as output:
        ontbrekendeGemeenten(verkiezing, vorige_verkiezing, output)

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
  result = load_and_process_json_file(filename, verkiezing, vorige_verkiezing)

  # Check if there was an error
  if isinstance(result, str):
      print(result)
      sys.exit(1)

  # Print the results
  print('Conversie opgeslagen in: ' + verkiezing + '/stemlokalen.json')
  print('Conversie gemeenten opgeslagen in: ' + verkiezing + '/gemeenten.json')

if __name__ == '__main__':
    main()
