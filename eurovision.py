import csv
import json
import re

# This is the python script used by instructors to create the JSON
# files in this repository. Students don't need to do anything with
# this file.
# Instructors: Download contestants.csv file from here to get started:
# https://github.com/Spijkervet/eurovision-dataset/releases

def to_camel_case(match):
    return match[0][1].upper()

with open('contestants.csv') as fileref:
    songs = []
    reader = csv.DictReader(fileref)
    songs_encountered = set()
    for row in reader:
        song = {}

        # Avoid duplicates
        if row['youtube_url'] in songs_encountered:
            continue
        else:
            songs_encountered.add(row['youtube_url'])

        for key in row.keys():
            camelKey = re.sub('_[a-zA-Z]', to_camel_case, key)
            if camelKey == 'lyrics':
                # The lyrics linebreaks are doubly escaped.
                # https://github.com/Spijkervet/eurovision-dataset/blob/4c9395e33cc197ba43db42feb96f718ccb2b8a64/eurovision/scrapers/votes.py#L239-L241
                song[camelKey] = re.sub('\\\\n', '\n', row[key])
            else:
                if not row[key]:
                    # null
                    song[camelKey] = None
                else:
                    try:
                        # Number
                        song[camelKey] = int(row[key])
                    except ValueError:
                        try:
                            # Number
                            song[camelKey] = int(round(float(row[key]), 0))
                        except ValueError:
                            # String
                            song[camelKey] = row[key]
        songs.append(song)

with open(f'eurovisionContestants.js', 'w') as fileref:
    js_string = f'''// The data in this file comes from
// "Eurovision Dataset" by Janne Spijkervet and others.
// Zenodo, November 9, 2023.
// https://doi.org/10.5281/zenodo.10088892
// CC BY 4.0.

export const contestants = {json.dumps(songs, indent=2)}'''
    fileref.write(js_string)
