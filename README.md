#### This uses WhisperX CPU to read an English MP3 file and turn it into a text file with 5 minute markers in the text

What I have used it for:

* Download a five hour podcast

* Turn this into a text file in less than 30 minutes on an AMD Ryzen 5 4500U with 8GB RAM

* Then feed this to an LLM and ask for a summary, or do a word search to find a section of the podcast

Uses the latest WhisperX and Pytorch CPU packages for surprisingly good speed and translation accuracey

#### What Do I Need?

While the script is here, and you could "just run it," I think it is better to set up a virtual environment to run it in.  

Why?  Because It has a ton of dependancies, and you need to bring up a series of pytorch on CPU programs for it to run.

Once you have cloned the directory, I suggest that you do the following:

```Powershell
# 1. 
# Install pyvenv to manage the virtual environment.
# Most AI will help you do this

# 2. Restart PowerShell session
# Close and reopen PowerShell after pyvenv

# 3. cd to the clone github

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

Now install all dependancies as per the Installed_Packages.txt file in the virtual environment.  

Run the program

#### Why does the Main Script Look Weird and why do you have a SPEC file

While the current script works, it is in the process of being debugged so that I can compile it, insert FFMPEG into the .exe, and allow anybody to run it from a command line.  However, compiling from python script to .exe is a big task, and this is in a half built state

The good news it will run just fine as a Python script

The better news would be for somebody clone this and compile it, and let me know you got it as an EXE so the newbie can run it as an EXE.

Regardless, since I can't find another good / quick WhisperX git, I am leaving this here for somebody to use it or improve it
