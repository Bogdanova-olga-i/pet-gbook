# pet-gbook

## Start
1. docker-compose up -d --build
2. Make tables in MySQL:
   1) python
   2) from app import app, db, User, Article, ExperimentData
   3) app.app_context().push()
   4) db.create_all()
3. Run app: python app.py



## What is wrong and what is my problem

1. I make simple boolean feature «my-feature» and publish it
2. And make Experiment with params:










   
  "id": "exp_4064501mlm0aa3x4",
  "trackingKey": "target_button",
  "organization": "org_4064501mlm09qaov",
  "project": "",
  "owner": "u_4064501mlm09qaoe",
  "datasource": "ds_4064501mlm09yaty",
  "userIdType": "anonymous",
  "exposureQueryId": "",
  "hashAttribute": "",
  "hashVersion": 2,
  "name": "target_button",
  "dateCreated": "2023-09-01T07:38:45.208Z",
  "dateUpdated": "2023-09-01T07:38:45.208Z",
  "tags": [],
  "description": "",
  "hypothesis": "",
  "metrics": [],
  "metricOverrides": [],
  "guardrails": [],
  "activationMetric": "",
  "segment": "",
  "queryFilter": "",
  "skipPartialData": false,
  "attributionModel": "firstExposure",
  "archived": false,
  "status": "draft",
  "analysis": "",
  "releasedVariationId": "",
  "excludeFromPayload": true,
  "autoAssign": false,
  "implementation": "code",
  "previewURL": "",
  "targetURLRegex": "",
  "variations": [
    {
      "id": "var_lm0a9665",
      "name": "Control",
      "description": "",
      "key": "0",
      "screenshots": [],
      "dom": []
    },
    {
      "id": "var_lm0a9666",
      "name": "Variation 1",
      "description": "",
      "key": "1",
      "screenshots": [],
      "dom": []
    }
  ],
  "phases": [
    {
      "dateStarted": "2023-09-01T07:38:00.000Z",
      "dateEnded": null,
      "name": "Main",
      "reason": "",
      "coverage": 1,
      "condition": "{}",
      "variationWeights": [
        0.5,
        0.5
      ],
      "groups": [],
      "seed": "target_button",
      "namespace": {
        "enabled": false,
        "name": "",
        "range": [
          0,
          1
        ]
      }
    }
  ],
  "lastSnapshotAttempt": "2023-09-01T07:38:45.208Z",
  "nextSnapshotAttempt": "2023-09-01T13:38:45.208Z",
  "autoSnapshots": true,
  "ideaSource": "",
  "linkedFeatures": [],
  "sequentialTestingEnabled": false,
  "sequentialTestingTuningParameter": 5000


At loading features by:
request.gb.load_features()
(L 108 in app.py)

A message appears on the command line:
**Unknown feature my-feature**


