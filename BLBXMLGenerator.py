from xml.etree.cElementTree import ElementTree as ET
import os
import argparse
import BLBFunctions


def parseArgs():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-ax", "--archiveXML", nargs='?', default='False', help="Generates XML at archive level")
    _parser.add_argument("-rx", "--recordXML", nargs='?', default='True', help="Generates XML at record level")
    _parser.add_argument("-r", "--renderMode", nargs='?', help="Sets renderMode")
    _parser.add_argument("-e", "--emission", nargs='?', help="Force Emission setting")
    _parser.add_argument("-uv", "--uv", nargs=2, help="Sets uvX value")
    _parser.add_argument("-sm", "--scaleMultiplier", nargs=2, help="Multiplies scale values")
    _args = _parser.parse_args()
    if (
            _args.renderMode is None and
            _args.emission is None and
            _args.uv is None and
            _args.scaleMultiplier
    ) is None:
        print("No script arguments found. Ending script execution. Please supply at least one argument.")
        exit()
    return _args


def generateXML(_renderMode=None, _emission=None, _uv=None, _scale=None):
    _xml = ["<?xml version=\"1.0\"?>", "<info>"]
    if _renderMode is not None:
        _xml.append("\t<renderMode>" + str(_renderMode) + "</renderMode>")
    if _emission is not None:
        _xml.append("\t<emission>" + str(_emission) + "</emission>")
    if _uv is not None:
        _xml.append("\t<uvX>" + str(_uv[0]) + "</uvX>")
        _xml.append("\t<uvY>" + str(_uv[1]) + "</uvY>")
    if _scale is not None:
        _xml.append("\t<scaleX>" + str(_scale[0]) + "</scaleX>")
        _xml.append("\t<scaleY>" + str(_scale[1]) + "</scaleY>")
    _xml.append("</info>")
    return _xml


def findScale(_xml):
    return [float(findXMLValue(_xml, "scaleX", "1")), float(findXMLValue(_xml, "scaleY", "1"))]


def findUV(_xml):
    _uvX = findXMLValue(_xml, "uvX", None)
    _uvY = findXMLValue(_xml, "uvY", None)
    if _uvX is not None and _uvY is not None:
        return [float(_uvX), float(_uvY)]
    return None


def findXMLValue(_xml, _tag, _default):
    for _i in range(0, len(_xml)):
        if _xml[_i].tag == _tag:
            return _xml[_i].text
    return _default


args = parseArgs()

renderMode = args.renderMode
emission = args.emission
if emission is not None:
    emission = str.capitalize(emission)
uv = args.uv
if uv is not None:
    uv[0] = float(uv[0])
    uv[1] = float(uv[1])

scaleMultiplier = args.scaleMultiplier
if scaleMultiplier is None:
    scaleMultiplier = [1, 1]
scaleMultiplier[0] = float(scaleMultiplier[0])
scaleMultiplier[1] = float(scaleMultiplier[1])

archives = BLBFunctions.getArchives()

for archiveId, records in archives.items():
    for recordId, frames in records.items():
        if str(recordId) == "path":
            if args.archiveXML == "True":
                xmlPath = os.path.join(frames, str(archiveId) + ".xml")
                newScale = [1, 1]
                if os.path.exists(xmlPath):
                    tree = ET()
                    tree = tree.parse(xmlPath)

                    existingScale = findScale(tree)
                    # Apply modifier to existing scale values
                    newScale[0] = existingScale[0] * scaleMultiplier[0]
                    newScale[1] = existingScale[1] * scaleMultiplier[1]
                    if renderMode is None:
                        renderMode = findXMLValue(tree, "renderMode", renderMode)

                    existingUV = findUV(tree)
                    if uv is None and existingUV is not None:
                        uv = existingUV
                else:
                    # Apply modifier to default scale values
                    newScale[0] = newScale[0] * scaleMultiplier[0]
                    newScale[1] = newScale[1] * scaleMultiplier[1]

                newXML = generateXML(_renderMode=renderMode, _emission=emission, _uv=uv, _scale=newScale)
                strXML = "\n"
                strXML = strXML.join(newXML)
                with open(xmlPath, 'w') as f:
                    f.write(strXML)
            continue

        if args.recordXML == "False":
            continue

        for frameId, frame in frames.items():
            if int(frameId) == 0:
                # change emission setting based on emission image existence
                emissivePath = frame["path"].replace(".png", "_Emission.png")
                if os.path.exists(emissivePath) and emission is None:
                    emission = True

                # check for existing XML
                newScale = [1, 1]
                xmlPath = frame["path"].replace(".png", ".xml")
                if os.path.exists(xmlPath):
                    tree = ET()
                    tree = tree.parse(xmlPath)

                    existingScale = findScale(tree)
                    # Apply modifier to existing scale values
                    newScale[0] = existingScale[0] * scaleMultiplier[0]
                    newScale[1] = existingScale[1] * scaleMultiplier[1]
                    if renderMode is None:
                        renderMode = findXMLValue(tree, "renderMode", renderMode)

                    existingUV = findUV(tree)
                    if uv is None and existingUV is not None:
                        uv = existingUV
                else:
                    # Apply modifier to default scale values
                    newScale[0] = newScale[0] * scaleMultiplier[0]
                    newScale[1] = newScale[1] * scaleMultiplier[1]

                newXML = generateXML(_renderMode=renderMode, _emission=emission, _uv=uv, _scale=newScale)
                strXML = "\n"
                strXML = strXML.join(newXML)
                with open(xmlPath, 'w') as f:
                    f.write(strXML)
