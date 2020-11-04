TRUNCATE TABLE station_list;
\copy station_list from /Users/skaor/Documents/ekimemo/station_database/src/station.csv with csv header null 'NULL' encoding 'utf-8';

TRUNCATE TABLE line_list;
\copy line_list from /Users/skaor/Documents/ekimemo/station_database/src/line.csv with csv header null 'NULL' encoding 'utf-8';
