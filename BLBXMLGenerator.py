from xml.etree.cElementTree import ElementTree as ET
import os
import argparse
import BLBFunctions


def parseArgs():
    _parser = argparse.ArgumentParser()
    _parser.add_argument("-r", "--renderMode", nargs='?', help="Sets renderMode")
    _parser.add_argument("-e", "--emission", nargs='?', help="Force Emission setting")
    _parser.add_argument("-uv", "--uv", nargs='+', help="Sets uvX value")
    _parser.add_argument("-s", "--scale", nargs='+', default=[1, 1], help="Sets scale values")
    return _parser.parse_args()


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

scaleModifier = args.scale
scaleModifier[0] = float(scaleModifier[0])
scaleModifier[1] = float(scaleModifier[1])

tree = ET()
archives = BLBFunctions.getArchives()

for archiveId, records in archives.items():
    for recordId, frames in records.items():
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
                    tree = tree.parse(xmlPath)
                    existingScale = findScale(tree)
                    # Apply modifier to existing scale values
                    newScale[0] = existingScale[0] * scaleModifier[0]
                    newScale[1] = existingScale[1] * scaleModifier[1]
                    if renderMode is None:
                        renderMode = findXMLValue(tree, "renderMode", renderMode)

                    existingUV = findUV(tree)
                    if uv is None and existingUV is not None:
                        uv = existingUV
                else:
                    # Apply modifier to default scale values
                    newScale[0] = newScale[0] * scaleModifier[0]
                    newScale[1] = newScale[1] * scaleModifier[1]

                newXML = generateXML(_renderMode=renderMode, _emission=emission, _uv=uv, _scale=newScale)
                strXML = "\n"
                strXML = strXML.join(newXML)
                with open(xmlPath, 'w') as f:
                    f.write(strXML)
