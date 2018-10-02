#!/usr/bin/env python3 

from helpers import *


def area_commits(area):
    # Area commits
    _cmd = "git log --pretty='%H' master -- {}".format(area)
    l = cmd(_cmd)
    return set(l)


def areas_violations(*areas):
    # Area violations
    assert(len(areas) >= 1)
    result = area_commits(areas[0])
    for area in areas[1:]:
        result &= area_commits(area)
    return result


def changed_files(_hash):
    # Show changed files in a list
    _cmd = 'git show --pretty="format:" --name-only ' + _hash
    l = cmd(_cmd)
    return l


def commit_message(_hash):
    # Get commit message
    _cmd = 'git show -s --format=%B ' + _hash
    l = cmd(_cmd)
    return l


def last_hash():
    _cmd = 'git show -s --format=%H HEAD'
    l = cmd(_cmd)
    return l[0]


def get_unique_commits(areas):
    # Get unique area commits
    unique_commits = {}

    for area in areas:
        print(area)
        unique_commits[area] = area_commits(area)

    # TODO Improve complexity
    for area in areas:
        for aarea in areas:
            if aarea != area:
                unique_commits[area] -= unique_commits[aarea]

    return unique_commits
