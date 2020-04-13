```
pip install streamlit
streamlit hello
```

- https://awesome-streamlit.org/
- https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
- https://towardsdatascience.com/how-to-deploy-your-data-science-as-web-apps-easily-with-python-955dd462a9b5

- https://www.rockyourcode.com/run-streamlit-with-docker-and-docker-compose/
- https://github.com/streamlit/streamlit/issues/837 (running behind nginx)


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