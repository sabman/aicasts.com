https://github.com/OpenDroneMap/WebODM

```sh
git clone https://github.com/OpenDroneMap/WebODM --config core.autocrlf=input --depth 1
cd WebODM
./webodm.sh start
```

https://dronemapper.com/blog/

Understanding `./webodm.sh` see https://github.com/OpenDroneMap/WebODM/blob/master/webodm.sh

````bash

#!/bin/bash

# https://gist.github.com/maxisam/e39efe89455d26b75999418bf60cf56c
# set -e The set -e option instructs bash to immediately exit if any command [1] has a non-zero exit status.
# set -o pipefail this setting prevents errors in a pipeline from being masked. If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline. By default, the pipeline's return code is that of the last command even if it succeeds. Imagine finding a sorted list of matching lines in a file

# ```
# $ grep some-string /non/existent/file | sort
# grep: /non/existent/file: No such file or directory
# % echo $?
# 0
# ```
# Here, grep has an exit code of 2, writes an error message to stderr, and an empty string to stdout.
# This empty string is then passed through sort, which happily accepts it as valid input, and returns a status code of 0.
# This is fine for a command line, but bad for a shell script: you almost certainly want the script to exit right then with a nonzero exit code... like this:
# ```
# $ set -o pipefail
# $ grep some-string /non/existent/file | sort
# grep: /non/existent/file: No such file or directory
# $ echo $?
# 2
# ```
set -eo pipefail
__dirname=$(cd $(dirname "$0"); pwd -P)
cd "${__dirname}"

platform="Linux" # Assumed
uname=$(uname)
case $uname in
	"Darwin")
	platform="MacOS / OSX"
	;;
	MINGW*)
	platform="Windows"
	;;
esac

if [[ $platform = "Windows" ]]; then
	export COMPOSE_CONVERT_WINDOWS_PATHS=1
fi

default_nodes=1
dev_mode=false
gpu=false

````
