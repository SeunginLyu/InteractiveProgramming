# Software Design MP5: InteractiveProgramming(Revision)

### <u>Game : Pixel Dancer (Revision by Seungin)</u>


##### *  [Project Proposal](https://docs.google.com/document/d/1RazNDZ761jDrDj-v3TPxPdJwY7d9778ixBn97HTK4Ps/edit?usp=sharing) (Thu, Feb 23rd, 2017)
##### *  [Initial Submission](https://github.com/yjiang0929/InteractiveProgramming)

#### Things that got Fixed:

1) I <i>modularized</i> the single "pixel_dancer.py" so that the code is better organized and more intuitively modifiable. Each model, view, controllers are
strictly divided into different modules and are independent of each other. <br>
2) The initial version before this revision did not really make any usage of the Model-View-Controller style. Everything was done in the __init__ class of viewers and controllers (they technically didn't even need to be classes, they were acting more like simple independent functions). Now the code is actually implemented in the <i>MVC style with appropriate OOP Features.</i><br>
3) "Rhythm" is now actually implemented as a class.<br>
4) I used python's unique features such as <i>list comprehension</i> and </i>property decoraters</i> to clean up the code. And I changed some of the misleading variable names to reduce confusion.
