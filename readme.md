# Setting up and using these scripts

To set up and run this scripts, please follow the steps below:

I've used Python 3.7 to develop but it probably works with newer v3s too. 

1. Install Python 3 ([https://www.python.org/downloads/release/python-379/](https://www.python.org/downloads/release/python-379/ "Python 3.7.9"))
2. Install the Pillow library ([https://pillow.readthedocs.io/en/stable/installation.html](https://pillow.readthedocs.io/en/stable/installation.html "Install Pillow"))

# WARNING: Any flats that are found are automatically processed by BLBFlatPadder and it will overwrite the images present in the folder(s) it processes without warning.

The scripts have been set up to check the sub-folders that are present in the folder where you execute the script from. It will process each sub-folder checking for images that follow the Daggerfall Unity naming pattern for flats. 

For example, if your folder structure looks like the below example, place the script in the Textures folder and run it from there. 

- Mod root folder\Textures\Enemy1
- Mod root folder\Textures\Enemy2
- Mod root folder\Textures\Enemy3  

## BLBFlatPadder
This script will automatically find the max width and height of a set of frames and add padding to the images and the emissive image if present.

### Arguments

This script currently has no arguments

### Usage
Run the script using the following command in a terminal:
 
`python BLBFlatPadder.py`

## BLBXMLGenerator

This script can create and / or bulk edit existing XML files for flat archives.

### Arguments
All script arguments are optional but you must supply at least one argument to make your intentions clear.

1. `-ax True|False` or `--archiveXML True|False` set to True to generate archive XMLs, defaults to False
2. `-rx True|False` or `--recordXML True|False` set to True to generate record XMLs, default to True 
3. `-r Opaque|Cutout|Fade|Transparent` or `--renderMode Opaque|Cutout|Fade|Transparent`
set the render mode
4. `-e True|False` or `--emission True|False` force the emission boolean to true or false. When omitted and an emission 
image is found it will default to True
5. `-uv 0.0 0.0` or `--uv 0.0 0.0` specifies UV coordinates
6. `-sm 1.0 1.0` or `--scaleMultiplier 1.0 1.0` manipulate existing scale values using this multiplier. 
Default scale when creating a new XML is 1.0 for both scaleX and scaleY

### Usage examples

Below are a few usage examples: 

1. Generate / alter archive XMLs with scale 1.0: `python BLBXMLGenerator.py -ax True -rx False -sm 1 1`
2. Generate / alter record XMLs with scale 1.0: `python BLBXMLGenerator.py -sm 1 1`
3. Generate / alter both archive and record XMLs: `python BLBXMLGenerator.py -ax True -sm 1 1`
4. Add / alter render mode in archive XMLs only: `python BLBXMLGenerator.py -ax True -rx False -r Opaque`
5. Add / alter render mode in record XML: `python BLBXMLGenerator.py -r Cutout`

By mixing the arguments you should be able to cover any situation you encounter. 
If not, please let me know and I'll see what I can do.

## BLBGIFMaker

This script automatically generates GIFs.

### Arguments
You can use the following arguments to control which GIFs get generated:

1. `-a <archiveID>` or `--archiveIds <archiveID>` Controls which archives are processed, you can add multiple archive IDs 
separated by a blank space
2. `-r <recordID>` or `--recordIds <recordID>` Controls which records are processed, you can add multiple record IDs 
separated by a blank space
3. `-fps <integer>` or `--framesPerSecond <integer>` Specify at how many frames per second the animation runs
4. `-bg <0-255> <0-255> <0-255>` or `--backgroundColor <0-255> <0-255> <0-255>` The background color to use 
for the GIF in 0-255 RGB format