### Datasets

*   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCensusData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01" target="_blank">Chicago Census Data</a>

*   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoPublicSchools.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01" target="_blank">Chicago Public Schools</a>

*   <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCrimeData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01" target="_blank">Chicago Crime Data</a>


%load_ext sql


import csv, sqlite3

con = sqlite3.connect("FinalDB.db")
cur = con.cursor()

!pip install -q pandas==1.1.5

%sql sqlite:///FinalDB.db


import pandas
df = pandas.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCensusData.csv")
df.to_sql("CENSUS_DATA", con, if_exists='replace', index=False,method="multi")

df = pandas.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoPublicSchools.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01")
df.to_sql("CHICAGO_PUBLIC_SCHOOLS", con, if_exists='replace', index=False,method="multi")

df = pandas.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DB0201EN-SkillsNetwork/labs/FinalModule_Coursera_V5/data/ChicagoCrimeData.csv?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDB0201ENSkillsNetwork20127838-2021-01-01")
df.to_sql("CHICAGO_CRIME_DATA", con, if_exists='replace', index=False,method="multi")

##### Finding the total number of crimes recorded in the CRIME table.

%sql SELECT COUNT(CASE_NUMBER) FROM 'CHICAGO_CRIME_DATA';

##### Listing community areas with per capita income less than 11000.

%sql SELECT "COMMUNITY_AREA_NAME", "PER_CAPITA_INCOME" FROM 'CENSUS_DATA' \
WHERE "PER_CAPITA_INCOME" < 11000 \
ORDER BY "PER_CAPITA_INCOME" ASC

##### Listing all case numbers for crimes involving minors

%sql SELECT "CASE_NUMBER", "DESCRIPTION" FROM "CHICAGO_CRIME_DATA" \
WHERE "DESCRIPTION" LIKE '%MINOR%';

##### Listing all kidnapping crimes involving a child

%sql SELECT "CASE_NUMBER", "PRIMARY_TYPE", "DESCRIPTION" FROM "CHICAGO_CRIME_DATA" \
WHERE "PRIMARY_TYPE" = 'KIDNAPPING' AND "DESCRIPTION" LIKE '%CHILD%';


##### Types of crimes recorded at schools

%sql SELECT DISTINCT PRIMARY_TYPE FROM "CHICAGO_CRIME_DATA" \
WHERE Location_Description LIKE '%SCHOOL%';


##### Listing the average safety score for each type of school

%sql SELECT "Elementary, Middle, or High School", AVG("SAFETY_SCORE") AS "Average Safety Score" \
FROM "CHICAGO_PUBLIC_SCHOOLS" \
GROUP BY "Elementary, Middle, or High School"

##### Listing 5 community areas with highest % of households below poverty line

%sql SELECT "COMMUNITY_AREA_NAME", "PERCENT_HOUSEHOLDS_BELOW_POVERTY" FROM "CENSUS_DATA" \
ORDER BY percent_households_below_poverty DESC \
LIMIT 5;

##### Which community area is most crime prone?

%sql SELECT CENSUS_DATA."COMMUNITY_AREA_NAME", COUNT(*) AS "Total Crimes" \
FROM CENSUS_DATA, CHICAGO_CRIME_DATA \
WHERE CENSUS_DATA."COMMUNITY_AREA_NUMBER" = CHICAGO_CRIME_DATA."COMMUNITY_AREA_NUMBER" \
GROUP BY CENSUS_DATA."COMMUNITY_AREA_NAME" \
ORDER BY "Total Crimes" DESC \
LIMIT 1;

##### Find the name of the community area with highest hardship index

%sql SELECT "COMMUNITY_AREA_NAME" FROM "CENSUS_DATA" \
WHERE "HARDSHIP_INDEX" = (SELECT MAX("HARDSHIP_INDEX") FROM "CENSUS_DATA");

##### Determine the Community Area Name with most number of crimes

%sql SELECT c."COMMUNITY_AREA_NAME", COUNT(*) as "NUM_CRIMES" \
FROM "CENSUS_DATA" c, "CHICAGO_CRIME_DATA" d \
WHERE c."COMMUNITY_AREA_NUMBER" = d."COMMUNITY_AREA_NUMBER" \
GROUP BY c."COMMUNITY_AREA_NAME" \
ORDER BY COUNT(*) DESC \
LIMIT 1;