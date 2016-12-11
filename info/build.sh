#!/bin/bash
#
# The conda-build build script to build eupspkg-packaged code
#

# Find the true source root: conda tries to be helpful and
# changes into the first non-empty directory given a github repository; 
export SRC_DIR=$(git rev-parse --show-toplevel)
cd $SRC_DIR

#
# Adjust OS-X specific parameters
#
if [[ "$OSTYPE" == darwin* ]]; then
	# - Can't run earlier than Mountain Lion (10.8)
	# (astrometry.net build breaks (at least))
	# - Can't run earlier than Mavericks
	# (boost won't build otherwise; 10.9 switched to libc++)
	export MACOSX_DEPLOYMENT_TARGET="10.9"

	# Make sure there's enough room in binaries for the install_name_tool magic
	# to work
	export LDFLAGS="$LDFLAGS -headerpad_max_install_names"

#	# Make sure binaries (e.g., tests) get built with enough
#	# padding in the header for the install_name_tool to work
#	# (sconsUtils adds the contents of this variable to CCFLAGS and LINKFLAGS)
#	export ARCHFLAGS='-headerpad_max_install_names'

	if [[ "$(ld -v 2>&1 | grep -Eow 'PROJECT:.*')" == "PROJECT:ld64-264.3.101" ]]; then
		echo "You're running XCode 7.3, with a broken linker (version ld64-264.3.101): implementing a workaround for the @rpath expansion bug".
		XCODE_73_RPATH_BUG=1
	fi
fi

# Add Anaconda's library path to DYLD_LIBRARY_PATH, to make the libraries visible
# to the builds
if [[ "$OSTYPE" == darwin* ]]; then
	export DYLD_FALLBACK_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$CONDA_DEFAULT_ENV/lib"
else
	export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CONDA_DEFAULT_ENV/lib"
fi


############################################################################
# Build the package using eupspkg
#
PRODUCT=$(basename ups/*.table .table)
EUPS_VERSION="12.1+1"
PREFIX="$PREFIX/opt/lsst/$PRODUCT"

# initialize EUPS
source eups-setups.sh

# prepare
eupspkg PREFIX="$PREFIX" PRODUCT="$PRODUCT" VERSION="$EUPS_VERSION" FLAVOR=generic prep

# setup dependencies (just for the environmental variables, really)
# FIXME: a command should be added to eupspkg to just get the envvars
eups list

setup -r .
export

#
# make debugging easier -- if the build breaks, make it possible to chdir into the
# build directory and run ./_build.sh <verb>
#
cat > _build.sh <<-EOT
	#!/bin/bash
	$(export)

	# XCODE_73_RPATH_BUG workaround?
	if [[ "$XCODE_73_RPATH_BUG" == 1 ]]; then
	    trap '{ rm -f @rpath; rm -rf "$PREFIX/@rpath"; }' EXIT
	    ln -fs "\$CONDA_DEFAULT_ENV/lib" @rpath
	fi

	PRODUCT="$PRODUCT"
	EUPS_VERSION="$EUPS_VERSION"

	eupspkg PREFIX="$PREFIX" PRODUCT="$PRODUCT" VERSION="$EUPS_VERSION" FLAVOR=generic "\$@"
EOT
chmod +x _build.sh

# configure, build, install, declare to EUPS
./_build.sh config
./_build.sh build
./_build.sh install
./_build.sh decl

# Add EUPS tags.  The tags will be stored in a file in the product's ups
# dir; it will be merged by the pre-link.sh script with the EUPS database
# when the package is installed
TAGFILE="$EUPS_PATH/ups_db/global.tags"
for TAG in current conda; do
	# FIXME: This should be handled by the post-link/pre-delete script !!!
	test -f "$TAGFILE" && echo -n " " >> "$TAGFILE"
	echo -n "$TAG" >> "$TAGFILE"

	eups declare -t $TAG "$PRODUCT" "$EUPS_VERSION"
done
mv "$TAGFILE" "$PREFIX/ups"


############################################################################
# Binary preparation, directory cleanups
#

# compile all .py and .cfg files so they don't get picked up as new by conda
# when building other packages
if [[ -d "$PREFIX/python" ]]; then
	# don't fail in case of syntax errors, etc.
	"$PYTHON" -m compileall "$PREFIX/python" || true
fi
if ls "$PREFIX/ups"/*.cfg 1> /dev/null 2>&1; then
	"$PYTHON" -m py_compile "$PREFIX/ups"/*.cfg
fi
