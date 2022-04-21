# Elden Ring death counter

Captures screen and detects "You died" upon death in the video game Elden Ring (2022)

## Install

Requires Windows and Python 3.7+

### If you know what Python and pip is:

Install with pip: `pip install youdied`

### If you don't know what Python is:

Make sure you have Python installed on you machine.

Go to your terminal and confirm that python is installed 
by typing `python -V` and press Enter. 
It should say something like `Python 3.10.4` or something similar. 
It must be version 3.7.0 or higher.

If you don't, there are many ways to install Python.
E.g. using __one of these__ approaches:

 - install windows app https://www.microsoft.com/en-us/p/python-310/9pjpw5ldxlz5?activetab=pivot:overviewtab (very easy)
 - download and install from https://www.python.org/downloads/ (default)
 - install miniconda from 
   https://docs.conda.io/en/latest/miniconda.html (potentially more advanced)

After you have installed Python, open you terminal (or anaconda prompt when using miniconda). 
Now, you should verify that you have Python installed, 
which also lets you use the `pip`-command to install new packages.
Go back to the step above and install using the `pip`-command.

__NOTE__: Python is capable of running any arbitrary code on your machine. 
If you have no idea what strangers' code does, then you should not run it on your 
machine. 
Be skeptical, and critical.
You could ask someone you trust to look over this code first if you're unable to verify yourself.
The code is freely available in the repository for scrutiny, inspiration and education.
  
## How to use `youdied`
After installed, you can run the `youdied` command from terminal 
(in the same Python environment that you installed this package in). 

__*How to stop the program from running?*__ Press Ctrl + Z in the terminal

### Start counting deaths

When program is running, it will notify you in the terminal on death detection.
There is a 5 second cooldown, to ensure that a death is only counted once.

### Examples

New character: `youdied <name of character`

Continue from last character: `youdied`

Print name of last character: `youdied -p` or `youdied --previous`

Death count file: *&lt;your user folder&gt; / .youdied / deathCounts / &lt;character name&gt;.txt*

Show stats: `youdied -l` or `youdied --list` will output something like

```
        Started last            Character          Death count
 2022-04-20 12:00:00       Always Feet 69                    4
 2022-04-17 12:00:00        Cavelady Dida                    4
 2022-04-12 12:00:00           Elden Lard                    8
 2022-04-09 12:00:00      Maidenless Hero                    4
```

### With words

In its simples form run `youdied <character name>`, 
for example `youdied Maidenless Hero` if your want to store death counts 
under the name "Maidenless Hero". 
The next time, you only have to run the `youdied` command without 
any arguments if you want to use the same character name.

If you want to register deaths in another name, stop the script (Ctrl + Z) and give a new name.

E.g. `youdied Cavelady Dida`

### Multiple characters?
Some players have more than one character, 
so therefore death counts are associated with a character name. 
The name is just a convenience to allow organizing the death counts.

(This name of course has nothing to do with what you call your character in the game.
If you wish, you may call them "character 1", "character 2", "tarnished Bob" or whatever you want.)

### Files and output
When running for the first time a folder `<your user folder> / .youdied` will be created.
This folder will keep track of death statistics and inspirational message use statistics
(to increase variety of messages shown)

Additionally, there is a folder called `<your user folder> / .youdied / deathCount` 
that holds a file for each registered character. 
E.g. with the four characters used above, there would be a file called "Always Feet 69.txt" 
with content only being the number "4".

If you want to know the death statistics of all characters you have tracked, 
run `youdied -l` as mentioned above.

### Help
Run `youdied -h` to get the help screen:

```
youdied -h
usage: youdied [-h] [-v] [-l] [-p] [character_name ...]

A motivational Elden Ring death counter. Uses screen capture to detect deaths. 
Will output motivational quotes and proverbs on detection.

positional arguments:
  character_name  Name of character to register stats on. If omitted the last used character is used, 
                  if any (default: None)

options:
  -h, --help      show this help message and exit
  -v, --version   Print version and exit. (default: False)
  -l, --list      List all characters and exit. (default: False)
  -p, --previous  Print out previous character, i.e. the last one used, and exit. (default: False)

Good luck, Tarnished!
```

### How to stop the program

Press Ctrl + Z in the terminal

## Credits

### D3DShot
Screen capturing is possible using Windows Duplication API, 
and we use the fabulous [D3DShot][d3dshot] python package to do so.
Unfortunately, there is an [issue with version of a dependecy package][d3dshot_issue]
`pillow`, which is breaks the installation. 
Any further development from the developers of D3DShot seems to be stalling.
We have therefore fixed the dependency and embedded their code inside this project because
[PYPI doesn't allow direct URI dependencies][pypi_uri_deps].

[d3dshot]: https://github.com/SerpentAI/D3DShot
[d3dshot_issue]: https://github.com/SerpentAI/D3DShot/issues/44
[pypi_uri_deps]: https://github.com/pypa/pip/issues/6301


### The world of amazing nerds
So many open source tools and programs. 
Look at all the free (as in beer) code others have shared! 

Imagine where we would be if they were not there.

Thanks!