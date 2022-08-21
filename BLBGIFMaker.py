from PIL import Image, ImageDraw
import BLBFunctions
import os
import argparse


def parseArgs():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-a", "--archiveId", nargs='?', help="Target a specific archive")
    _parser.add_argument("-r", "--recordId", nargs='?', help="Target a specific record")
    _parser.add_argument("-fps", "--framesPerSecond", nargs='?', help="Frames per second to determine frame duration")
    _args = _parser.parse_args()
    if _args.framesPerSecond is None:
        print("No script arguments found. Ending script execution. Please supply the frames per second at least.")
        exit()
    return _args


def removeTransparency(_img_path, _color=(0, 0, 0)):
    png = Image.open(_img_path).convert('RGBA')
    background = Image.new('RGBA', png.size, _color)
    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite_3 = alpha_composite.convert('RGB')
    return alpha_composite_3


args = parseArgs()
fps = int(args.framesPerSecond)
archives = BLBFunctions.getArchives()
for archiveId, records in archives.items():
    if args.archiveId is not None:
        if archiveId != args.archiveId:
            continue
    archivePath = ""
    for recordId, frames in records.items():
        if str(recordId) == "path":
            archivePath = frames
            continue

        if args.recordId is not None:
            if recordId != args.recordId:
                continue

        images = []
        frameCount = len(frames.items())
        if frameCount < 2:
            continue
        duration = (1 / fps) * 1000
        for frameId, frame in frames.items():
            im = removeTransparency(frame["path"])
            images.append(im)
        gifPath = os.path.join(archivePath, str(archiveId) + "_" + str(recordId) + ".gif")
        print("Saving", gifPath, "with frame length ", duration)
        images[0].save(gifPath, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
