#!/usr/bin/env python

import requests
import sys

def main():
   registry = "http://127.0.0.1:5000"
   image = sys.argv[1]
   res = requests.get(registry + "/v2/")
   assert res.status_code == 200

   res = requests.get(registry + "/v2/_catalog?n=1000")
   assert res.status_code == 200
   repositories = res.json().get("repositories", [])

   for repository in repositories:
      if repository == image:
         print("repository {} found".format(repository))
         res = requests.get(registry + "/v2/{}/tags/list".format(repository))
         #assert res.status_code == 200
         tags = res.json().get("tags", None)

         if tags:
            for tag in tags:
               print("begin deleting %s ......"%(format(repository)+':'+format(tag)))
               res = requests.get(registry + "/v2/{}/manifests/{}".format(repository, tag), headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})
               blobs = [e["blobSum"] for e in res.json().get("fsLayers",  [])]
               #print res.status_code
               digest = res.headers.get("Docker-Content-Digest", None)
               #assert digest
               print("deleting blobs...")
               for blob in blobs:
                  res = requests.delete(registry + "/v2/{}/blobs/{}".format(repository, blob))
                  print(res)
               print("deleting manifest...")
               res = requests.delete(registry + "/v2/{}/manifests/{}".format(repository, digest))
               if res.status_code == 202:
                  print "delete %s success......"%(format(repository)+':'+format(tag))
               else:
                  print "delete %s fail......"%(format(repository)+':'+format(tag))
         else:
            print("no tags to clean")

if __name__ == "__main__":
   main()
