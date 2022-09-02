from PIL import Image, ImageDraw
import BLBFunctions
import TransparentAnimatedGIFConverter
import os
import argparse


def parseArgs():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-af", "--archiveFilter", nargs='+', help="Target specific archive(s)")
    _parser.add_argument("-rf", "--recordFilter", nargs='+', help="Target specific record(s)")
    _parser.add_argument("-fps", "--framesPerSecond", nargs='?', help="Frames per second to determine frame duration")
    _args = _parser.parse_args()
    if _args.framesPerSecond is None:
        print("Supply at least the frames per second (-fps).")
        exit()
    return _args


args = parseArgs()
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
        durations = []
        for frameId, frame in frames.items():
            im = Image.open(frame["path"])
            images.append(im)
            durations.append(duration)
        gifPath = os.path.join(archivePath, str(archiveId) + "_" + str(recordId) + ".gif")
        print("Saving", gifPath, "with frame length ", duration)
        # images: List[Image], durations: Union[int, List[int]], save_file
        TransparentAnimatedGIFConverter.save_transparent_gif(images[1:], durations, gifPath)