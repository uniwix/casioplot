Settings
========

The :py:class:`casioplot_settings` allows you to manage settings like the
size of the screen, the output mode, and provide shortcuts methods.

How to set a setting
--------------------

.. code-block:: python

    from casioplot import *

    casioplot_settings.set(<setting_name>=<setting_value>)

How to get a setting
--------------------

.. code-block:: python

    from casioplot import *

    value = casioplot_settings.get('<setting_name>')

Available settings
------------------

For each setting, the default value is shown

Height and Width
~~~~~~~~~~~~~~~~

.. code-block:: python

    from casioplot import *

    casioplot_settings.set(height=192)
    casioplot_settings.set(width=384)

Output filename
~~~~~~~~~~~~~~~

.. code-block:: python

    from casioplot import *

    casioplot_settings.set(filename="casioplot.png")

Output image format
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from casioplot import *

    casioplot_settings.set(image_format="png")

Shortcuts methods
-----------------

:py:meth:`default` method
~~~~~~~~~~~~~~~~~~~~~~~~~

Restore the default configuration.

.. code-block:: python

    from casioplot import *

    casioplot_settings.default()

Default settings for the calculator **CASIO Graph 90+e**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will set the width and height of the calculator screen
and will add the head of the screen (where power states
are displayed on the calculator).

.. code-block:: python

    from casioplot import *

    casioplot_settings.casio_graph_90_plus_e()

The blank screen will look like:

.. image::
    https://github.com/uniwix/casioplot/blob/master/src/casioplot/images/CASIO_Graph_90+e_empty.png?raw=true
    :alt: Casio Graph 90+e empty
