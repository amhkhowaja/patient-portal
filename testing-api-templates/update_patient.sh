#!/bin/bash

request_payload_path="payloads/update_patient.json"

payload=$(cat "$request_payload_path")

curl -X PUT -H "Content-Type: application/json" -d "$payload" "127.0.0.1:5000/patient/1"