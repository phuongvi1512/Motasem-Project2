db = db.getSiblingDB('analyticdb');

// Create the 'analytics' collection if it doesn't already exist
db.createCollection('analytic');