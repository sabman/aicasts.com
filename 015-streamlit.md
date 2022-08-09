```
pip install streamlit
streamlit hello
```

- https://towardsdatascience.com/build-an-app-to-synthesize-photorealistic-faces-using-tensorflow-and-streamlit-dd2545828021
- https://awesome-streamlit.org/
- https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
- https://towardsdatascience.com/how-to-deploy-your-data-science-as-web-apps-easily-with-python-955dd462a9b5

- https://www.rockyourcode.com/run-streamlit-with-docker-and-docker-compose/
- https://github.com/streamlit/streamlit/issues/837 (running behind nginx)
- https://discuss.streamlit.io/search?q=multiple%20apps

```conf
 location ~* /streamlit.* {
    proxy_pass http://127.0.0.1:8501;

    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Real-IP $remote_addr;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header  Referer  http://localhost;
    proxy_set_header Origin "";
  }
```

```conf
[program:streamlit]
user=sammy
environment=HOME=/home/sammy
directory=/home/sammy/environments/streamlit_apps
priority=500
command=/bin/bash -c 'source /home/sammy/environments/my_env/bin/activate && streamlit hello'
```

Streamlit config https://github.com/ysraell/examples/blob/d39e4f8cfada8217bd8b9b146f6f42605f839214/Streamlit_DEMO/config.toml

```sh
(my_env) sammy@fa54e25df4ea:~/environments$ streamlit config show
```

```toml
# Below are all the sections and options you can have in ~/.streamlit/config.toml.

[global]

# By default, Streamlit checks if the Python watchdog module is available and, if not, prints a warning asking for you to install it. The watchdog module is not required, but highly recommended. It improves Streamlit's ability to detect changes to files in your filesystem.
# If you'd like to turn off this warning, set this to True.
# Default: false
# The value below was set in /home/sammy/.streamlit/config.toml
disableWatchdogWarning = false

# Configure the ability to share apps to the cloud.
# Should be set to one of these values: - "off" : turn off sharing. - "s3" : share to S3, based on the settings under the [s3] section of this config file. - "file" : share to a directory on the local machine. This is meaningful only for debugging Streamlit itself, and shouldn't be used for production.
# Default: "off"
# The value below was set in /home/sammy/.streamlit/config.toml
sharingMode = "off"

# If True, will show a warning when you run a Streamlit-enabled script via "python my_script.py".
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
showWarningOnDirectExecution = true

# Level of logging: 'error', 'warning', 'info', or 'debug'.
# Default: 'info'
# The value below was set in /home/sammy/.streamlit/config.toml
logLevel = "info"


[client]

# Whether to enable st.cache.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
caching = true

# If false, makes your Streamlit script not draw to a Streamlit app.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
displayEnabled = true


[runner]

# Allows you to type a variable or string by itself in a single line of Python code to write it to the app.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
magicEnabled = true

# Install a Python tracer to allow you to stop or pause your script at any point and introspect it. As a side-effect, this slows down your script's execution.
# Default: false
# The value below was set in /home/sammy/.streamlit/config.toml
installTracer = false

# Sets the MPLBACKEND environment variable to Agg inside Streamlit to prevent Python crashing.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
fixMatplotlib = true


[server]

# List of folders that should not be watched for changes. This impacts both "Run on Save" and @st.cache.
# Relative paths will be taken as relative to the current working directory.
# Example: ['/home/user1/env', 'relative/path/to/folder']
# Default: []
# The value below was set in /home/sammy/.streamlit/config.toml
folderWatchBlacklist = []

# Change the type of file watcher used by Streamlit, or turn it off completely.
# Allowed values: * "auto" : Streamlit will attempt to use the watchdog module, and falls back to polling if watchdog is not available. * "watchdog" : Force Streamlit to use the watchdog module. * "poll" : Force Streamlit to always use polling. * "none" : Streamlit will not watch files.
# Default: "auto"
# The value below was set in /home/sammy/.streamlit/config.toml
fileWatcherType = "auto"

# If false, will attempt to open a browser window on start.
# Default: false unless (1) we are on a Linux box where DISPLAY is unset, or (2) server.liveSave is set.
# The value below was set in /home/sammy/.streamlit/config.toml
headless = true

# Immediately share the app in such a way that enables live monitoring, and post-run analysis.
# Default: false
# The value below was set in /home/sammy/.streamlit/config.toml
liveSave = false

# Automatically rerun script when the file is modified on disk.
# Default: false
# The value below was set in /home/sammy/.streamlit/config.toml
runOnSave = false

# The address where the server will listen for client and browser connections. Use this if you want to bind the server to a specific address. If set, the server will only be accessible from this address, and not from any aliases (like localhost).
# Default: (unset)
#address =

# The port where the server will listen for browser connections.
# Default: 8501
# The value below was set in /home/sammy/.streamlit/config.toml
port = 8501

# The base path for the URL where Streamlit should be served from.
# Default: ""
# The value below was set in /home/sammy/.streamlit/config.toml
baseUrlPath = "/streamlit"

# Enables support for Cross-Origin Request Sharing, for added security.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
enableCORS = true

# Max size, in megabytes, for files uploaded with the file_uploader.
# Default: 200
# The value below was set in /home/sammy/.streamlit/config.toml
maxUploadSize = 200


[browser]

# Internet address where users should point their browsers in order to connect to the app. Can be IP address or DNS name and path.
# This is used to: - Set the correct URL for CORS purposes. - Show the URL on the terminal - Open the browser - Tell the browser where to connect to the server when in liveSave mode.
# Default: 'localhost'
# The value below was set in /home/sammy/.streamlit/config.toml
serverAddress = "localhost"

# Whether to send usage statistics to Streamlit.
# Default: true
# The value below was set in /home/sammy/.streamlit/config.toml
gatherUsageStats = true

# Port where users should point their browsers in order to connect to the app.
# This is used to: - Set the correct URL for CORS purposes. - Show the URL on the terminal - Open the browser - Tell the browser where to connect to the server when in liveSave mode.
# Default: whatever value is set in server.port.
# The value below was set in /home/sammy/.streamlit/config.toml
serverPort = 8501


[mapbox]

# Configure Streamlit to use a custom Mapbox token for elements like st.deck_gl_chart and st.map. If you don't do this you'll be using Streamlit's own token, which has limitations and is not guaranteed to always work. To get a token for yourself, create an account at https://mapbox.com. It's free! (for moderate usage levels)
# Default: ""
# The value below was set in /home/sammy/.streamlit/config.toml
token = ""


[s3]

# Name of the AWS S3 bucket to save apps.
# Default: (unset)
#bucket =

# URL root for external view of Streamlit apps.
# Default: (unset)
#url =

# Access key to write to the S3 bucket.
# Leave unset if you want to use an AWS profile.
# Default: (unset)
#accessKeyId =

# Secret access key to write to the S3 bucket.
# Leave unset if you want to use an AWS profile.
# Default: (unset)
#secretAccessKey =

# The "subdirectory" within the S3 bucket where to save apps.
# S3 calls paths "keys" which is why the keyPrefix is like a subdirectory. Use "" to mean the root directory.
# Default: ""
# The value below was set in /home/sammy/.streamlit/config.toml
keyPrefix = ""

# AWS region where the bucket is located, e.g. "us-west-2".
# Default: (unset)
#region =

# AWS credentials profile to use.
# Leave unset to use your default profile.
# Default: (unset)
#profile =
```

