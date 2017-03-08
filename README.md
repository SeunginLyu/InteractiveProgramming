# Software Design MP4: InteractiveProgramming

# <u>Game : Pixel Dancer</u>
### by Seungin Lyu and Yichen Jiang


##### *  [Project Proposal](https://docs.google.com/document/d/1RazNDZ761jDrDj-v3TPxPdJwY7d9778ixBn97HTK4Ps/edit?usp=sharing) (Thu, Feb 23rd, 2017)
##### * How To Run:
###### 1) Install Python3 <br>
###### 2) Install Pygame, Numpy module using pip3 <br>
###### 3) Then Run "python3 pixel_dancer.py" to Play!
##### * Basic Game Instruction
Move your doggy around with the arrow keys to paint as many
pictures as possible. Remember, you should follow the music rhythm! If you
aren't following the beat, you will lose your precious energy and end up
only coloring half the grid you are on.  Also, you don't want to go out of the
picture and be careful not to eat the toxic chocolates! You will gain some
extra energy everytime you complete one picture. Good Luck!
(by the way..the energy decreases naturally because doggy is hungry..)
You can play with the game settings by manipulating the defined constants.
##### * For Detailed Documentation, refer to "pixel_dancer.html"


## 1. Project Overview:
In this project, we made an interactive game: PIXEL DANCER! The player needs to control a cute dog to clear the obstacles and reveal the secrets underneath. During the game, the player will need to follow the music beat and avoid the toxic chocolate bars to avoid losing energy. The game is based on Python 3 and is built on the Pygame module.

## 2. Results:
The player can move the dog using the arrow keys on the keyboard. The grid that the dog moves into will then be cleared or half-cleared depending on whether the player has followed the rhythm or not. Whenever the player moves out of the game canvas, the dog will be relocated on the top left corner. After the player clears one image, a new image will generate underneath the old one and the old picture will become the grids of this level.

During the game, an energy bar will be displayed on the right to inform the player of the remaining time. Any illegal move(move out of canvas, not follow the music beat, run into a "delicious" chocolate) will decrease the energy by 10%. When the player finishes a level, the energy bar will be replenish 20%. When the energy runs out, a "Game Over" screen will appear and display the number of pictures the player cleared. And the player can press enter to start a new round of adventure!
<br>

[![Pixel Dancer](https://i.ytimg.com/vi/Vvjet8vUsKg/maxresdefault.jpg)](https://youtu.be/Vvjet8vUsKg)

### If you would like to see a video demo of the game, please [click here](https://youtu.be/Vvjet8vUsKg)

## 3. Implementation:
The Pixel Dancer game is composed of some basic classes. The Player class displays the dog, handles keyboard controls and updates energy information. The Monster class generate chocolates at random locations and displays warning signs in the grids that the chocolates will appear. The monsters will not generate on top of each other and are updated every two beats. The RhythmViewer class displays the music beat for the player to follow. The BPM(beat per minute) of the music is predefined instead of using real-time Fast Fourier Transform. We made this simplification because the alternative is beyond our current knowledge and the predefined beat constant can serve our purpose well enough.

The GridList class handles all the grids that the player will clear. When the player steps on a grid, the grid's alpha value will change accordingly. After the player clears a canvas, the GridList class takes the old background and chops it into the new grids on the canvas. The default pygame chop function can only chop the interior of a function. In order to get the correct individual grids, we developed an algorithm to chop the image iteratively and it works for different number of rows as well. While making the game, we kept in mind to keep the game robust for different canvas size and monster number. And we can make the game more difficult or easy by changing the corresponding global constants.

To tell the program when to stop the game, we set up two flags that decides whether to run the game of display the game over screen. We also allowed the player to restart the game by pressing ENTER instead of rerunning the code in Terminal. We wanted to try our best to make the game as realistic as possible.

However, our code can be much better implemented by fixing a few things.<br>
1) __init__ method of all viewer classes should only specify the self.model
attribute and they should extend it from a basic Viewer class.
Also, draw() methods for each classes should be defined.
Right now the classes aren't technically classes (but are more like functions)<br>
2) OOP (Object Oriented Programming) Features for relationships such as:<br>
   - Gridlist has Grids.
   - All the different Viewer classes extend default(parent) Viewer class.


## 4. Reflection:
We collaborated really well as a team. We each wrote separate parts of the code and then put them together with the help of Github. Merge conflicts are sometimes frustrating, but each of us having a concrete picture of the project idea made it easier to resolve such merge conflicts.

One lesson that we learned is that once a code is written without a clear map of OOP relationships and detailed class structure, the code gets really messy implementation-wise and it is actually very time-consuming to rewrite all the code in the right convention. During the project, we realized that we were implementing the viewer classes in a wrong way but the problem is that we were DONE implementing most of them (this happened because we were learning OOP as we were working on this project). So for the revision, we plan to work with a more detailed picture of classes and refactor the code according to the strictly defined OOP features.

At first we thought the project was a bit over-scoped because there were too many components we want to put together. But as we managed to complete the minimum viable product before the mid check-in, we started to go beyond what we expected in the project proposal. We are very satisfied with how the project eventually turned out and are willing to improve the game even more in Project 5(revision). Through out the project, we really got our hands on objected-oriented programing and the Pygame skills we learned can be useful in future visual developments as well.
