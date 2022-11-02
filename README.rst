Casioplot for computer
======================

    Module ``casioplot`` from Casio calculator for Computer.

This can help to develop python programs in your computer and run it before put it in your calculator.

.. image:: https://raw.githubusercontent.com/uniwix/casioplot/master/images/rectangle.png
    :alt: A red rectangle

Installation
------------

.. code-block:: sh

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

.. code-block:: python

    from casioplot import *

    red = (255, 0, 0)
    set_pixel(10, 10, red)
    show_screen()  # Don't forget to show the screen to see the result.

.. image:: https://raw.githubusercontent.com/uniwix/casioplot/master/images/pixel.png
    :alt: A single pixel on the screen

For more examples and usage, please refer to the `Docs <https://casioplot.readthedocs.io/en/latest/>`_.

Development setup
-----------------

Nothing needed.

Release History
---------------

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

Uniwix - odevlo.me@gmail.com

Distributed under the MIT license. See `LICENSE <https://github.com/uniwix/casioplot/blob/master/LICENSE>`_ for more information.

`<https://github.com/uniwix>`_

Contributing
------------

1. Fork it (`<https://github.com/uniwix/casioplot/fork>`_)
2. Create your feature branch (``git checkout -b feature/fooBar``)
3. Commit your changes (``git commit -am 'Add some fooBar'``)
4. Push to the branch (``git push origin feature/fooBar``)
5. Create a new Pull Request

Compatibility Notes
-------------------

Some behaviors aren't respected:

- The output isn't show in the screen but saved on a picture.
- The function ``draw_string`` can't print all the characters and doesn't support the sizes ``small`` and ``large``.
- Only one calculator implemented: **casio graph 90+e**.


v 1.3.0 - Uniwix