To run behind a proxy change
baseUrlPath = "/streamlit"

---

https://towardsdatascience.com/build-an-app-to-synthesize-photorealistic-faces-using-tensorflow-and-streamlit-dd2545828021

```
git clone https://github.com/streamlit/demo-face-gan.git
cd demo-face-gan
pip install -r requirements.txt
streamlit run app.py
```

## App Structure

```python
def main():
    st.title("Streamlit Face-GAN Demo")

    # Step 1. Download models and data files.
    for filename in EXTERNAL_DEPENDENCIES.keys():
        download_file(filename)

    # Step 2. Read in models from the data files.
    tl_gan_model, feature_names = load_tl_gan_model()
    session, pg_gan_model = load_pg_gan_model()

    # Step 3. Draw the sidebar UI.
    ...
    features = ...  # Internally, this uses st.sidebar.slider(), etc.

    # Step 4. Synthesize the image.
    with session.as_default():
        image_out = generate_image(session, pg_gan_model, tl_gan_model,
                features, feature_names)

    # Step 5. Draw the synthesized image.
    st.image(image_out, use_column_width=True)
```

1. Download model files
2.

```py
#  If the file exists and has the expected size, return.
if os.path.exists(file_path):
    if "size" not in EXTERNAL_DEPENDENCIES[file_path]:
        return
    elif os.path.getsize(file_path) == EXTERNAL_DEPENDENCIES[file_path]["size"]:
        return

```

Draw download UI

```py
# Draw UI elements.
weights_warning = st.warning("Downloading %s..." % file_path)
progress_bar = st.progress(0)

with open(file_path, "wb") as output_file:
    with urllib.request.urlopen(...) as response:

        ...

        while True:

            ...  # Save downloaded bytes to file here.

            # Update UI elements.
            weights_warning.warning(
                "Downloading %s... (%6.2f/%6.2f MB)" %
                (file_path, downloaded_size))
            progress_bar.progress(downloaded_ratio)
...

# Clear UI elements when done.
weights_warning.empty()
progress_bar.empty()
```
