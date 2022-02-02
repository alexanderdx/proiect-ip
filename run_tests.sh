#!/bin/bash

if [ -f "test.db" ] ; then
    rm "test.db"
fi

python -m pytest test/

if [ -f "test.db" ] ; then
    rm "test.db"
fi