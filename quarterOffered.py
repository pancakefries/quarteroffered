#!/usr/bin/env python
"""
    quarterOffered
    
    A dead simple web scraper to make it easier to plan classes at UChicago

    By: Josh Garza
"""
import urllib.request
import re, string
from bs4 import BeautifulSoup

url = "http://collegecatalog.uchicago.edu/thecollege/"

deptcodes = {"astr":"astronomyastrophysics",
             "bios":"biologicalsciences",
             "phys":"physics",
             "math":"mathematics",
             "stat":"statistics",
             "cmsc":"computerscience",
             "chem":"chemistry",
             "sosc":"socialsciences",
             "anth":"anthropology",
             "arth":"arthistory",
             "cmst":"cinemamediastudies",
             "arch":"architecturalstudies",
             "clcv":"classicalstudies",
             "chdv":"comparativehumandevelopment",
             "cmlt":"comparativeliterature",
             "crwr":"creativewriting",
             "econ":"economics",
             "ensc":"environmentalscience",
             "geos":"geophysicalsciences",
             "hist":"history",
             "ling":"linguistics",
             "meng":"molecularengineering",
             "musi":"music",
             "psyc":"psychology",
             "taps":"theaterperformancestudies"}

def run():
    coursename = input("Enter the course code: ")

    valid_dept = False
    try:
        coursecode = re.findall("[0-9]{5}", coursename)[0]
        deptname = deptcodes[re.findall("[a-zA-Z]{4}", coursename)[0].lower()]

        fp = urllib.request.urlopen(url + deptname)
    except:
        print("Invalid department name/course code")
        pass
    else:
        valid_dept = True

    if valid_dept:
        mybytes = fp.read()
        fp.close()

        soup = BeautifulSoup(mybytes, 'html.parser')
        blocks = [soup.find_all(class_ = 'courseblock main'), soup.find_all(class_ = 'courseblock subsequence')]
        if not blocks[0] and not blocks[1]:
            raise LookupError('Page has no courses listed')

        for block in blocks:
            for course in block:
                coursenum = re.findall('\d{5}', course.text)
                if coursenum[0] == coursecode:
                    quarter = re.findall('(Terms Offered:[ |\n][\w+\s]+)\nPrerequisite', course.text)

        try:
            print(quarter[0].replace('\n', ', '))
        except:
            print('Did not find quarter offered, did you enter the correct course code?')

while True:
    run()