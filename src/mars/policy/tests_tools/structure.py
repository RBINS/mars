import csv

def getStructure(
    csvfilename=None,
    delimiter=';',
    quotechar='"',
    quoting=csv.QUOTE_NONNUMERIC
):
    """Read structure/content to import from csvreplicata csvfile.

    >>> import pprint
    >>> structure = []
    >>> csvfilename = 'xml_doctests/structure.csv'
    >>> structure = getStructure(csvfilename)

    >>> pprint.pprint(structure)
    [{'description': '',
      'id': 'territoire',
      'parent': '',
      'title': 'TERRITOIRE',
      'type': 'Folder'},
     {'description': '',
      'id': 'portrait-type',
      'parent': 'territoire',
      'title': 'Portrait type',
      'type': 'Folder'},
     {'description': '',
      'id': 'economie',
      'parent': '',
      'title': 'ECONOMIE',
      'type': 'Folder'},
     {'description': '',
      'id': 'contexte',
      'parent': 'economie',
      'title': 'Contexte',
      'type': 'Folder'},
     {'description': '',
      'id': 'competences',
      'parent': '',
      'title': 'COMPETENCES',
      'type': 'Folder'},
     {'description': '',
      'id': 'etudier',
      'parent': 'competences',
      'title': 'Etudier',
      'type': 'Folder'},
     {'description': '',
      'id': 'travailler',
      'parent': 'competences',
      'title': 'Travailler',
      'type': 'Folder'}]

    """
    structure = []
    csvfile = open(csvfilename, 'rb')
    csvfile.seek(0)
    reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar,
                        quoting=csv.QUOTE_NONNUMERIC)
    #skip firstline
    reader.next()

    for row in reader:
        # read type fields
        if row[0] == 'parent':
            keys = row
            reader.next()
        # label line pass
        elif row[0]=='Parent Folder':
            reader.next()
        #appends a dict mapping keys and row values
        else:
            structure.append(dict(zip(keys, row)))

    csvfile.close()

    return structure


if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)
