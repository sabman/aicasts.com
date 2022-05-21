# The following command is optional, to make kfctl binary easier to use.
export PATH=$PATH:/Users/shoaib/code/aicasts/aicasts.com/017-kubeflow

# Set KF_NAME to the name of your Kubeflow deployment. This also becomes the
# name of the directory containing your configuration.
# For example, your deployment name can be 'my-kubeflow' or 'kf-test'.
export KF_NAME=kf-geodb-v1

# Set the path to the base directory where you want to store one or more
# Kubeflow deployments. For example, /opt/.
# Then set the Kubeflow application directory for this deployment.
export BASE_DIR=/Users/shoaib/code/aicasts/aicasts.com/017-kubeflow/opt
export KF_DIR=${BASE_DIR}/${KF_NAME}

# Set the configuration file to use, such as the file specified below:
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.0-branch/kfdef/kfctl_k8s_istio.v1.0.2.yaml"

# Generate and deploy Kubeflow:
mkdir -p ${KF_DIR}
cd ${KF_DIR}
kfctl apply -V -f ${CONFIG_URI}

# Tutorial: From Notebook to Kubeflow Pipelines to KFServing: the Data Science... - Karl Weinmeister
# https://www.youtube.com/watch?v=VDINH5WkBhA