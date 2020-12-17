import csv, re, sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

exp = re.compile('(Grade: ([ABCDF])[-+]?( \((\d*\.*\d*)\))?)|(Grade: (\d+\.?\d+))')

student = ''
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg in ("-s", "--student"):
        if i + 1 == len(sys.argv):
            print("no argument to {}".format(arg))
            sys.exit(1)
        student = sys.argv[i + 1]
    i += 1

with open('export.csv') as file:
    with open('parsed.csv', 'w', newline='') as out:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        writer = csv.writer(out)
        writer.writerow(['date', 'student', 'course', 'grade'])
        for row in reader:
            course = row[10]
            date = row[0]
            name = row[1]
            if name != student:
                continue;
            note = row[13]
            match = exp.match(note)
            if match is None:
                continue

            grade = match.group(2) # e.g. C
            if grade is None:
                grade = match.group(4) # e.g. C (70)
            if grade is None:
                grade = match.group(6) # e.g. 70

            if grade == 'A':
                grade = 100
            elif grade == 'B':
                grade = 80
            elif grade == 'C':
                grade = 70
            elif grade == 'D':
                grade = 60
            elif grade == 'F':
                grade = 50

            writer.writerow([pd.to_datetime(date), name, course, grade])

dateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
cs_df = pd.read_csv('parsed.csv', parse_dates=['date'], date_parser=dateparser)

sns.set_theme(style="darkgrid")

fig, ax = plt.subplots(figsize = (12,12))

fig = sns.lineplot(x="date", y="grade", hue="course", data=cs_df, ax=ax)

plt.show()
