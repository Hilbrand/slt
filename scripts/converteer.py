import json
import sys

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
        return data

    except Exception as e:
        return f'Error processing the JSON: {str(e)}'

def transform(json):
  gemeenten = {}
  data = json['data']
  for code in data:
    gem = ""
    toegs = []
    totaal = 0
    for c in data[code]:
       if c == 'g':
         gem = data[code][c]
       else:
         toegs.append([c, data[code][c]])
         cat_totaal = sum(data[code][c].values())
         if cat_totaal > totaal:
           totaal = cat_totaal

    gemeenten[code] = [gem, totaal, toegs]

  json['data'] = gemeenten

def totalen(json):
  gemeenten = json['data']
  totaalStemlokalen = 0
  toegsTotaal = {}
  for code in gemeenten:
    gemeente = gemeenten[code]
    totaalStemlokalen += gemeente[1]
    for tg in gemeente[2]:
      tgName = tg[0]
      if tgName not in toegsTotaal:
         toegsTotaal[tgName] = [tgName, {}]
      values = tg[1]
      for value in values:
        totalTg = toegsTotaal[tgName][1]
        if value not in totalTg:
          totalTg[value] = 0
        totalTg[value] += values[value]
  totalenArray = []
  for tg in toegsTotaal:
    totalenArray.append(toegsTotaal[tg])
  json['national'] = ['national', sum(totalenArray[0][1].values()), totalenArray]

def greaterZero(values, key):
  return key in values and values[key] > 0

def increment(values, key):
  if (key not in values[1]):
    values[1][key] = 1
  else:
    values[1][key] += 1

def atLeastOne(json):
  gemeenten = json['data']
  totaalGemeenten = 0
  toegsTotaal = {}
  for code in gemeenten:
    gemeente = gemeenten[code]
    totaalGemeenten += 1
    for tg in gemeente[2]:
      tgName = tg[0]
      if tgName not in toegsTotaal:
         toegsTotaal[tgName] = [tgName, {}]
      values = tg[1]
      if greaterZero(values, 'j'):
        increment(toegsTotaal[tgName], 'j')
      elif greaterZero(values, 'a'):
        increment(toegsTotaal[tgName], 'a')
      elif greaterZero(values, 'l'):
        increment(toegsTotaal[tgName], 'l')
      elif 'n' in values and values['n'] == tg[1]:
        increment(toegsTotaal[tgName], 'n')
      else:
        increment(toegsTotaal[tgName], '')
  totalenArray = []
  for tg in toegsTotaal:
    totalenArray.append(toegsTotaal[tg])
  json['atLeastOne'] = ['atLeastOne', sum(totalenArray[0][1].values()), totalenArray]

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
            totalen(counted)
            atLeastOne(counted)
            with open(output_filename + '.json', 'w', encoding='utf-8') as output:
                json.dump(counted, output)
            with open(output_filename + '_gemeenten.json', 'w', encoding='utf-8') as output:
                json.dump(togemeenten(counted['data']), output)
            #totalePercentage(totalenArray)
            #print(totalenArray)
    except Exception as e:
        return f'Error loading or processing file: {str(e)}'

def main():
    # Check if a filename was provided as command line argument
    if len(sys.argv) != 3:
        print('Usage: python script.py path_to_json_file')
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
    print('resultaat geschreven naar ' + output_filename + '.json')
    print('resultaat geschreven naar ' + output_filename + 'gemeenten.json')
    # for code, counts in result.items():
    #     print(f'\nCode: {code}')
    #     for value, count in counts.items():
    #         # For empty strings, show as 'empty value'
    #         display_value = ''empty value'' if value == '' else f''{value}''
    #         print(f'  Value {display_value}: {count} occurrences')

if __name__ == '__main__':
    main()


