import csv
import os

reviews = {}
br_file = os.path.join('..', 'data', 'br.csv')
# Parse out the all but title, author, review in the book reviews data
print "Parsing %s into a dictionary {'author-title': review}" % br_file
with open(br_file, 'r') as br_f:
    reader = csv.reader(br_f, delimiter=',')
    reader.next()  # remove headers
    for row in reader:
        key = str(row[1]) + '---' + str(row[2])
        val = row[3]
        reviews[key] = val

# for r in reviews.iteritems():
    # print r

summarys = {}
summ_file = os.path.join('..', 'data', 'booksummaries.txt')
print "Parsing %s into a dictionary {'author-title': review}" % summ_file
# Parse out the title, author, plot
with open(summ_file, 'r') as summ_f:
    reader = csv.reader(summ_f, delimiter='\t')

    for row in reader:
        key = str(row[2]) + '---' + str(row[3])
        val = row[-1]
        summarys[key] = val

# Moment of truth... the overlap
# TODO: optimize for better overlap
intersect = set(summarys.keys()) & set(reviews.keys())

# Write the combined data set to file
comb_file = os.path.join('..', 'data', 'combined.csv')
print "Writing cobined dataset %s to file" % comb_file
with open(comb_file, 'w') as comb_f:
    writer = csv.writer(comb_f, delimiter=',')
    for key in intersect:
        row = [key, summarys[key], str(reviews[key])]
        writer.writerow(row)
