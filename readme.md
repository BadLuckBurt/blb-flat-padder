#Setting up and using blb-flat-padder

To set up and run this script, please follow the steps below:

I've used Python 3.7 to develop but it probably works with newer v3s too. 

1. Install Python 3 ([https://www.python.org/downloads/release/python-379/](https://www.python.org/downloads/release/python-379/ "Python 3.7.9"))
2. Install the Pillow library ([https://pillow.readthedocs.io/en/stable/installation.html](https://pillow.readthedocs.io/en/stable/installation.html "Install Pillow"))

# WARNING: Any flats that are found are automatically processed by this script and it will overwrite the images present in the folder(s) it processes without warning.#

The script has been set up to check the sub-folders that are present in the folder where you execute the script from. It will process each sub-folder checking for images that follow the Daggerfall Unity naming pattern for flats. 

For example, if your folder structure looks like the below example, place the script in the Textures folder and run it from there. 

- Mod root folder\Textures\Enemy1
- Mod root folder\Textures\Enemy2
- Mod root folder\Textures\Enemy3  

After the script finishes you should see that the images for each enemy have been padded where necessary.