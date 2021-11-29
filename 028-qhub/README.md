https://github.com/Quansight/qhub

Components
The technology stack is an integration of the following existing open source libraries:

- Terraform a tool for building, changing, and versioning infrastructure.

- Kubernetes a cloud-agnostic orchestration system

Helm: a package manager for Kubernetes

JupyterHub: a shareable compute platform for data science

JupyterLab: a web-based interactive development environment for Jupyter Notebooks

Dask: a scalable and flexible library for parallel computing in Python

Dask-Gateway: a secure, multi-tenant server for managing Dask clusters

traefik for routing web/tcp traffic inside cluster

traefik-forward-auth single sign on and easy securing of web applications

GitHub Actions: a tool to automate, customize, and execute software development workflows in a GitHub repository.

Amongst the newly created open source libraries on the tech stack are:

jupyterhub-ssh brings the SSH experience to a modern cluster manager.

jupyter-videochat allows video-chat with JupyterHub peers inside JupyterLab, powered by Jitsi.

conda-store serves identical conda environments and controls its life-cycle.

conda-docker, an extension to the docker concept of having declarative environments that are associated with Docker images allowing tricks and behaviour that otherwise would not be allowed.

vscode built-in web editor tied to jupyterlab server

Integrations
In an effort for QHub to serve as a core that services can integrate with.

prefect workflow management

clearml machine learning platform

prometheus cluster monitoring

grafana cluster monitoring visualizations

Why use QHub?
QHub provides enables teams to build their own scalable compute infrastructure with:

Easy installation and maintenance controlled by a single configuration file.

Autoscaling JupyterHub installation deployed on the Cloud provider of your choice.

Option to choose from multiple compute instances, such as: namely normal, high memory, GPU, etc.

Autoscaling Dask compute clusters for big data using any instance type.

Shell access and remote editing access (i.e. VSCode remote) through KubeSSH.

Full linux style permissions allowing for different shared folders for different groups of users.

Robust compute environment handling allowing both prebuilt and ad-hoc environment creation.

- Integrated video conferencing, using Jitsi.
