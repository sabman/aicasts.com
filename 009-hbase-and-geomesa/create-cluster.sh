KeyName=${KeyName:-external-devops}
SubnetId=${SubnetId:-subnet-84b197ed}
export CID=$(
aws emr create-cluster                                                         \
--name "GeoMesa HBase on S3"                                                   \
--release-label emr-5.5.0                                                      \
--output text                                                                  \
--use-default-roles                                                            \
--ec2-attributes KeyName=$KeyName,SubnetId=$SubnetId                           \
--applications Name=Hadoop Name=Zookeeper Name=Spark Name=HBase                \
--instance-groups                                                              \
  Name=Master,InstanceCount=1,InstanceGroupType=MASTER,InstanceType=m4.large   \
  Name=Workers,InstanceCount=3,InstanceGroupType=CORE,InstanceType=m4.large    \
--configurations file://./geomesa-hbase-on-s3.json                             \
)
