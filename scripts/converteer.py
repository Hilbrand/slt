import json
import sys
from datetime import date
import subprocess

toegankelijkheids_categorieen = [
    'Toegankelijk voor mensen met een lichamelijke beperking',
    'Toegankelijke ov-halte',
    'Gehandicaptentoilet',
    'Host',
    'Prikkelarm',
    'Geleidelijnen',
    'Kandidatenlijst in braille',
    'Kandidatenlijst met grote letters',
    'Stemmal met audio-ondersteuning',
    'Gebarentolk (NGT)',
    'Gebarentalig stembureaulid (NGT)',
    'Akoestiek geschikt voor slechthorenden',
]

toegankelijkheids_categorieen_short = {
    'Toegankelijk voor mensen met een lichamelijke beperking': 'lb',
    'Toegankelijke ov-halte'                                 : 'ov',
    'Gehandicaptentoilet'                                    : 'to',
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
          v = 'j'
        case 'nee':
          v = 'n'
        case 'op afstand':
          v = 'a'
        case 'op locatie':
          v = 'l'
        case _:
          v = value
    stc = toegankelijkheids_categorieen_short[tc]
    if stc not in gemeente:
        gemeente[stc] = {}
    if v not in gemeente[stc]:
        gemeente[stc][v] = 0
    gemeente[stc][v] += 1

def count_values(json_data):
    try:
        # Extract the records array
        records = json_data['result']['records']

        # Group records by CBS gemeentecode
        data = { 'resource_id': json_data['result']['resource_id'], 'data' : {} }
        gemeentecode_groups = data['data']
        keys = {}
        for record in records:
            code = record.get('CBS gemeentecode')[2:]

            if code not in gemeentecode_groups:
                gemeentecode_groups[code] = {'g': record.get('Gemeente')}

            for tc in toegankelijkheids_categorieen:
               value = record.get(tc, '')
               set_value(gemeentecode_groups[code], tc, value)
               keys[value] = 1
        print("Counted all records.")
        return data
    except Exception as e:
        return f'Error processing the JSON: {str(e)}'

#
#
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
  print("Transformed counted values to new structure.")
  json['data'] = gemeenten

#
#
#
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
  json['national'] = ['national', sum(toegsTotaal['lb'].values()), toegsTotaal]
  print("Counted national values.")

def greaterZero(values, key):
  return key in values and values[key] > 0

def increment(values, key):
  if (key not in values):
    values[key] = 1
  else:
    values[key] += 1

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
      if tgName not in toegsTotaal:
          toegsTotaal[tgName] = {}
      states = allTgStates[tgName]
      if greaterZero(states, 'j'):
        increment(toegsTotaal[tgName], 'j')
      elif greaterZero(states, 'a'):
        increment(toegsTotaal[tgName], 'a')
      elif greaterZero(states, 'l'):
        increment(toegsTotaal[tgName], 'l')
      elif 'n' in states and states['n'] == gemeente[1]:
        increment(toegsTotaal[tgName], 'n')
      else:
        increment(toegsTotaal[tgName], '')
  json['atLeastOne'] = ['atLeastOne', sum(toegsTotaal['lb'].values()), toegsTotaal]
  print("Counted at-least-one.")

def togemeenten(data):
  gemeenten = []
  for code in data:
    gemeenten.append([code, data[code][0]])

  return sorted(gemeenten, key=lambda item: item[1])

def load_and_process_json_file(filename, output_filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            counted = count_values(data)
            transform(counted)
            nationalTotals(counted)
            atLeastOne(counted)
            with open(output_filename + '.json', 'w', encoding='utf-8') as output:
                json.dump(counted, output)
            with open(output_filename + '_gemeenten.json', 'w', encoding='utf-8') as output:
                json.dump(togemeenten(counted['data']), output)
            with open(output_filename + '_voortgang.csv', 'a', encoding='utf-8') as voortgangBestand:
                datum = date.today().strftime('%d-%m-%Y')
                #Gebruik volgende regels als een eerdere commit datum moet worden opgehaald.
                #Check de slt repo in andere directory uit, pass directory hieronder aan, checkout de specifieke commit
                #en run dit script.
                #datum = subprocess.run(['git', 'show', '-s', '--format=%cd', '--date=format:%d-%m-%Y'],
                #      cwd='<directory naar andere repo waar specifieke commit is uitgecheckt>',
                #      capture_output=True, text=True)
                #    .stdout.strip()
                voortgangBestand.write(datum + ',' + str(len(counted['data'])) + '\n')

    except Exception as e:
        return f'Error loading or processing file: {str(e)}'

def main():
    # Check if a filename was provided as command line argument
    if len(sys.argv) != 3:
        print('Gebruik: python converteer.py [stemlokalen json bestand] [uitvoer bestand zonder extensie]')
        sys.exit(1)

    # Get the filename from command line arguments
    filename = sys.argv[1]
    output_filename = sys.argv[2]

    # Process the file
    result = load_and_process_json_file(filename, output_filename)

    # Check if there was an error
    if isinstance(result, str):
        print(result)
        sys.exit(1)

    # Print the results
    print('Conversie opgeslagen in: ' + output_filename + '.json')
    print('Conversie gemeentes opgeslagen in: ' + output_filename + '_gemeenten.json')

if __name__ == '__main__':
    main()
