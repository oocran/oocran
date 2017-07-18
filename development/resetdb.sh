#!/usr/bin/env bash

cd ../srs
#images
rm images/migrations/*
touch images/migrations/__init__.py
#libraries
rm scripts/migrations/*
touch scripts/migrations/__init__.py
#ns pools
rm pools/migrations/*
touch pools/migrations/__init__.py
#ns ues
rm ues/migrations/*
touch ues/migrations/__init__.py
#ns bbus
rm bbus/migrations/*
touch bbus/migrations/__init__.py
#ns/ns
rm ns/migrations/*
touch ns/migrations/__init__.py
#operators
rm operators/migrations/*
touch operators/migrations/__init__.py
#scenarios
rm scenarios/migrations/*
touch scenarios/migrations/__init__.py
#vims
rm vims/migrations/*
touch vims/migrations/__init__.py
#vnfs
rm vnfs/migrations/*
touch vnfs/migrations/__init__.py
#schedulers
rm schedulers/migrations/*
touch schedulers/migrations/__init__.py
#alerts
rm alerts/migrations/*
touch alerts/migrations/__init__.py
#keys
rm keys/migrations/*
touch keys/migrations/__init__.py
#delete db
rm db.sqlite3 &> /dev/null
#delete vagrant files
rm -r drivers/Vagrant/repository/* &> /dev/null
cd ..
