#GF Syntax Coloring

Authors:

* Jordi Saludes


##Xcode

XCode plugins and Syntax Coloring is not documented, unfortunately 
syntax coloring must be manually selected from the Editor :/


Based on the work on Lua by:

* Tiago Bastos
* Alex Karahalios (Install Script)
* Bret Victor (Syntax file)
* Graham Henstridge (Syntax file)



##Pygments

1. Download a copy of __Pygments__ and install it.

2. Assuming `Pygments` is where your copy resides, copy `Gf.py` into `Pygments/pygments/lexers`.

3. From `Pygments` call `make mapfiles`.

##Sublime Text
Copy folder `Gf` into `Packages` in the __Sublime Text 2__ installation folder.

###Commands
__open_related__: When viewing a GF source file,
`view.run_command('open_related')` opens all related files (abstract and
concretes).

