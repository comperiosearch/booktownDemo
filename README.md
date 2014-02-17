#Elasticsearch river-jdbc demo
##Prerequisites:

Download and install 

- [elasticsearch 1.0.0.RC1](http://www.elasticsearch.org/downloads/1-0-0-rc1/)

- [postgresql](http://www.postgresql.org/download/)
 
Latest version of postgres jdbc driver
http://www.postgresql.org/download/

## Setup postgres
 Download  [booktown.sql](http://www.commandprompt.com/ppbook/booktown.sql)  to install  the BookTown database


	psql -u postgres -f booktown.sql


## Setup Elasticsearch
Install the  [river-jdbc elasticsearch plugin](https://github.com/jprante/elasticsearch-river-jdbc)


	./bin/plugin -install river-jdbc -url http://bit.ly/1dKqNJy (ES 1.0.0.RC1)


### Download postgres jdbc driver jar
[http://jdbc.postgresql.org/download.html](http://jdbc.postgresql.org/download.html)
(Recommended version is [JDBC 41](http://jdbc.postgresql.org/download/postgresql-9.3-1100.jdbc41.jar)
)
Copy the postgres.****.jar file into the `/plugins/river-jdbc` folder of your elasticsearch installation.


##Elasticsearch commandoes:
All the Elasticsearch commandoes you need to use to follow this demo are available at 
[http://sense.qbox.io/gist/d10ac6949d7574a5f0acc94b309b9d3ab314b13e](http://sense.qbox.io/gist/d10ac6949d7574a5f0acc94b309b9d3ab314b13e).

[An introduction to using the Sense plugin](https://www.found.no/foundation/Sense-Elasticsearch-interface/)

[http://sense.qbox.io](http://sense.qbox.io) provide a hosted Sense experience, something like Gist for Elasticsearch. 

restart elasticsearch
loaded [river-jdbc] should occur in log


Put river
 "success [15 items]"


          select books.id as _id, title, author_id as 'Author.Id', subject_id as 'Subject.Id', last_name as 'Author.LastName', first_name as 'Author.FirstName', subject as 'Subject.Subject', location as 'Subject.Location' from books left join authors on authors.id = books.author_id left join subjects on books.subject_id = subjects.id

select books.id as _id, title, author_id  , subject_id  , last_name  , first_name  , subject  , location  from books left join authors on authors.id = books.author_id left join subjects on books.subject_id = subjects.id

https://github.com/jprante/elasticsearch-river-jdbc/wiki/Structured-Objects
