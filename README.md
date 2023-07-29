![Tagline](./assets/tagline.png)

![Author](./assets/author.png)

### Getting Started and Usage

To start using the utilities provided by SnapSimp, you'll first want to create a virtual environement:

`python -m venv snap-simp-venv` or `python3 -m venv snap-simp-venv`

Now you'll need to activate the virtual environment. If you're on Windows simply:

`.\snap-simp-venv\Scripts\activate`

If you're on Mac OSX, you'll need to source it:

`source ./snap-simp-venv/bin/activate`

Now you can simply install the requirements once inside of the virtual environement:

`pip install -r requirements.txt`

Any and all HTML files to be analyzed are expected to be placed in the `html` folder within the same directory as this README. If you place them somwhere else, you'll need to provide the relative paths to the files via command line arguments such as `--snap-history-file` which is by default named `snap_history.html` and `--account-file` which is by default named `account.html`. If you name these something else, then you'll also need to specify that.

### Who

That's kind of a dumb question but I'll assume you're asking who made this or who this is for. I, Nate Cheshire, made this as a means of procrastination late July, 2023. I made this for anyone who wants to use the tool, primarily me.

### What

Python 3.11, virtual environments, Beautiful Soup, boredom, and caffeine.

### Where

From my home, my bedroom to be exact (yes my software engineer steup and beep boop MacBook are in my room); earth dimension C137 even.

### When

I guess I already said this in the "Who" section, but I'll repeat for those who are dyslexic or illiterate since I happen to be in that community. I was bored on Friday, late July, 2023 and with no actual work work to do since our sprint just ended, I thought instead of working on one of my 17 unfinished side projects, I'd start a new one.

### Why

I wanted to do some data visualization stuff and see statistics about my snaps. In particular, I happen to video the person at the top of my best friends list A LOT so I thought it might be cool to generate some statistics which is why you can even generate a ratio for image to video snaps.

### How

By the power of snakes, Python 3.11, ya boi Guido van Rossum, decades of computer science advancements, GitHub free tier, and GPT4 and Copilot, useless projects such as this can exist and occupy possibly vital bandwidth and server space.

### Credits and thanks

Thanks to Nate Cheshire for making this. You're welcome, thanks for thinking of me when using my tool. No problem, Nate. I'd also like to dedicate the existence of this tool to you, you know who you are.
