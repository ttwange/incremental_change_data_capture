Run this to bring up the docker-compose file and its images 
          :docker-compose up -d (to compose a docker container)
Use this command to connect the debezium with kafka  
          :curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" 127.0.0.1:8083/connectors/ --data "@debezium.json" 
          (set up debezium connector to listen the postgres table changes)
Run this command to start monitoring the changes made to the db
          :docker run --tty --network project1_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=s -s value=avro -r http:/schema-registry:8081 -t postgres.public.
          tablename 
          :docker run --tty --network incremental_change_data_capture_default confluentinc/cp-kafkacat kafkacat -b kafka:9092 -C -s key=s -s value=avro -r http:/schema-registry:8081 -t postgres.public.asset
          (Tail the kafka topic to see if it's listening to debezium postgres changes)

to get the docker_network run docker network ls to get your local network
