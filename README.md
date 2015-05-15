# itunes-gmusic
`itunes-gmusic` is a python (2.7) interface between your iTunes music library
and your Google Play Music library.

I created this project to sync play counts between the two services,
as currently this only happens at first Google Music upload.
If I get this working, I might start adding in other features as well.

As a fair warning, this is my first python project of any significant size. Criticism is appreciated :p

### Current State of the Project
Like much of github, `itunes-gmusic` is "currently" under development 
in a non-workable state by an amateur programmer. Currently, the semi-module abomination can:  
* Load your iTunes and Google Music libraries
* Evaluate exact track matches

Running `main.py` will deliver just a naive count of these matches
right now. 

#### Hidden Dependencies
Until I create a proper `setup.py`, the project has one dependency:  
* `gmusicapi`, available on `pip`.

#### Goals

The primary purpose of this project right now is to be able to sync play counts. Further to this goal, I am working on the following functionality:  
* Close string matches (SeatGeek's `fuzzywuzzy` looks interesting!)
* Evaluate how to total up play counts (likely difficult if track has been played independently numerous times)
* Update iTunes play counts via Applescript (Mac Only!)
* Update iTunes play counts via XML manipulation (Risky!)
* Creating a proper module out of this mess.
