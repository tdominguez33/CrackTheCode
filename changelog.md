# Crack the Code Changelog

## V0.5.0 - 14/04/2023
- ##### You can now choose length of the code you want to crack! Choose between Easy (3 digits), Normal (4 Digits) or Hard (5 Digits).
- ##### Added a few comments to the code to improve it's legibility.

## V0.4.2 - 13/04/2023
- ##### Reverted the fullscreen default, how mobile looks depends on pygbag so makes no sense to limit PC.

## V0.4.1 - 13/04/2023
- ##### The game is now fullscreen by default so it can adapt better on mobile (I hope) and the key to exit on PC is ESC.
- ##### Fixed a bug where the backspace image didn't move properly when resizing the window.

## V0.4.0 - 13/04/2023
- ##### The window is now resizable, all elements should adjust according to the size of the window (especially useful for mobile).
- ##### Improvements to the code to be able to add more features on the future.

## V0.3.0 - 10/04/2023
- ##### New mechanic! You can now select which square to write the next number into, just click the number and the selected square will change color to indicate its been selected (this also works to delete and replace numbers).
- ##### Now if a number is introduced its key on the on-screen keyboard changes color.
- ##### More minor improvements to the code.

## V0.2.2 - 09/04/2023
- ##### Made the on-screen keyboard keys bigger for it to be better suited for mobile use.
- ##### Aesthetic changes.
- ##### Made more coordinates relative to a determined constant instead of being hardcoded.

## V0.2.1 - 07/04/2023
- ##### Implemented restart without the need of a keyboard (Anxious me deployed the last update without implementing that).
- ##### Fixed a bug that deleted a number if you pressed on the space in between the number buttons.

## V0.2.0 - 07/04/2023
- ##### Added an on-screen keyboard (this doesn't replace the keyboard input, they coexist).
- ##### Noticed the game only gave you 9 tries instead of 10, so fixed that.
- ##### Minor extra improvements.

### To-Do
 - ##### Correct various thing having to do with the coordinates of some elements and pieces of code that are repeated for the physical keyboard and on-screen keyboard.

## V0.1.2 - 06/04/2023
- ##### Minimum restyle, new colors, font and icon.
- ##### Fixed a small visual bug where numbers appeared in the win or lose screen if a key was pressed.

## V0.1.1 - 03/04/2023
- ##### Added restart option (R key).
- ##### Started using numpy for the random number generation because of a problem with the standard random library and pygbag.

## V0.1.0 - 02/04/2023
- ##### Initial Release, the game works fine but needs more work. (restart option, redesign, etc).