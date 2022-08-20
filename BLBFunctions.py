import os
import re
from PIL import Image


def getArchives():
    fileRegEx = r"^(\d+)\_(\d+)\-(\d+).(?:png|PNG)$"
    workDirectoryContents = os.scandir()

    archives = {}

    for entry in workDirectoryContents:
        if entry.is_dir():
            # print("Processing ", entry.path)
            directoryContents = os.scandir(entry.path)
            for obj in directoryContents:
                if obj.is_file():
                    fileName = obj.name
                    searchResult = re.search(fileRegEx, fileName)
                    if searchResult:
                        archiveId = searchResult.group(1)
                        if archiveId not in archives:
                            archives[archiveId] = {}
                            archives[archiveId]["path"] = entry.path

                        recordId = searchResult.group(2)
                        if recordId not in archives[archiveId]:
                            archives[archiveId][recordId] = {}

                        frame = searchResult.group(3)
                        if frame not in archives[archiveId][recordId]:
                            archives[archiveId][recordId][frame] = {}

                        filePath = obj.path
                        archives[archiveId][recordId][frame]["path"] = filePath
                        img = Image.open(filePath)
                        archives[archiveId][recordId][frame]["size"] = img.size
                        img.close()
    return archives
