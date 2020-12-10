import os,sys
from kafka.KcConsumer import KafkaConsumer

print(" @@@ Executing script: ConsumeContainers.py")

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
# Parse arguments to get the container ID to poll for
def parseArguments():
    global TOPIC_NAME, ID
    print("The arguments for the script are: " , str(sys.argv))
    if len(sys.argv) != 3:
        print("[ERROR] - The ConsumeContainer.py script expects two arguments: The container ID and the topic to send the container event to.")
        exit(1)
    ID = sys.argv[1]
    TOPIC_NAME = sys.argv[2]
    print("The Kafka environment is: " + KAFKA_ENV)
    print("The Kafka brokers are: " + KAFKA_BROKERS)
    print("The Kafka User is: " + KAFKA_USER)
    print("The Kafka Password is: " + KAFKA_PASSWORD)

####################### MAIN #######################
if __name__ == '__main__':
    parseArguments()
    consumer = KafkaConsumer(KAFKA_ENV,KAFKA_BROKERS,KAFKA_USER,KAFKA_PASSWORD,TOPIC_NAME)
    consumer.prepareConsumer()
    consumer.pollNextEvent(ID,'containerID')
    consumer.close()