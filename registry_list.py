#!/usr/bin/env python
import requests
#import simplejson as json
import json
import sys

def main():
  registry = "http://127.0.0.1:5000"
  res = requests.get(registry + "/v2/")
  assert res.status_code == 200

  res = requests.get(registry + "/v2/_catalog?n=1000")
  assert res.status_code == 200
  repositories = res.json().get("repositories", [])
  #print("registry reports {} repositories".format(len(repositories)))

  for repository in repositories:
    res = requests.get(registry + "/v2/{}/tags/list".format(repository))
    #assert res.status_code == 200
    tags = res.json().get("tags", None)
    if tags:
      for tag in tags:
        image = format(repository)
        tag = format(tag)
        if len(sys.argv) < 2:  #list all docker registry images tag
           print (image + ":" + tag)
        else:
           imagecatalog = sys.argv[1]
	   if image.startswith(imagecatalog):
              print (image)

if __name__ == "__main__":
  main()
