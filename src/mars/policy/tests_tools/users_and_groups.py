import csv

def getUsersandGroups(
    csvfilename=None,
    delimiter=';',
    quotechar='"',
    quoting=csv.QUOTE_NONNUMERIC
):
    """Read structure/content to import from csvreplicata csvfile.

    >>> import pprint
    >>> imports = []
    >>> csvfilename = 'xml_doctests/users_and_groups.csv'
    >>> imports = getUsersandGroups(csvfilename)

get users
    >>> pprint.pprint(imports[0])
    [{'description': 'Membre 11 est Reviewer',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 11',
      'home_page': '',
      'id': 'member11',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member', 'Reviewer']},
     {'description': 'Descriptif Membre 12',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 12',
      'home_page': '',
      'id': 'member12',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member']},
     {'description': 'Descriptif Membre 13',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 13',
      'home_page': '',
      'id': 'member13',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member']},
     {'description': 'Membre 21 est Reviewer',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 21',
      'home_page': '',
      'id': 'member21',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member', 'Reviewer']},
     {'description': 'Descriptif Membre 22',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 22',
      'home_page': '',
      'id': 'member22',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member']},
     {'description': 'Descriptif Membre 23',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Membre 23',
      'home_page': '',
      'id': 'member23',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member']},
     {'description': '',
      'email': 'jpc@makinacorpus.com',
      'fullname': 'Administrateur du Portail',
      'home_page': '',
      'id': 'administrateur',
      'language': '',
      'location': '',
      'password': 'corpus',
      'roles': ['Member', 'Reviewer', 'Manager']}]

get groups
    >>> pprint.pprint(imports[1])
    [{'description': 'Description groupe1',
      'email': 'gr1@makina-corpus.com',
      'members': ['member11', 'member12', 'member13'],
      'name': 'group1',
      'role': ['Manager'],
      'title': 'Groupe 1'},
     {'description': 'Description groupe2',
      'email': 'gr2@makina-corpus.com',
      'members': ['member21', 'member22', 'member23'],
      'name': 'group2',
      'role': ['Member', 'Reviewer'],
      'title': 'Groupe 2'}]

no errors
    >>> pprint.pprint(imports[2])
    []

    """
    members = []
    groups = []
    errors = []
    values_without_spaces = ['id', 'roles', 'members', 'email', 'role']
    if type(csvfilename).__name__ == 'instance':
        csvfile = csvfilename
    else:
        csvfile = open(csvfilename, 'rb')
    csvfile.seek(0)
    reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar,
                        quoting=csv.QUOTE_NONNUMERIC)

    for row in reader:
        if row[0] in ['members', 'groups']:
            importing = row[0]
        elif row[0] == 'id' or row[0] == 'name':
            keys = row
        else:
            #building a mapping wiht keys and row values
            element = dict(zip(keys, row))
            #clear empty cells saved for columns alignment
            if '' in element:
                del element['']
            #delete spaces in values for sensibles keys
            for key in values_without_spaces :
                if key in element:
                    element[key] = element[key].strip()
            # append to corresponding list
            if importing == 'members':
                #spliting roles
                element['roles'] = [elt.strip() for elt in
                                    element['roles'].split(',')]
                members.append(element)
            elif importing == 'groups':
                #spliting members
                element['members'] = [elt.strip() for elt in
                                      element['members'].split(',')]
                element['role'] = [elt.strip() for elt in
                                      element['role'].split(',')]
                groups.append(element)
            else:
                errors.append(row)

    csvfile.close()

    return (members, groups, errors)

if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)
