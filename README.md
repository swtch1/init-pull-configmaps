# credit
originally forked from https://github.com/kiwigrid/k8s-sidecar and modified.

# Description
This is a docker container intended to run inside a kubernetes cluster to collect config maps with a specified label and
store the included files in an local folder. This container is intended to be run as an init container and pulls relevant
configmaps (those matching the label) into a specified directory.  The contained python script is working with the Kubernetes API 1.10

## Configuration Environment Variables

- `LABEL` 
  - description: Label that should be used for filtering
  - required: true
  - type: string

- `FOLDER`
  - description: Folder where the files should be placed
  - required: true
  - type: string

- `NAMESPACE`
  - description: If specified, the sidecar will search for config-maps inside this namespace. Otherwise the namespace in which the sidecar is running will be used. It's also possible to specify `ALL` to search in all namespaces.
  - required: false
  - type: string
