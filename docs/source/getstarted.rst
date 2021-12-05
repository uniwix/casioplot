Getting Started
===============

Installation
------------

.. code-block:: shell

    pip install casioplot


Requirements
------------

This module use python 3.10.0.

Need the module :py:mod:`Pillow` to work.

Install :py:mod:`Pillow`:
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    pip install pillow


Settings
--------

See :doc:`settings options <settings>` for more information.


Compatibility Notes
-------------------

Some behaviors aren't respected:

- The output isn't show in the screen but saved on a picture.
- The function :py:func:`casioplot.draw_string` can't print all the characters
  and doesn't support the sizes ``small`` and ``large``.
- Only one calculator implemented: **casio graph 90+e**.
