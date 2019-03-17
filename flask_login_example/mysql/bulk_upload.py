#! venv/bin/python3.7

import csv
from itertools import islice

import requests

def parse_file(filepath, limit=None):
    fieldnames = ('RegistrationUsername', 'Identity', 'Alignment', 'Gender', 'Sex',
                  'EyeColour', 'HairColour', 'Alive', 'Appearances')
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in (reader if limit is None else islice(reader, limit)):
            character = {}
            character['RegistrationUsername'] = row['RegistrationUsername']
            character['RegistrationPassword'] = row['RegistrationUsername']
            character['RegistrationPassword2'] = row['RegistrationUsername']
            character['Identity'] = {'': 'None', 'Secret Identity': 'secret', 'Public Identity': 'public', 'Identity Unknown': 'unknown', 'Known to Authorities Identity': 'known', 'No Dual Identity': 'no_dual'}[row['Identity']]
            character['Alignment'] = {'': 'None', 'Bad Characters': 'bad', 'Good Characters': 'good', 'Neutral Characters': 'neutral', 'Reformed Criminals': 'reformed'}[row['Alignment']]
            character['Gender'] = {'': 'None', 'Bisexual Characters': 'bisexual', 'Genderfluid Characters': 'genderfluid', 'Homosexual Characters': 'homosexual', 'Pansexual Characters': 'pansexual', 'Transgender Characters': 'transgender', 'Transvestites': 'transvestites'}[row['Gender']]
            character['Sex'] = {'': 'None',  'Agender Characters': 'agender', 'Female Characters': 'female', 'Genderfluid Characters': 'genderfluid', 'Genderless Characters': 'genderless', 'Male Characters': 'male', 'Transgender Characters': 'transgender'}[row['Sex']]
            character['EyeColour'] = {'': 'None', 'Amber Eyes': 'amber', 'Auburn Hair': 'auburn', 'Black Eyeballs': 'black', 'Black Eyes': 'black', 'Blue Eyes': 'blue', 'Brown Eyes': 'brown', 'Compound Eyes': 'compound', 'Gold Eyes': 'gold', 'Green Eyes': 'green', 'Grey Eyes': 'grey', 'Hazel Eyes': 'hazel', 'Magenta Eyes': 'magenta', 'Multiple Eyes': 'multiple', 'No Eyes': 'no', 'One Eye': 'one', 'Orange Eyes': 'orange', 'Photocellular Eyes': 'photocellular', 'Pink Eyes': 'pink', 'Purple Eyes': 'purple', 'Red Eyes': 'red', 'Silver Eyes': 'silver', 'Variable Eyes': 'variable', 'Violet Eyes': 'violet', 'White Eyes': 'white', 'Yellow Eyeballs': 'yellow', 'Yellow Eyes': 'yellow'}[row['EyeColour']]
            character['HairColour'] = {'': 'None', 'Auburn Hair': 'auburn', 'Bald': 'bald', 'Black Hair': 'black', 'Blond Hair': 'blond', 'Blue Hair': 'blue', 'Bronze Hair': 'bronze', 'Brown Hair': 'brown', 'Dyed Hair': 'dyed', 'Gold Hair': 'gold', 'Green Hair': 'green', 'Grey Hair': 'grey', 'Light Brown Hair': 'light', 'Magenta Hair': 'magenta', 'No Hair': 'no', 'Orange Hair': 'orange', 'Orange-brown Hair': 'orange-brown', 'Pink Hair': 'pink', 'Platinum Blond Hair': 'platinum', 'Purple Hair': 'purple', 'Red Hair': 'red', 'Reddish Blond Hair': 'reddish', 'Reddish Brown Hair': 'reddish', 'Silver Hair': 'silver', 'Strawberry Blond Hair': 'strawberry', 'Variable Hair': 'variable', 'Violet Hair': 'violet', 'White Hair': 'white', 'Yellow Hair': 'yellow'}[row['HairColour']]
            character['Alive'] = {'': 'living', 'Deceased Characters': 'deceased', 'Living Characters': 'living'}[row['Alive']]
            character['Appearances'] = int(float(row['Appearances'] if row['Appearances'] else 0))
            yield character


if __name__ == '__main__':
    characters = parse_file(r'mysql/comic_book_characters.txt')
    for character in characters:
        print(character['RegistrationUsername'])
        requests.post(r'http://127.0.0.1:5000/', data=character)
