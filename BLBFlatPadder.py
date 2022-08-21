import os
import re
import math
import BLBFunctions
from PIL import Image


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new("RGBA", (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def find_frame_max(_frames):
    size = [0, 0]
    for _frameId, _frameData in _frames.items():
        # print(_frameData)
        size[0] = max(size[0], _frameData["size"][0])
        size[1] = max(size[1], _frameData["size"][1])
    return size


fileRegEx = r"^(\d+)\_(\d+)\-(\d+).(?:png|PNG)$"
workDirectory = os.getcwd()
workDirectoryContents = os.scandir()

archives = BLBFunctions.getArchives()

for archiveId, records in archives.items():
    for recordId, frames in records.items():
        if str(recordId) == "path":
            continue
        frameMax = find_frame_max(frames)
        for frameId, frame in frames.items():
            widthDifference = max(0, frameMax[0] - frame["size"][0])
            heightDifference = max(0, frameMax[1] - frame["size"][1])
            print("ArchiveID:", archiveId, "RecordID:", recordId, "FrameID:", frameId,
                  "Difference:", widthDifference, heightDifference)

            paddingLeft = math.floor(widthDifference / 2)
            paddingRight = widthDifference - paddingLeft
            paddingTop = heightDifference
            paddingBottom = 0

            emissivePath = frame["path"].replace(".png", "_Emission.png")
            if os.path.exists(emissivePath):
                img = Image.open(emissivePath)
                newImg = add_margin(img, paddingTop, paddingRight, paddingBottom, paddingLeft, (0, 0, 0, 0))
                img.close()
                newImg.save(emissivePath)
                newImg.close()

            img = Image.open(frame["path"])
            newImg = add_margin(img, paddingTop, paddingRight, paddingBottom, paddingLeft, (0, 0, 0, 0))
            img.close()
            newImg.save(frame["path"])
            newImg.close()

print("successfully padded all images")
