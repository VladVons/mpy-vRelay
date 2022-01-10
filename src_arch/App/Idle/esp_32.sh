#!/bin/bash

find . -type f -printf '%T@ %p\n' | sort -r
