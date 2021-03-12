#!/bin/sh

sqlite3 ./users.db < ./users.sql
sqlite3 ./timelines.db < ./timelines.sql
