#### This uses WhisperX CPU to read an English MP3 file and turn it into a text file with 5 minute markers in the text

What I have used it for:

* Download a five hour podcast

* Turn this into a text file in less than 30 minutes on an AMD Ryzen 5 4500U with 8GB RAM

* Then feed this to an LLM and ask for a summary, or do a word search to find a section of the podcast

MP3toTXT uses the latest WhisperX and Pytorch CPU packages for surprisingly good speed and translation accuracy. It throw a time stamp in every five minutes to allow some rudimentary tracking between your MP3 and the transcript.

If you have a Cuda layer, I would suggest [Kit-Whisperx](https://github.com/rgcodeai/Kit-Whisperx) github, which is a beautiful app ever.  However, it is very slow, and when benchmarked against this script it requires higher weights for equal output.

The MP3ToTXT package uses the tiny.en weights, but in tests, it produce as good of accuracy as the medium in the Kit-Whisperx script.  I'm not sure why it does so well, but I encourage you to benchmark for yourself.

So, this is a quick and dirty answer if you don't have any speed.

When you run it, it will give warnings like

```python MP3toTXT.py
INFO:speechbrain.utils.quirks:Applied quirks (see `speechbrain.utils.quirks`): [disable_jit_profiling, allow_tf32]
INFO:speechbrain.utils.quirks:Excluded quirks specified by the `SB_DISABLE_QUIRKS` environment (comma-separated list): 
Model was trained with pyannote.audio 0.0.1, yours is 3.3.2. Bad things might happen unless you revert pyannote.audio to 0.x.
Model was trained with torch 1.10.0+cu102, yours is 2.6.0+cpu. Bad things might happen unless you revert torch to 1.x.
```

You don't need to worry about it.  It runs just fine.

Finally, it creates just a mess of text. So, you can run ppsplit script in the other repository to chunk it up and make it more readable.  Not necessary for an LLM to digest.

#### What Do I Need?

It needs FFMPEG.exe to run.  If you don't have it in your path, you are going to need to go and get it and download it.  I suggest that you can just simply put it by the python script if you don't install it and get it into your PATH env variable.  If you don't have it, when you run the script, it will give you a weird error message that doesn't look like "you're missing the FFMPEG.exe file."  So, put it in.

While the script is here, and you could "just run it," I think it is better to set up a virtual environment to run it in.  

Why?  Because It has a ton of dependancies, and you need to bring up a series of pytorch on CPU programs for it to run.

Once you have cloned the directory, I suggest that you do the following:

```Powershell
# 1. Install pyenv to manage the virtual environment.
# Most AI will help you pip the package.  It really simple once your understand it.

# 2. Restart PowerShell session
# Close and reopen PowerShell after pyvenv

# 3. cd to the clone github most likely MP3ToTXT subdirectory on your machine

# 4. Install Python 3.11.0
pyenv install 3.11.0

# 5. Set as local Python version
pyenv local 3.11.0

# 6. Create virtual environment but see below debugging to get it going
python -m venv MP3ToTXT 

# 7. Turn it on

.\MP3ToTXT\Scripts\Activate.ps1


# 8. Check to verify that you are running Python 3.11.0

python --version
```

What I will tell you is that you should immediately upgrade pip.

Start off by by installing whisperx 3.3.1.  This is a little fickle, and I may have installed it using a wheel.  However, you can try 

```powershell
pip install whisperx==3.3.1
```

If you have never done anything with pytorch, torch, and torchaudio, you are on the verge of being in "dependancy heck" because you need to blend python, whisperx, and other packages. I've settled on 3.11 for the virtual python environment, but I don't know if this is best.

Whatever you do, don't install torchvision because it creates a crazy dependancy matrix which is very hard to solve, and you don't need it for audio.

After you have installed whisperX, it will install a lot of the packages.

Other dependancies as per the Installed_Packages.txt file.Run the program

#### Why does the Main Script Look Weird and why do you have a SPEC file

While the current script works, it is in the process of being debugged so that I can compile it, insert FFMPEG into the .exe, and allow anybody to run it from a command line.  However, compiling from python script to .exe is a big task, and this is in a half built state

The good news it will run just fine as a Python script

The better news would be for somebody clone this and compile it, and let me know you got it as an EXE so the newbie can run it as an EXE.

Regardless, since I can't find another good / quick WhisperX git, I am leaving this here for somebody to use it or improve it
