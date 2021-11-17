https://github.com/OpenDroneMap/WebODM

```
git clone https://github.com/OpenDroneMap/WebODM --config core.autocrlf=input --depth 1
cd WebODM
./webodm.sh start
```

https://dronemapper.com/blog/

Understanding `./webodm.sh` see https://github.com/OpenDroneMap/WebODM/blob/master/webodm.sh

```bash

#!/bin/bash
set -eo pipefail
__dirname=$(cd $(dirname "$0"); pwd -P)
cd "${__dirname}"


```
