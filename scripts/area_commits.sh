#!/bin/sh

# Obtain ordered list of SHA hashes for the specified directory
area_commits()
{
  git log --pretty='%H' master -- $1 | sort
}

# Find commits that touch both
comm -12 <(area_commits kernel) <(area_commits $1)
