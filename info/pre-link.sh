#!/bin/bash

# Fail immediately if something's wrong
set -e

# Write into this file for anything that the user should see
OUT="$PREFIX/.messages.txt"

# Adjust SOURCE_DIR (for convenience)
SOURCE_DIR="$SOURCE_DIR/opt/lsst/obs_decam"

# Add $PREFIX/bin to $PATH; it's not on the path when run
# in _build environment (is this a bug in conda-build?)
export PATH="$PREFIX/bin:$PATH"

# initialize EUPS
source eups-setups.sh

# Merge the EUPS tags used by this package with the global EUPS database
#
IFS=':' read -ra EUPS_PATH_ARR <<< "$EUPS_PATH"
TAGFILE="${EUPS_PATH_ARR[0]}/ups_db/global.tags"

# We need to merge the tags in the existing global.tags file, with any new
# tags that our product needs:
#
# What the magic below does (in order):
#   * cat both files, ensuring there's a newline between them
#   * convert whitespaces to newlines
#   * sort & run uniq
#   * remove any empty lines
#   * translate newlines back to whitespaces
touch "$TAGFILE"						# make sure it exists
awk 'FNR==1{print ""}1' "$SOURCE_DIR/ups/global.tags" "$TAGFILE" | 	\
		tr ' ' '\n' | \
		sort -u     | \
		awk 'NF'    | \
		tr '\n' ' ' \
		> "$TAGFILE".tmp

# Move the new file into place
mv "$TAGFILE".tmp "$TAGFILE"
