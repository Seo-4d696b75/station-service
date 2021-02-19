# Station-Service

日本中の駅・路線データへの簡潔なアクセス手段を提供します. ここで扱うデータは[GitHub station_database](https://github.com/Seo-4d696b75/station_database)で管理されています.

## Deploy

[heroku](https://station-service.herokuapp.com/api/docs)にホストされる  


## Update Data

現状は手動操作が必要

1. fetch data  
  `$ python py/data.py` 
2. open console  
  `$ heroku pg:psql -a station-service`  
   then run script:  
  `$ \i sql/load.sql;`  
  `$ INSERT INTO data_info (data_version, updated_at) VALUES (${version}, now());`
3. restart api server  
  `$ heroku restart -a station-service`  
   tree data is loaded directly when app reboots
