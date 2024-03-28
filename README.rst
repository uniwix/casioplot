Casioplot for computer
======================

    Module ``casioplot`` from Casio calculator for Computer.

This can help to develop python programs in your computer and run it before put it in your calculator.

.. image:: https://raw.githubusercontent.com/uniwix/casioplot/master/docs/source/images/rectangle.png
    :alt: A red rectangle

Installation
------------

.. code-block:: shell

    pip install casioplot

This module use python 3.10.0.

Need the module ``Pillow`` to work.

**Install Pillow:**

.. code-block:: shell

    pip install pillow

Usage example
-------------

Draw a single pixel
~~~~~~~~~~~~~~~~~~~

.. code-block:: python3

    from casioplot import *

    red = (255, 0, 0)
    set_pixel(10, 10, red)
    show_screen()  # Don't forget to show the screen to see the result.

.. image:: https://raw.githubusercontent.com/uniwix/casioplot/master/docs/source/images/pixel.png
    :alt: A single pixel on the screen

For more examples and usage, please refer to the `Docs <https://casioplot.readthedocs.io/en/latest/>`_.

Notes on performance
--------------------

The performance you get in the computer is not representative of the performance on the calculatores.
Keep in mind the following differences:
    * Obviosly ever operation that isn't from the casioplot package is going to be faster in the Computer
    * clear_screen, set_pixel, get_pixel and draw_string are faster in the computer
    * show_screen is slower in the computer

For example, the following codes draw a black square of 100 by 100 pixels.

.. code-block:: python3

    for x in range(100):
        for y in raange(100):
            set_pixel(x, y)
    show_screen()

Is faster on the computer, but

.. code-block:: python3

    for x in range(100):
        for y in raange(100):
            set_pixel(x, y)
            show_screen()

Is slower.

Development setup
-----------------

Nothing needed.

Release history
---------------

* 2.2.0
    * Update the settings system to use toml
    * Clean the code
* 2.1.1
    * Fix imports
    * Add new presets
    * Change example ``image_3d_test.py``
* 2.1.0
    * Add all the characters in the function ``draw_string``
* 2.0.0
    * Add tkinter support
    * Change the way to show the screen
    * Change settings implementation
    * Thanks to `@miguelTorrinhaPereira <https://github.com/miguelTorrinhaPereira>`_ for the help
* 1.3.2
    * Minor fix
* 1.3.1
    * Minor fix
* 1.3.0
    * Update settings and usage
    * Adding documentation
* 1.2.0
    * ADD: Character support
* 1.0.9
    * FIX: images in the docs
* 1.0.5
    * FIX: import in the ``__init__`` file
* 1.0.1
    * First release on PyPI (this release is no more available now)
* 1.0.0
    * Work in progress

Meta
----

Uniwix - `uniwixu@gmail.com <uniwixu@gmail.com>`_

Distributed under the MIT license. See `LICENSE <https://github.com/uniwix/casioplot/blob/master/LICENSE>`_ for more information.

`<https://github.com/uniwix>`_

Contributing
------------

1. Fork it (`<https://github.com/uniwix/casioplot/fork>`_)
2. Create your feature branch (``git checkout -b feature/fooBar``)
3. Commit your changes (``git commit -am 'Add some fooBar'``)
4. Push to the branch (``git push origin feature/fooBar``)
5. Create a new Pull Request


v 2.2.0 - Uniwix
