
PDF Whitespace-Inserter
=======================

Overview
--------

### This has an extremely specific use case, which it fulfills perfectly, but I would be shocked if it was useful to anybody else.

#### Converts the input PDF into an image, provides a minimal GUI (yes I know it's Qt which is not minimal, but I put zero effort into the GUI so it's a minimal effort GUI in reality) where the user can click and drag to insert whitespace. You can press s to save to the output file, which is converted back into a pdf.

Usage
-----

*   Functions somewhat like a CLI, but uglier.
*   From the root directory of this folder (or anywhere if you add this folder to your PATH) you call:
    
        python makeroom.py "inputfile.pdf" "outputname" "desired DPI"
    
*   Example:
    
        python makeroom.py in.pdf out 800
    

Details
-------

*   This program involves multiple conversion steps, and is therefore lossy, but it is perfectly suitable for adding space to math homework PDF's.
*   This thing is slow, as it's using python, opencv, and is shifting large amounts of image data at every moment that the user is dragging their mouse.
*   Might rewrite this in C++, not sure if it's worth the hassle of using real Qt, would likely opt for OpenGL/ImGUI because reasons.
