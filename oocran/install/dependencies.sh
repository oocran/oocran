#!/usr/bin/env bash

influx  -execute "CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES"
