https://dokku.com/

```sh
 # download the installation script

wget -NP . https://dokku.com/bootstrap.sh

# run the installer

sudo DOKKU_TAG=v0.35.20 bash bootstrap.sh

# Configure your server domain

dokku domains:set-global dokku.me

# and your ssh key to the dokku user

PUBLIC_KEY="your-public-key-contents-here"

echo "$PUBLIC_KEY" | dokku ssh-keys:add admin

# create your first app and you're off!

dokku apps:create test-app 
```