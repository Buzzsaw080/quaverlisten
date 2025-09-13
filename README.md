# QuaverListen
Simple python script to extract and name the songs from your entire quaver library for listening purposes without needing to open the game
## How to use
QuaverListen has no dependencies except for stdlib, so you just need to [Install Python](https://www.python.org/downloads/)
then clone the repository: `git clone https://github.com/Buzzsaw080/quaverlisten` (you can also click the green code button and press Download ZIP)
And then in a terminal with the folder you just downloaded
```bash
# Extract your songs, guessing the quaver install and outputting into a folder called output
python main.py --output-path output

# The above assumes you installed quaver through steam in the default path, if you installed it somewhere else you can specify that directory
python main.py --output-path output --quaver-path ~/Downloads/Quaver

# If you want your files to be named a certain way, you can change the format
# By default the format is {{ARTIST}} - {{TITLE}}
python main.py --output-path output --format "{{TITLE}}"
```
It will try to symlink the files, not using any extra storage space, but if you don't have permission to create symlinks (like on windows) it will fall back to copying the files