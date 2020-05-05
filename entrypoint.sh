#!/bin/bash
uvicorn --host 0.0.0.0 --workers 4 app.main:api --reload
