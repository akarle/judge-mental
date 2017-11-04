import csv
import os

br_file = os.path.join('..', 'data', 'br.csv')
br_trim = os.path.join('..', 'data', 'br-trim.csv')
if not os.path.isfile(br_trim):
    # Parse out the all but title, author, review in the book reviews data
    print 'creating ', br_trim
    with open(br_file, 'r') as brf:
        with open(br_trim, 'w') as testf:
            reader = csv.reader(brf, delimiter=',')
            writer = csv.writer(testf, delimiter=',')
            reader.next()  # remove headers
            for row in reader:
                writer.writerow(row[1:4])

else:
    print '%s already exists, not recreating' % br_trim
