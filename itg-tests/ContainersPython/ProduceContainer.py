import os, time, sys
from kafka.KcProducer import KafkaProducer

print(" @@@ Executing script: ProduceContainer.py")

##############################
##### READ ENV VARIABLES #####
##############################
try:
    KAFKA_BROKERS = os.environ['KAFKA_BROKERS']
except KeyError:
    print("The KAFKA_BROKERS environment variable needs to be set.")
    exit(1)

# Try to read the Kafka environment from the environment variables
try:
    KAFKA_ENV = os.environ['KAFKA_ENV']
except KeyError:
    KAFKA_ENV='LOCAL'

# Try to read the Kafka user from the environment variables
try:
    KAFKA_USER = os.environ['KAFKA_USER']
except KeyError:
    print("The KAFKA_USER environment variable not set... assume local deployment")
    KAFKA_USER=''

# Try to read the Kafka password from the environment variables
try:
    KAFKA_PASSWORD = os.environ['KAFKA_PASSWORD']
except KeyError:
    print("The KAFKA_PASSWORD environment variable not set... assume local deployment")
    KAFKA_PASSWORD=''


####################### VARIABLES #######################
ID = "c01"
TOPIC_NAME="test"

####################### FUNCTIONS #######################
# Create a default container
def createContainer(id):
    print('Creating container...', end ='')
    data = {"containerID": id, 
        "type": "Reefer", 
        "status": "Empty",
        "latitude": 37.80,
        "longitude":  -122.25,
        "capacity": 110, 
        "brand": "itg-brand"}
    containerEvent = {"containerID": id,"timestamp": int(time.time()),"type":"ContainerAdded","payload": data}
    print("DONE")
    return containerEvent

# Parse arguments to get the Container ID
def parseArguments():
    global TOPIC_NAME, ID
    print("The arguments for the script are: " , str(sys.argv))
    if len(sys.argv) == 3:
        ID = sys.argv[1]
        TOPIC_NAME = sys.argv[2]
    else:
        print("[ERROR] - The ProduceContainer.py script expects two arguments: The container ID and the topic to send the container event to.")
        exit(1)

####################### MAIN #######################
if __name__ == '__main__':
    parseArguments()
    evt = createContainer(ID)
    print("Container event to be published:")
    print(evt)
    kp = KafkaProducer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_USER,KAFKA_PASSWORD)
    kp.prepareProducer("ProduceContainerPython")
    kp.publishEvent(TOPIC_NAME,evt,"containerID")
