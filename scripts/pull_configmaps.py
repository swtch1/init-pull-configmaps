from kubernetes import client, config, watch
import os
import sys
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def writeTextToFile(folder, filename, data):
    with open(folder +"/"+ filename, 'w') as f:
        f.write(data)
        f.close()


def request(url, method, payload):
    r = requests.Session()
    retries = Retry(total = 5,
            connect = 5,
            backoff_factor = 0.2,
            status_forcelist = [ 500, 502, 503, 504 ])
    r.mount('http://', HTTPAdapter(max_retries=retries))
    r.mount('https://', HTTPAdapter(max_retries=retries))
    if url is None:
        print("No url provided. Doing nothing.")
        # If method is not provided use GET as default
    elif method == "GET" or method is None:
        res = r.get("%s" % url, timeout=10)
        print ("%s request sent to %s. Response: %d %s" % (method, url, res.status_code, res.reason))
    elif method == "POST":
        res = r.post("%s" % url, json=payload, timeout=10)
        print ("%s request sent to %s. Response: %d %s" % (method, url, res.status_code, res.reason))


def removeFile(folder, filename):
    completeFile = folder +"/"+filename
    if os.path.isfile(completeFile):
        os.remove(completeFile)
    else:
        print("Error: %s file not found" % completeFile)


def download_cmap_files_with_label(label, targetFolder, current):
    v1 = client.CoreV1Api()
    namespace = os.getenv("NAMESPACE")
    if namespace is None:
        allCmaps = v1.list_namespaced_config_map(namespace=current)
    elif namespace == "ALL":
        allCmaps = v1.list_config_map_for_all_namespaces()
    else:
        allCmaps = v1.list_namespaced_config_map(namespace=namespace)
    for cm in allCmaps.items:
        if cm.metadata.labels is None:
            continue
        print('Working on configmap {}/{}'.format(cm.metadata.namespace, cm.metadata.name))
        if label in cm.metadata.labels.keys():
            print('Configmap has label {}'.format(label))
            if cm.data is None:
                print('configmap does not have data')
                continue
            for filename in cm.data.keys():
                print('File in configmap {}: {}'.format(cm.metadata.name, filename))
                writeTextToFile(targetFolder, filename, cm.data[filename])


def main():
    print("Starting config map collector")
    label = os.getenv('LABEL')
    if label is None:
        print("Should have added LABEL as environment variable! Exit")
        return -1
    targetFolder = os.getenv('FOLDER')
    if targetFolder is None:
        print("Should have added FOLDER as environment variable! Exit")
        return -1

    config.load_incluster_config()
    print("Config for cluster api loaded...")
    namespace = open("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read()
    download_cmap_files_with_label(label, targetFolder, namespace)

    # basic way to show all the files we've written
    print('### all files in FOLDER ###')
    for dirpath, dirnames, filenames in os.walk(targetFolder):
        if dirpath:
            print(dirpath + ':')
        if dirnames:
            for d in dirnames:
                print(d)
        if filenames:
            for f in filenames:
                print(f)
        print()


if __name__ == '__main__':
    main()
