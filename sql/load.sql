TRUNCATE TABLE station_list;
\copy station_list from ./data/station.csv with csv header null 'NULL' encoding 'utf-8';
TRUNCATE TABLE line_list;
\copy line_list from ./data/line.csv with csv header null 'NULL' encoding 'utf-8';