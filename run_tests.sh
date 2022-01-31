#!/bin/bash

if [ -f "test.db" ] ; then
    rm "test.db"
fi

source venv/scripts/activate

python -m pytest test/

if [ -f "test.db" ] ; then
    rm "test.db"
fi