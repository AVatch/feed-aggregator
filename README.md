# Feed-Aggregator
A python module which goes through either RSS or twitter sources and parses out any articles in them. 

## To Run
```bash
python aggregate -m rss -w 0
```

Arguments: ```-m``` or ```--mode``` can be either ```rss``` or ```twitter```. This goes into ```/sources/``` and 
pulls all content from those sources. 

```-w``` or ```--write``` can be either ```0``` or ```1```. If ```0``` this only streams the content, otherwise
it writes it to mongodb. If writing to mongodb, you need to have ```pymongo``` installed and be running ```mongod```.

