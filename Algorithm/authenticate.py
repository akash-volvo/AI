import warnings
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

# Ignore warnings
warnings.filterwarnings("ignore")

# MongoDB connection parameters
uri = "mongodb+srv://akash123455190:qk9QYRTQRznnoeAj@ai.dnfpij7.mongodb.net/?appName=AI"

# Create a new client and connect to the server with TLS options
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))

db = client['AI']

results_collection = db['results']
weights_collection = db['weights']
