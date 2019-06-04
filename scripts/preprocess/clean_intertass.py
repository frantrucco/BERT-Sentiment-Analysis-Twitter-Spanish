import csv
import sys
import os
from tass import InterTASSReader as Reader
from cleaner import clean

DATASET_FILES = {
    "CR": {
        "dev": "CR/intertass-CR-development-tagged.xml",
        "test": "CR/intertass-CR-test.xml",
        "train": "CR/intertass-CR-train-tagged.xml"
    },

    "ES": {
        "dev": "ES/intertass-ES-development-tagged.xml",
        "test": "ES/intertass-ES-test.xml",
        "train": "ES/intertass-ES-train-tagged.xml"
    },

    "PE": {
        "dev": "PE/intertass-PE-development-tagged.xml",
        "test": "PE/intertass-PE-test.xml",
        "train": "PE/intertass-PE-train-tagged.xml"
    }
}

TYPES = ["dev", "test", "train"]


if __name__ == '__main__':
    IN_DIR = sys.argv[1]
    OUT_DIR = sys.argv[2]

    data = {}

    try:
        os.mkdir(IN_DIR)
    except OSError:
        pass

    for t in TYPES:
        for country, dataset in DATASET_FILES.items():
            reader = Reader(IN_DIR + '/' + dataset[t])
            data[t] = list(zip(reader.y(), reader.X()))

        with open('{}/{}.tsv'.format(OUT_DIR, t), 'w') as out:
            csv_out = csv.writer(out, delimiter='\t')
            for row in data[t]:
                sentiment, text = row
                text = clean(text)
                if sentiment:
                    csv_out.writerow([sentiment, text])
                else:
                    csv_out.writerow([text])
