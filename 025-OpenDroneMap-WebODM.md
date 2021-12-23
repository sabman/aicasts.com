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

# define realpath replacement function
if [[ $platform = "MacOS / OSX" ]]; then
    realpath() {
        [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
    }
fi

# Load default values
source "${__dirname}/.env"
DEFAULT_PORT="$WO_PORT"
DEFAULT_HOST="$WO_HOST"
DEFAULT_MEDIA_DIR="$WO_MEDIA_DIR"
DEFAULT_SSL="$WO_SSL"
DEFAULT_SSL_INSECURE_PORT_REDIRECT="$WO_SSL_INSECURE_PORT_REDIRECT"
DEFAULT_BROKER="$WO_BROKER"


# Parse args for overrides
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --port)
    export WO_PORT="$2"
    shift # past argument
    shift # past value
    ;;    
    --hostname)
    export WO_HOST="$2"
    shift # past argument
    shift # past value
    ;;
	--media-dir)
    export WO_MEDIA_DIR=$(realpath "$2")
    shift # past argument
    shift # past value
    ;;
    --ssl)
    export WO_SSL=YES
    shift # past argument
    ;;
	--ssl-key)
    export WO_SSL_KEY=$(realpath "$2")
    shift # past argument
    shift # past value
    ;;
	--ssl-cert)
    export WO_SSL_CERT=$(realpath "$2")
    shift # past argument
    shift # past value
    ;;
	--ssl-insecure-port-redirect)
    export WO_SSL_INSECURE_PORT_REDIRECT="$2"
    shift # past argument
    shift # past value
    ;;
    --debug)
    export WO_DEBUG=YES
    shift # past argument
    ;;
    --dev-watch-plugins)
    export WO_DEV_WATCH_PLUGINS=YES
    shift # past argument
    ;;
    --dev)
    export WO_DEBUG=YES
    export WO_DEV=YES
    dev_mode=true
    shift # past argument
    ;;    
	--gpu)
    gpu=true
    shift # past argument
    ;;
	--broker)
    export WO_BROKER="$2"
    shift # past argument
    shift # past value
    ;;
    --no-default-node)
    default_nodes=0
    echo "ATTENTION: --no-default-node is deprecated. Use --default-nodes instead."
    export WO_DEFAULT_NODES=0
    shift # past argument
    ;;
    --with-micmac)
    load_micmac_node=true
    shift # past argument
    ;;
    --detached)
    detached=true
    shift # past argument
    ;;
    --default-nodes)
    default_nodes="$2"
    export WO_DEFAULT_NODES="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done

````
