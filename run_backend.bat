@echo off
set PYTHONPATH=.
uvicorn src.main:app --reload --port 8080