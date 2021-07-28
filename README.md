# zmonkey

This tiny python script helps map your joysticks and gamepads to MIDI output.

It's a super MVP, so feel free to submit PRs for more features.

## Requirements

You need the following libraries to run this script:

* pyglet
* simplecoremidi

## Setting up your environment

You could do this in a bunch of ways, but I will explain how you can run Python3
in the default virtual environment to launch this script.

First, clone the repo from GitHub:

```
$ git clone https://github.com/unix-ninja/zmonkey.git
```

Next, enter the repo and setup the virtual environment

```
$ cd zmonkey
$ python3 -m venv .
```

Activate the virtual environment

```
$ source bin/activate
```

And finally, install the dependencies

```
$ pip install pyglet simplecoremidi
```

Now you can just launch the script and have fun!

```
$ python zmonkey.py
```

Feel free to run it with `-h` for help info.
