# AirBnB MongoDB Analysis

## About the Data
My chosen data set is a csv file containing information on AirBnB listings in Amsterdam, Netherlands. The original data can be found [here](http://insideairbnb.com/get-the-data/), and summaries and visualizations of the data can be found on [this page](http://insideairbnb.com/amsterdam). The first 20 rows of the data set can be seen below, along with a link to the csv file. I am only including some of the fields as all 75 columns would be difficult to fit into this document.

|   id   |             listing_url             |                       name                        | host_id | host_response_time | host_is_superhost |
|--------|-------------------------------------|---------------------------------------------------|---------|--------------------|-------------------|
| 2818   | https://www.airbnb.com/rooms/2818   | Quiet Garden View Room & Super Fast Wi-Fi         | 3159    | within an hour     | t                 |
| 311124 | https://www.airbnb.com/rooms/311124 | *historic centre* *bright* *canal view* *jordaan* | 1600010 | within a few hours | f                 |
| 319985 | https://www.airbnb.com/rooms/319985 | Elegant Appartement Central Location.             | 1640702 | within a day       | t                 |
| 327285 | https://www.airbnb.com/rooms/327285 | beautiful designed ap.+bikes+garden               | 1672823 | within an hour     | f                 |
| 331946 | https://www.airbnb.com/rooms/331946 | Lovely FAMILY house near Vondelpark               | 1687595 | N/A                | f                 |
| 343094 | https://www.airbnb.com/rooms/343094 | Amstel Nest - an urban retreat for two            | 1740785 | within an hour     | t                 |
| 20168  | https://www.airbnb.com/rooms/20168  | Studio with private bathroom in the centre 1      | 59484   | within an hour     | f                 |
| 350271 | https://www.airbnb.com/rooms/350271 | Luxe boat AMSTERDAM IJBURG!!!                     | 1775032 | N/A                | f                 |
| 357980 | https://www.airbnb.com/rooms/357980 | ★ STYLISH FAMILY HOME - CITY CENTER               | 1811745 | within a few hours | f                 |
| 366438 | https://www.airbnb.com/rooms/366438 | Amsterdam@ city centre & canal view               | 1849988 | within an hour     | t                 |
| 367107 | https://www.airbnb.com/rooms/367107 | IN HISTORIC CENTRE, NEXT TO AMSTEL, PEACEFUL HOME | 1853421 | within a day       | f                 |
| 27886  | https://www.airbnb.com/rooms/27886  | Romantic, stylish B&B houseboat in canal district | 97647   | within an hour     | t                 |
| 28871  | https://www.airbnb.com/rooms/28871  | Comfortable double room                           | 124245  | within an hour     | t                 |
| 367491 | https://www.airbnb.com/rooms/367491 | Charming,  bright and quiet home center Amsterdam | 1855417 | within a few hours | t                 |
| 29051  | https://www.airbnb.com/rooms/29051  | Comfortable single room                           | 124245  | within an hour     | t                 |
| 44391  | https://www.airbnb.com/rooms/44391  | Quiet 2-bedroom Amsterdam city centre apartment   | 194779  | N/A                | f                 |
| 378523 | https://www.airbnb.com/rooms/378523 | Freedom on the water!                             | 1901477 | within an hour     | f                 |
| 49552  | https://www.airbnb.com/rooms/49552  | Multatuli Luxury Guest Suite in top location      | 225987  | within a few hours | t                 |
| 379885 | https://www.airbnb.com/rooms/379885 | Private Studio Houseboat *BEST VIEW* @Amstel      | 1907015 | within an hour     | t                 |
| 402353 | https://www.airbnb.com/rooms/402353 | Comfortable design apartment with roof terrace    | 2008330 | within an hour     | t                 |

> [link to csv file](/data/listings.csv)  

<br/>

## Data Scrubbing
Overall, there weren't any glaring formatting issues with the data set. One issue I decided to address were the fields that contained no values, such as ```neighborhood_group_cleansed```, ```calendar_updated```, and ```bathrooms```. I removed the ```neighborhood_group_cleansed``` and ```calendar_updated``` fields entirely, and added values into the ```bathrooms``` column by slicing the number from the ```bathrooms_text``` values. I also added quotes around the values and converted quotes within values to double quotes to make the csv file easier to parse. The Python code I used to perform the munging can be found in the [munge.py](munge.py) file in this directory. There are also a lot of fields with redundant information that could be removed, but I decided it would be best not to delete any data from the table. For the sake of this assignment, it would also be best to keep all the data in one table and thus I decided not to normalize. I saved the cleansed file as [listings_clean.csv](/data/listings_clean.csv) in the data directory.

<br/> 

## MongoDB Queries
<br/> 

### 1) Show 2 documents from the 'listings' collection in any order:
```db.listings.find().sort({"id":1}).limit(2)```
<br/> 
The query above selects 2 documents from the database, and includes all fields. It is sorted by the ```id``` field in ascending order, so that it selects the two documents with the lowest ```id``` value. There is nothing notable that can be said about this query.
<br/> 

### 2) Show 10 documents in any order using 'prettyprint'
```db.listings.find().sort({"id":1}).limit(10).pretty()```
<br/> 
This query does the same thing as the code for the first question, except formatted using ```.pretty()``` for better readability. This also doesn't give us any insights into the data, as we are not looking at any specific criteria.
<br/> 

### 3) Choose two hosts who are 'superhosts' and show all of the listings by both hosts
```db.listings.find({host_is_superhost:"t"},{_id:0,host_id:1,host_is_superhost:1},)```
```db.listings.find({host_id:{$in:[124245,3159]}},{_id:0,name:1,price:1,neighbourhood:1,host_name:1,host_is_superhost:1}).sort({"host_id":1})```
<br/> 
The first query displays the values of the ```host_id``` for all documents where ```host_is_superhost``` is true. From those results, I picked two ```host_id``` values to use as criteria for the second query, which shows the listings for each of the two superhosts. Based on the values in the ```name``` field, a lot of these listings appear to be duplicates, which may also explain why many hosts have multiple listings. 
<br/> 

### 4) Find all unique ```host_name``` values
```db.listings.distinct("host_name")```
<br/> 
This query finds all of the distinct values for the field ```host_name```. This does give us very valuable insight into the data, but it does allow us to infer that many hosts own multiple listings, as the number of distinct documents shown by this query is far less than the total number of documents in the data set.
<br/> 

### 5) Find all places that have more than 2 ```beds``` in a particular neighborhood
```db.listings.find({beds:{$gte:3,},neighbourhood:"Amsterdam, North Holland, Netherlands"},{_id:0,name:1,beds:1}).sort({"reviews_scores_rating":-1})```
<br/> 
This query shows all listings with 3 or more beds in the neighbordhood Amsterdam, sorted by descending order of average rating. I chose this neighborhood because it contained the most listings. The only notable insight this query could provide would be that it seems like listings with more beds tend to be rated better, although it is difficult to say with a small sample size, and the correlation is not strong. 
<br/> 

### 6) Show the number of listings per host
```db.listings.aggregate([{$group:{_id:{host_id:"$host_id",host_name:"$host_name"},listingCount:{$sum:1}}},{$project:{_id:0,host_name:"$_id.host_name",host_id:"$_id.host_id",listingCount:1}}])```
<br/> 
This query groups this listings by ```host_id```, then counts the number of instances of each unique ```host_id``` to give the number of listings per host. Going through the list, there seems to be very few hosts with only one listing, with the majority having two. 
<br/> 

### 7) Find the average ```review_scores_rating``` per neighborhood, only show the ones above 95
```db.listings.aggregate([{$group:{_id:"$neighbourhood",avg_score:{$avg:"$review_scores_rating"}}},{$match:{avg_score:{$gte:4.75}}},{$project: {_id:0,neighbourhood:"$_id",avg_score:1}},{$sort:{avg_score:-1}}])```
<br/> 
This query groups the listings by ```neighbourhood```, then finds the average ```review_scores_rating``` for listings in each ```neighbourhood```. Since my values for ```review_scores_rating``` were from 1-5 rather than out of 100, I filtered out results that were less than 4.75 rather than 95 using the ```$match``` operator. I then used ```$sort``` to display the documents in descending order of average score. I found that the formatting of neighborhood names was incosistent, which resulted in redundancy when performing this query. This is something I didn't identify when performing the data munging. Of the documents displayed by this query that were unique neighborhoods, the one witht he highest average score was Landsmeer at 4.97.
<br/> 