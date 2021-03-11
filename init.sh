#!/bin/sh

sqlite3 ./users/users.db < ./users/users.sql
sqlite3 ./timelines/timelines.db < ./timelines/timelines.sql
