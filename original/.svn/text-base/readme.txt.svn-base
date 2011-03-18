Here's the source code and assets for a simple game demo Miika and I did for the Introduction to Game Development course.

This is the original version we did in about four days time.

Run tsaap.bat or tsaap.sh to execute the game or unittests.bat or unittests.sh to run the tests.


The keys are:

Player one:
Up arrow: Move forward
Left arrow: Rotate left
Right arrow: Rotate right
Right ctrl: shoot

Player two:
w: Move forward
a: Rotate left
d: Rotate right
Left ctrl: shoot

Escape: quit
p: pause game
F1: Player one view
F2: Player two view
F3: Normal camera
F4: Static camera


P.S. To enable anti-aliasing in Panda3D applications add these lines to your panda etc\Config.prc file in windows or to /etc/Config.prc in linux:

  framebuffer-multisample #t
  multisamples 2

P.P.S. If you're having performance issues, try commenting/removing these two lines from Game.py, to disable the use of shaders:

  render.setShaderAuto()
  render.setShaderInput('light', lightnode)


-Vesa Nieminen