# Comms Cloud Deployer

This script will help you to dynamically generate .yaml file with manifest paths to use with vlocity build tool. Thanks
to that you are able to deploy only those files that was changed or added since last deployment.


### Requirements
+ Python 3.9

### Clone and Setup
You can quickly get CommsCloudDeployer by following these steps:

1. Clone the repository:
    ```commandline
    git clone https://github.com/kacperosko/CommsCloudDeployer.git
    cd CommsCloudDeployer
    ```
2. Install the required dependencies:
    ```commandline
    pip3 install -r requirements.txt
    ```
3. Move CommsCloudDeployer inside Your repository catalog
    ```commandline
    mv -f CommsCloudDeployer PATH_TO_YOUR_REPO
    ```
4. Run the command
      ```commandline
      python3 CommsCloudDeployer.py --branch BRANCH_NAME --catalog COMMS_CLOUD_CATALOG_NAME --org TARGET_ORG_DEPLOYMENT --tagOnly N
    ```
#
To check required flags in command use help:
```commandline
python3 CommsCloudDeployer.py --help
usage: Comms Cloud Deployer [-h] -b BRANCH -o ORG -c CATALOG -t TAGONLY

Generate .yaml file with manifest files to deploy

options:
  -h, --help                      show this help message and exit
  -b BRANCH, --branch BRANCH      Name of the branch
  -o ORG, --org ORG               Name of the target Org
  -c CATALOG, --catalog CATALOG   Name of the catalog for Communications Cloud data
  -t TAGONLY, --tagOnly TAGONLY   Create only the new tag
```

You can also turn off generating dynamic .yaml by setting below flag in [settings.py](settings.py) to False:
```python
# Mark this to False if you want to skip retrieving diff and generating manifest file
MANIFEST_ONLY = True # by default this value is True
```
### Script Result

That's the result of run the CommsCloudDeployer:
```yaml
projectPath: ./CC
oauthConnection: true
activate: true
separateProducts: true
manifestOnly: true
manifest:
  - DataRaptor/sample_getAccounts
  - DataRaptor/sample_createQuote
  - Product2/000111222333-0bd8-eeee-000
```


### Example use

Here is an example of configuration in bitbucket pipelines. The whole catalog of CommsCloudDeployer is put inside repo project.

Sample project file tree:
```bash
.
repository_catalog
├── some_files.txt
├── salesforce_catalog
├── comms_cloud_catalog   <---- Comms Cloud Catalog
│   ├── DataRaptor
│   ├── Product2
│   └── etc
│
├── scripts
│   ├── some_scripts
│   └── CommsCloudDeployer    <--- Comms cloud deployer project catalog
│       ├── CommsCloudDeployer.py
│       └── resources
│
├── README.md
├── PyCommsCloud.yaml  <----- here is the result of Comms Cloud Deployer
└── pipelines.yml
```

Pipelines configuration:
```yaml
definitions:
  scripts:
    deployVlocity: &deployVlocity |
      vlocity -sfdx.username USERNAME -job ./PyCommsCloud.yaml packDeploy # <----- add PyCommsCloud.yaml as job file
    generateDynamicManifest: &generateDynamicManifest |
      python3 ./scripts/CommsCloudDeployer/CommsCloudDeployer.py \
        --branch $BITBUCKET_BRANCH --catalog comms_cloud_catalog --org QA --tagOnly N
      cat PyCommsCloud.yaml 
    createTagForDynamicManifest: &createTagForDynamicManifest |
      python3 ./scripts/CommsCloudDeployer/CommsCloudDeployer.py \
        --branch $BITBUCKET_BRANCH --catalog comms_cloud_catalog --org QA --tagOnly Y

  steps:
    - step: &deployVlocityStep
        name: Deploy Vlocity
        script:
          - *generateDynamicManifest # <-------- HERE IS COMMS CLOUD DEPLOYER START
          - *deployVlocity
          - *createTagForDynamicManifest  # <-------- HERE IS COMMS CLOUD DEPLOYER END
    
pipelines:
  custom: 
    deploy-vlocity:
      - step: *deployVlocityStep
```