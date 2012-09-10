#-*- coding: utf-8 -*-
#  mars http://www.naturalsciences.be/metamars/products/
#  Archetypes implementation of the MARS core types based on ATContentTypes
#  Copyright (c) 2003-2007 MARS development team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""

"""
__author__  = 'David Convent <david.convent@naturalsciences.be>'
__docformat__ = 'restructuredtext'


from Products.Archetypes.public import DisplayList, IntDisplayList

# Some portal type lists first

FILE_TYPES = ('File', 'External File')

IMAGE_FILE_TYPES = ('Image', 'Picture')

FOLDER_TYPES = ('Folder', 'Large Plone Folder')

FILE_AND_FOLDER_TYPES = FILE_TYPES + FOLDER_TYPES

IMAGE_FILE_AND_FOLDER_TYPES = IMAGE_FILE_TYPES + FILE_AND_FOLDER_TYPES

PEOPLE = ('People',)

PEOPLE_AND_INSTITUTION = PEOPLE + ('Institution',)

STRATIGRAPHICAL_LAYER = ('Stratigraphical Layer',)

DISCOVERY_PLACES = ('Mars Site', 'Excavation', 'Stratigraphy',
                    'Stratigraphical Layer', 'Structure Assemblage')

ASSEMBLAGE_COMPONENTS = ('Artefact', 'Hominid Remain', 'Fauna remain', 'Flora remain')

ARTEFACTS_TYPES = ['Artefact Reference Sample', 'Reference Sample', 'Artefact', 'Artefact Individual', 'Artefact Assemblage', 'EthnoArchaeologyReferenceSample', ]
HOMINIDS_TYPES = ['Hominid Reference Sample', 'Hominid Remain', 'Hominid Individual',  'Hominid Assemblage',]
FAUNA_TYPES = ['Flora Reference Sample', 'Fauna Remain', 'Fauna Individual', 'Fauna Assemblage', ]
FLORA_TYPES = ['Fauna Reference Sample', 'Flora Remain', 'Flora Individual', 'Flora Assemblage', ]
REFERENCE_SAMPLES = ARTEFACTS_TYPES + HOMINIDS_TYPES + FLORA_TYPES + FAUNA_TYPES

# Real vocabs (display lists now):

bp_dating_values  = range(0,        1000,      10)
bp_dating_values += range(1000,     5000,      50)
bp_dating_values += range(5000,     10000,     100)
bp_dating_values += range(10000,    50000,     500)
bp_dating_values += range(50000,    250000,    10000)
bp_dating_values += range(250000,   1000000,   50000)
bp_dating_values += range(1000000,  5000000,   100000)
bp_dating_values += range(5000000,  10000000,  500000)
bp_dating_values += range(10000000, 100000001, 10000000)
bp_dating_years = ()
for value in bp_dating_values:
    bp_dating_years += ((value, value),)
bp_dating_years = IntDisplayList(bp_dating_years)

begin_end_excavation_years = ()
for y in range(1800, 2051):
    begin_end_excavation_years += ((str(y), str(y)),)
begin_excavation_years = DisplayList(begin_end_excavation_years)

end_excavation_years = (('', 'Undefined'),) + begin_end_excavation_years
end_excavation_years = DisplayList(end_excavation_years)

dating_association = DisplayList((
        ('direct','direct'),
        ('context absolute dating','context absolute dating'),
        ('context relative dating','context relative dating'),
        ))

Countries_List = DisplayList((
        ("", "Choose"),
        ("AF","AFGHANISTAN, AF"),
        ("AX","ALAND ISLANDS, AX"),
        ("AL","ALBANIA, AL"),
        ("DZ","ALGERIA, DZ"),
        ("AS","AMERICAN SAMOA, AS"),
        ("AD","ANDORRA, AD"),
        ("AO","ANGOLA, AO"),
        ("AI","ANGUILLA, AI"),
        ("AQ","ANTARCTICA, AQ"),
        ("AG","ANTIGUA AND BARBUDA, AG"),
        ("AR","ARGENTINA, AR"),
        ("AM","ARMENIA, AM"),
        ("AW","ARUBA, AW"),
        ("AU","AUSTRALIA, AU"),
        ("AT","AUSTRIA, AT"),
        ("AZ","AZERBAIJAN, AZ"),
        ("BS","BAHAMAS, BS"),
        ("BH","BAHRAIN, BH"),
        ("BD","BANGLADESH, BD"),
        ("BB","BARBADOS, BB"),
        ("BY","BELARUS, BY"),
        ("BE","BELGIUM, BE"),
        ("BZ","BELIZE, BZ"),
        ("BJ","BENIN, BJ"),
        ("BM","BERMUDA, BM"),
        ("BT","BHUTAN, BT"),
        ("BO","BOLIVIA, BO"),
        ("BA","BOSNIA AND HERZEGOVINA, BA"),
        ("BW","BOTSWANA, BW"),
        ("BV","BOUVET ISLAND, BV"),
        ("BR","BRAZIL, BR"),
        ("IO","BRITISH INDIAN OCEAN TERRITORY, IO"),
        ("BN","BRUNEI DARUSSALAM, BN"),
        ("BG","BULGARIA, BG"),
        ("BF","BURKINA FASO, BF"),
        ("BI","BURUNDI, BI"),
        ("KH","CAMBODIA, KH"),
        ("CM","CAMEROON, CM"),
        ("CA","CANADA, CA"),
        ("CV","CAPE VERDE, CV"),
        ("KY","CAYMAN ISLANDS, KY"),
        ("CF","CENTRAL AFRICAN REPUBLIC, CF"),
        ("TD","CHAD, TD"),
        ("CL","CHILE, CL"),
        ("CN","CHINA, CN"),
        ("CX","CHRISTMAS ISLAND, CX"),
        ("CC","COCOS (KEELING) ISLANDS, CC"),
        ("CO","COLOMBIA, CO"),
        ("KM","COMOROS, KM"),
        ("CG","CONGO, CG"),
        ("CD","CONGO, THE DEMOCRATIC REPUBLIC OF THE, CD"),
        ("CK","COOK ISLANDS, CK"),
        ("CR","COSTA RICA, CR"),
        ("CI","COTE D'IVOIRE, CI"),
        ("HR","CROATIA, HR"),
        ("CU","CUBA, CU"),
        ("CY","CYPRUS, CY"),
        ("CZ","CZECH REPUBLIC, CZ"),
        ("DK","DENMARK, DK"),
        ("DJ","DJIBOUTI, DJ"),
        ("DM","DOMINICA, DM"),
        ("DO","DOMINICAN REPUBLIC, DO"),
        ("EC","ECUADOR, EC"),
        ("EG","EGYPT, EG"),
        ("SV","EL SALVADOR, SV"),
        ("GQ","EQUATORIAL GUINEA, GQ"),
        ("ER","ERITREA, ER"),
        ("EE","ESTONIA, EE"),
        ("ET","ETHIOPIA, ET"),
        ("FK","FALKLAND ISLANDS (MALVINAS), FK"),
        ("FO","FAROE ISLANDS, FO"),
        ("FJ","FIJI, FJ"),
        ("FI","FINLAND, FI"),
        ("FR","FRANCE, FR"),
        ("GF","FRENCH GUIANA, GF"),
        ("PF","FRENCH POLYNESIA, PF"),
        ("TF","FRENCH SOUTHERN TERRITORIES, TF"),
        ("GA","GABON, GA"),
        ("GM","GAMBIA, GM"),
        ("GE","GEORGIA, GE"),
        ("DE","GERMANY, DE"),
        ("GH","GHANA, GH"),
        ("GI","GIBRALTAR, GI"),
        ("GR","GREECE, GR"),
        ("GL","GREENLAND, GL"),
        ("GD","GRENADA, GD"),
        ("GP","GUADELOUPE, GP"),
        ("GU","GUAM, GU"),
        ("GT","GUATEMALA, GT"),
        ("GN","GUINEA, GN"),
        ("GW","GUINEA-BISSAU, GW"),
        ("GY","GUYANA, GY"),
        ("HT","HAITI, HT"),
        ("HM","HEARD ISLAND AND MCDONALD ISLANDS, HM"),
        ("VA","HOLY SEE (VATICAN CITY STATE), VA"),
        ("HN","HONDURAS, HN"),
        ("HK","HONG KONG, HK"),
        ("HU","HUNGARY, HU"),
        ("IS","ICELAND, IS"),
        ("IN","INDIA, IN"),
        ("ID","INDONESIA, ID"),
        ("IR","IRAN, ISLAMIC REPUBLIC OF, IR"),
        ("IQ","IRAQ, IQ"),
        ("IE","IRELAND, IE"),
        ("IL","ISRAEL, IL"),
        ("IT","ITALY, IT"),
        ("JM","JAMAICA, JM"),
        ("JP","JAPAN, JP"),
        ("JO","JORDAN, JO"),
        ("KZ","KAZAKHSTAN, KZ"),
        ("KE","KENYA, KE"),
        ("KI","KIRIBATI, KI"),
        ("KP","KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF, KP"),
        ("KR","KOREA, REPUBLIC OF, KR"),
        ("KW","KUWAIT, KW"),
        ("KG","KYRGYZSTAN, KG"),
        ("LA","LAO PEOPLE'S DEMOCRATIC REPUBLIC, LA"),
        ("LV","LATVIA, LV"),
        ("LB","LEBANON, LB"),
        ("LS","LESOTHO, LS"),
        ("LR","LIBERIA, LR"),
        ("LY","LIBYAN ARAB JAMAHIRIYA, LY"),
        ("LI","LIECHTENSTEIN, LI"),
        ("LT","LITHUANIA, LT"),
        ("LU","LUXEMBOURG, LU"),
        ("MO","MACAO, MO"),
        ("MK","MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF, MK"),
        ("MG","MADAGASCAR, MG"),
        ("MW","MALAWI, MW"),
        ("MY","MALAYSIA, MY"),
        ("MV","MALDIVES, MV"),
        ("ML","MALI, ML"),
        ("MT","MALTA, MT"),
        ("MH","MARSHALL ISLANDS, MH"),
        ("MQ","MARTINIQUE, MQ"),
        ("MR","MAURITANIA, MR"),
        ("MU","MAURITIUS, MU"),
        ("YT","MAYOTTE, YT"),
        ("MX","MEXICO, MX"),
        ("FM","MICRONESIA, FEDERATED STATES OF, FM"),
        ("MD","MOLDOVA, REPUBLIC OF, MD"),
        ("MC","MONACO, MC"),
        ("MN","MONGOLIA, MN"),
        ("MS","MONTSERRAT, MS"),
        ("MA","MOROCCO, MA"),
        ("MZ","MOZAMBIQUE, MZ"),
        ("MM","MYANMAR, MM"),
        ("NA","NAMIBIA, NA"),
        ("NR","NAURU, NR"),
        ("NP","NEPAL, NP"),
        ("NL","NETHERLANDS, NL"),
        ("AN","NETHERLANDS ANTILLES, AN"),
        ("NC","NEW CALEDONIA, NC"),
        ("NZ","NEW ZEALAND, NZ"),
        ("NI","NICARAGUA, NI"),
        ("NE","NIGER, NE"),
        ("NG","NIGERIA, NG"),
        ("NU","NIUE, NU"),
        ("NF","NORFOLK ISLAND, NF"),
        ("MP","NORTHERN MARIANA ISLANDS, MP"),
        ("NO","NORWAY, NO"),
        ("OM","OMAN, OM"),
        ("PK","PAKISTAN, PK"),
        ("PW","PALAU, PW"),
        ("PS","PALESTINIAN TERRITORY, OCCUPIED, PS"),
        ("PA","PANAMA, PA"),
        ("PG","PAPUA NEW GUINEA, PG"),
        ("PY","PARAGUAY, PY"),
        ("PE","PERU, PE"),
        ("PH","PHILIPPINES, PH"),
        ("PN","PITCAIRN, PN"),
        ("PL","POLAND, PL"),
        ("PT","PORTUGAL, PT"),
        ("PR","PUERTO RICO, PR"),
        ("QA","QATAR, QA"),
        ("RE","REUNION, RE"),
        ("RO","ROMANIA, RO"),
        ("RU","RUSSIAN FEDERATION, RU"),
        ("RW","RWANDA, RW"),
        ("SH","SAINT HELENA, SH"),
        ("KN","SAINT KITTS AND NEVIS, KN"),
        ("LC","SAINT LUCIA, LC"),
        ("PM","SAINT PIERRE AND MIQUELON, PM"),
        ("VC","SAINT VINCENT AND THE GRENADINES, VC"),
        ("WS","SAMOA, WS"),
        ("SM","SAN MARINO, SM"),
        ("ST","SAO TOME AND PRINCIPE, ST"),
        ("SA","SAUDI ARABIA, SA"),
        ("SN","SENEGAL, SN"),
        ("CS","SERBIA AND MONTENEGRO, CS"),
        ("SC","SEYCHELLES, SC"),
        ("SL","SIERRA LEONE, SL"),
        ("SG","SINGAPORE, SG"),
        ("SK","SLOVAKIA, SK"),
        ("SI","SLOVENIA, SI"),
        ("SB","SOLOMON ISLANDS, SB"),
        ("SO","SOMALIA, SO"),
        ("ZA","SOUTH AFRICA, ZA"),
        ("GS","SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS, GS"),
        ("ES","SPAIN, ES"),
        ("LK","SRI LANKA, LK"),
        ("SD","SUDAN, SD"),
        ("SR","SURINAME, SR"),
        ("SJ","SVALBARD AND JAN MAYEN, SJ"),
        ("SZ","SWAZILAND, SZ"),
        ("SE","SWEDEN, SE"),
        ("CH","SWITZERLAND, CH"),
        ("SY","SYSRIAN ARAB REPUBLIC, SY"),
        ("TW","TAIWAN, PROVINCE OF CHINA, TW"),
        ("TJ","TAJIKISTAN, TJ"),
        ("TZ","TANZANIA, UNITED REPUBLIC OF, TZ"),
        ("TH","THAILAND, TH"),
        ("TL","TIMOR-LESTE, TL"),
        ("TG","TOGO, TG"),
        ("TK","TOKELAU, TK"),
        ("TO","TONGA, TO"),
        ("TT","TRINIDAD AND TOBAGO, TT"),
        ("TN","TUNISIA, TN"),
        ("TR","TURKEY, TR"),
        ("TM","TURKMENISTAN, TM"),
        ("TC","TURKS AND CAICOS ISLANDS, TC"),
        ("TV","TUVALU, TV"),
        ("UG","UGANDA, UG"),
        ("UA","UKRAINE, UA"),
        ("AE","UNITED ARAB EMIRATES, AE"),
        ("GB","UNITED KINGDOM, GB"),
        ("US","UNITED STATES, US"),
        ("UM","UNITED STATES MINOR OUTLYING ISLANDS, UM"),
        ("UY","URUGUAY, UY"),
        ("UZ","UZBEKISTAN, UZ"),
        ("VU","VANUATU, VU"),
        ("ho","Vatican City State see HOLY SEE"),
        ("VE","VENEZUELA, VE"),
        ("VN","VIET NAM, VN"),
        ("VG","VIRGIN ISLANDS, BRITISH, VG"),
        ("VI","VIRGIN ISLANDS, U.S., VI"),
        ("WF","WALLIS AND FUTUNA, WF"),
        ("EH","WESTERN SAHARA, EH"),
        ("YE","YEMEN, YE"),
        ("za","Zaire see CONGO, THE DEMOCRATIC REPUBLIC OF THE"),
        ("ZM","ZAMBIA, ZM"),
        ("ZW","ZIMBABWE, ZW"),
        ))

basic_chronology = DisplayList((
        ('recent','recent'),
        ('historic','historic'),
        ('prehistoric','prehistoric'),
        ))

CoordinatesAquisition = DisplayList((
        ('GPS Site Coordinates','GPS Site Coordinates'),
        ('Map Site Coordinates','Map Site Coordinates'),
        ('GPS nearest city Coordinates','GPS nearest city Coordinates'),
        ('Map nearest city Coordinates','Map nearest city Coordinates'),
        ('other','other'),
        ))

collection_source = DisplayList((
        ('None', ''),
        ('Excavation', 'Excavation'),
        ('Prospection', 'Prospection'),
        ('Exchange', 'Exchange'),
        ('Donation', 'Donation'),
        ('Purchase', 'Purchase'),
        ('Distraint', 'Distraint'),
        ('Other','Other'),
        ))

# Default Selection Values
default_date_precision = DisplayList((
        ('exact', 'exact'),
        ('before', 'before'),
        ('after', 'after'),
        ('around', 'around'),
        ))

default_gender = DisplayList((
        ('female','female'),
        ('male','male'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

default_origin = DisplayList((
        ('Anthropic','Anthropic'),
        ('Animal','Animal'),
        ('natural','natural'),
        ('other','other'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

default_laterality = DisplayList((
        ('Left','Left'),
        ('Right','Right'),
        ('Unpaired','Unpaired'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

default_polarity = DisplayList((
        ('Upper','Upper'),
        ('Lower','Lower'),
        ('Proximal','Proximal'),
        ('Distal','Distal'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

default_preservation = DisplayList((
        ('complete','complete'),
        ('fragmentary','fragmentary'),
        ))

default_burial = DisplayList((
        ('certain','certain'),
        ('supposed','supposed'),
        ('improbable','improbable'),
        ('No','No'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

archeological_status = DisplayList((
        ('certain','certain'),
        ('supposed','supposed'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))

analysis_keywords = DisplayList((
        ('',''),
        ))

# Flora Selection Values
flora_gender = default_gender
flora_laterality = default_laterality
flora_polarity = default_polarity
flora_origin = default_origin
flora_preservation = default_preservation
flora_burial = default_burial

# Fauna Selection Values
fauna_gender = default_gender
fauna_laterality = default_laterality
fauna_polarity = default_polarity
fauna_origin = default_origin
fauna_preservation = default_preservation
fauna_burial = default_burial

# Hominid Selection Values
hominid_gender = default_gender
hominid_laterality = default_laterality
hominid_polarity = default_polarity
hominid_origin = default_origin
hominid_preservation = default_preservation
hominid_burial = default_burial

# Institution Selection Values
institution_nature = DisplayList((
        ('Museum','Museum'),
        ('University','University'),
        ('Research institution','Research institution'),
        ('Fundation','Fundation'),
        ('Other','Other'),
        ))

# XXX: Why not a workflow ??
institution_status = DisplayList((
        ('Public','Public'),
        ('Private','Private'),
        ))

institution_level = DisplayList((
        ('International','International'),
        ('National','National'),
        ('Federal','Federal'),
        ('Regional','Regional'),
        ('Other','Other'),
        ))

# XXX: Why not a workflow ??
analysis_status = DisplayList((
        ('published','published'),
        ('pending','pending'),
        ('...','...'),
        ))


# Abandoned vocabs (they are now categories):
default_age = DisplayList((
        ('foetus or neonate','foetus or neonate'),
        ('baby','baby'),
        ('immature','immature'),
        ('adult','adult'),
        ('unknown','unknown'),
        ('undetermined','undetermined'),
        ))
hominid_age = DisplayList((
        ('adult','adult (20y and more)'),
        ('subadult','subadult (below 20)'),
        ('foetus','foetus( week 9 - birth)'),
        ('neonate','neonate (0 - 1y)'),
        ('foetus or neonate','foetus or neonate'),
        ('infans','infans (infans I or II)'),
        ('infans I','infans I (1 - 6y)'),
        ('infans II','infans II (7 - 13y)'),
        ('juvenile','juvenile (14 - 19y)'),
        ('undetermined','undetermined'),
        ))


MarsTypes = [
    'Analysis Absolute Dating',
    'Analysis Relative Dating',
    'Analysis',
    'Artefact Assemblage',
    'Artefact Individual',
    'Artefact Reference Sample',
    'Artefact',
    'Categories Container',
    'Mars Collection',
    'Curation',
    'Excavation',
    'Fauna Assemblage',
    'Fauna Individual',
    'Fauna Reference Sample',
    'Fauna Remain',
    'Flora Assemblage',
    'Flora Individual',
    'Flora Reference Sample',
    'Flora Remain',
    'Hominid Assemblage',
    'Hominid Individual',
    'Hominid Reference Sample',
    'Hominid Remain',
    'InbookReference',
    'Institution',
    'Mars Category',
    'People',
    'Reference Sample',
    'Mars Site',
    'Stratigraphical Layer',
    'Stratigraphy',
    'Structure Assemblage',
]

REFERENCEFIELDS_INDEXES = {}

