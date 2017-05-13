#!/usr/bin/env bash

cd ../srs
#images
rm images/migrations/*
touch images/migrations/__init__.py
#libraries
rm libraries/migrations/*
touch libraries/migrations/__init__.py
#nfs
rm nfs/migrations/*
touch nfs/migrations/__init__.py
#ns/utrans
rm ns/utrans/migrations/*
touch ns/utrans/migrations/__init__.py
#ns/epcs
rm ns/epcs/migrations/*
touch ns/epcs/migrations/__init__.py
#ns/ns
rm ns/ns/migrations/*
touch ns/ns/migrations/__init__.py
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

rm db.sqlite3

echo "reset finish!"
echo "exe: ./oocran install server"