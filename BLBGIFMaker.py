from PIL import Image, ImageDraw
import BLBFunctions
import os
import argparse


def parseArgs():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-af", "--archiveFilter", nargs='+', help="Target specific archive(s)")
    _parser.add_argument("-rf", "--recordFilter", nargs='+', help="Target specific record(s)")
    _parser.add_argument("-fps", "--framesPerSecond", nargs='?', help="Frames per second to determine frame duration")
    _parser.add_argument("-bg", "--backgroundColor", nargs=3, help="Specify the RGB background color (range 0-255)")
    _args = _parser.parse_args()
    if _args.framesPerSecond is None or _args.backgroundColor is None:
        print("Supply at least a background color (-bg) and the frames per second (-fps).")
        exit()
    return _args


def removeTransparency(_img_path, _color=(0, 0, 0)):
    png = Image.open(_img_path).convert('RGBA')
    background = Image.new('RGBA', png.size, _color)
    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite_3 = alpha_composite.convert('RGB')
    return alpha_composite_3


args = parseArgs()
bg = (int(args.backgroundColor[0]), int(args.backgroundColor[1]), int(args.backgroundColor[2]))
fps = int(args.framesPerSecond)
archives = BLBFunctions.getArchives()
for archiveId, records in archives.items():
    if args.archiveFilter is not None:
        if archiveId not in args.archiveFilter:
            continue
    archivePath = ""
    for recordId, frames in records.items():
        if str(recordId) == "path":
            archivePath = frames
            continue

        if args.recordFilter is not None:
            if recordId not in args.recordFilter:
                continue

        images = []
        frameCount = len(frames.items())
        if frameCount < 2:
            continue
        duration = (1 / fps) * 1000
        for frameId, frame in frames.items():
            im = removeTransparency(frame["path"], bg)
            images.append(im)
        gifPath = os.path.join(archivePath, str(archiveId) + "_" + str(recordId) + ".gif")
        print("Saving", gifPath, "with frame length ", duration)
        images[0].save(gifPath, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
