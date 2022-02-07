#!/bin/python3

# If you put some file names in a file named '.hidden', Nautilus will
# hide them. However, Nautilus only checks exact matches. This script
# allows to use gitignore-like patterns to hide files.
#
# The workaround used here is that .hidden file is split into two sections
# separated by a line of at least 5 equal signs (i.e. =====). The patterns
# should be placed before this separator. Then, this script completes
# the file by adding/updating exact filenames after the separator.
#
# In practice, you need to run this script manually to update the file
# with new matches. Maybe adding this file as a FilemanagerActions would
# be a good idea.


import glob
from pathspec import PathSpec


def main():
    patterns = find_patterns('.hidden')
    files = ls()
    matches = find_matches(patterns, files)
    update_dothidden(patterns, matches)


def find_patterns(filepath):
    patterns = []
    with open(filepath) as f:
        lines = f.readlines()
    for line in lines:
        if line[0:5] == '=====':
            break
        patterns.append(line)
    return patterns


def ls():
    return glob.iglob('**/**', recursive=True)


def find_matches(patterns, files):
    path_spec = PathSpec.from_lines('gitwildmatch', patterns)
    return filter(path_spec.match_file, files)


def update_dothidden(patterns, matches):
    with open('.hidden', 'w') as f:
        for pattern in patterns:
            f.write(pattern)
        f.write('======================\n\n')
        for match in matches:
            f.write(match + '\n')
        f.write("\n# For usage, see https://github.com/m2-farzan/dothidden-patterns")


if __name__ == '__main__':
    main()
