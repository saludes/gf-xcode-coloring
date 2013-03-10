set -e

# Assumes Xcode 4+.
XCODE_MAJOR_VERSION=`xcodebuild -version | awk 'NR == 1 {print substr($2,1,1)}'`
if [ "$XCODE_MAJOR_VERSION" -lt "4" ]; then
        echo "Xcode 4.x not found."
        exit 1
fi

# Path were this script is located
SCRIPT_PATH="$(dirname "$BASH_SOURCE")"

TEMPLATES_PATH="/Applications/Xcode.app/Contents/Developer/Library/Xcode/Templates/'File Templates'"

cp -r "$SCRIPT_PATH/Gf.xctemplate" "$TEMPLATES_PATH/Other/"