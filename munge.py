import csv

f = open('data/listings.csv','r')
data = list(csv.DictReader(f))


for row in data:
    #remove columns with no values
    del row['neighbourhood_group_cleansed']
    del row['calendar_updated']

    #filling in empty values for 'bathrooms'
    bathroom_text_separate = row['bathrooms_text'].split(' ') #separate out number from bathrooms description
    row['bathrooms'] = bathroom_text_separate[0] #put number into 'bathrooms' column


clean = open('data/listings_clean.csv','w')

headers = list(data[0].keys())
clean.write(','.join(headers)+'\n')


for row in data:
    values = list(row.values())
    values_clean = []
    for item in values:
        item = item.replace('"','""') #replace quotes within values with double quotes
        item = '"'+str(item)+'"' #add quotes around values that contain commas or excape characters
        values_clean.append(item)

    clean.write(','.join(values_clean)+'\n')
clean.close()
