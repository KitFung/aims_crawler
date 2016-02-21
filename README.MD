Requirement
---

1. Python 2.7

2. pip

3. [mongodb](https://www.mongodb.org)

Target
---
CityU Aims System

Environment variables
---
AIMS_NAME: username

AIMS_PASSWORD: password

```bash
$ export AIMS_NAME=XXXX
$ export AIMS_PASSWORD=XXXX
```

Setup
---

```bash
$ virtualenv -p /usr/bin/python2.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt #It take a few minutus
#setup mongodb
$ mongo
> use aims
> aims.createCollection(course)
> db.course.createIndex('code', 'text')
```

Run!
---

`$ scrapy crawl course`

Example Record
---

```javascript
{'code': u'EF3442',
 'details': [{'Avail': 23,
              'CRN': u'37330',
              'Campus': u'Main Campus',
              'Cap': 105,
              'Credit': 3,
              'Level': u'B',
              'Section': u'C01',
              'WEB': True,
              'Waitlist_Avail': False,
              'lessons': [{'Bldg': u'AC1',
                           'Date': (datetime.datetime(2016, 1, 11, 0, 0),
                                    datetime.datetime(2016, 4, 23, 0, 0)),
                           'Day': u'F',
                           'Instructor': [u'MUTLU Gulseren'],
                           'Room': u'LT-18',
                           'Time': (900, 1050)}],
              'not_allow_majors': [u'U'],
              'only_colleges': [u'CB'],
              'only_degrees': [u'BBA', u'BBA1', u'EXFB']},
             {'Avail': 0,
              'CRN': u'37331',
              'Campus': u'Main Campus',
              'Cap': 35,
              'Credit': 0,
              'Level': u'B',
              'Section': u'T01',
              'WEB': True,
              'Waitlist_Avail': False,
              'lessons': [{'Bldg': u'AC1',
                           'Date': (datetime.datetime(2016, 1, 11, 0, 0),
                                    datetime.datetime(2016, 4, 23, 0, 0)),
                           'Day': u'R',
                           'Instructor': [u'MUTLU Gulseren'],
                           'Room': u'Y5-205',
                           'Time': (1200, 1250)}],
              'not_allow_majors': [u'U'],
              'only_colleges': [u'CB'],
              'only_degrees': [u'BBA', u'BBA1', u'EXFB']},
             {'Avail': 18,
              'CRN': u'37332',
              'Campus': u'Main Campus',
              'Cap': 35,
              'Credit': 0,
              'Level': u'B',
              'Section': u'T02',
              'WEB': True,
              'Waitlist_Avail': False,
              'lessons': [{'Bldg': u'AC1',
                           'Date': (datetime.datetime(2016, 1, 11, 0, 0),
                                    datetime.datetime(2016, 4, 23, 0, 0)),
                           'Day': u'T',
                           'Instructor': [u'MUTLU Gulseren'],
                           'Room': u'Y5-303',
                           'Time': (1700, 1750)}],
              'not_allow_majors': [u'U'],
              'only_colleges': [u'CB'],
              'only_degrees': [u'BBA', u'BBA1', u'EXFB']},
             {'Avail': 5,
              'CRN': u'37333',
              'Campus': u'Main Campus',
              'Cap': 35,
              'Credit': 0,
              'Level': u'B',
              'Section': u'T03',
              'WEB': True,
              'Waitlist_Avail': False,
              'lessons': [{'Bldg': u'AC1',
                           'Date': (datetime.datetime(2016, 1, 11, 0, 0),
                                    datetime.datetime(2016, 4, 23, 0, 0)),
                           'Day': u'R',
                           'Instructor': [u'MUTLU Gulseren'],
                           'Room': u'B5-309',
                           'Time': (1100, 1150)}],
              'not_allow_majors': [u'U'],
              'only_colleges': [u'CB'],
              'only_degrees': [u'BBA', u'BBA1', u'EXFB']}],
 'exclusive_formula': [],
 'exclusive_text': '',
 'full_header': u'EF3442 Intermediate Microeconomics',
 'requirement_formula': [u'CB2400', u'FB2400', u'or'],
 'requirement_text': u'CB2400 or FB2400',
 'unit': u'Economics & Finance'}

```


Todo
---

- [X] Setup the basic function, include fetching course detail and design the data structure.
- [ ] Support fetch all the record in different semester
- [ ] Support other data in the aims system
- [ ] Optimize the data structure according to the monogodb best practice and practical usage