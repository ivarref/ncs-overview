#!/bin/bash

set -ex

cd derived-remaining

lein run -m derived-remaining.produced-field-monthly

cd -
