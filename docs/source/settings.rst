Settings
========

Settings are used to configure the output image to match your calculator
screen or to change the output image format, for example. There are
a lot of settings available. This allows you to customize the output
image to your needs.

How to set a setting
--------------------

To set a setting, or use a preset, you must place the setting in a toml file. The file
must be named ``config.toml`` and must be placed in the directory
where the script is executed. You can also set global settings to all your projects by
placing a toml file in the ``~/.config/casioplot/`` directory.

Available settings
------------------

.. literalinclude :: <../../casioplot/presets/default.toml>
:language: toml


Presets
-------

You can use a preset by specifying the path of the preset in the
``config_to`` key in the toml file. If you want to use a global preset,
you need to prefix the path with ``global/``. If you want to use a preset
that we made, you need to prefix the path with ``preset/``.

Here is a example of how to use a preset:

..code-block:: toml

    config_to = "preset/fx-CG50.toml"

    # enable saving the screen
    [saving_screen]
    save_screen = true

This will use the preset for the **CASIO fx-CG50** calculator,
which mean all the settings will be inherited from this file.
However, the ``save_screen`` setting will be set to ``true``
in order to save an image of the screen.

By default, no preset is loaded. You can load a preset by setting
the ``config_to`` key in the toml file, without any other settings
to use any preset.


Default preset
~~~~~~~~~~~~~~

We strongly recommend to include the default preset in your toml file,
at least if you are not using any other preset. This will ensure that
all the settings are set to the default values, and that you get no errors
when running the script.

.. code-block:: toml

    config_to = "preset/default.toml"

Default settings for the calculator **fx-CG50**, **fx-CG50 AU** and **Graph 90+e**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will set the width and height of the calculator screen
and will add the head of the screen (where power states
are displayed on the calculator).

fx-CG50
^^^^^^^

.. code-block:: toml

    config_to = "preset/fx-CG50.toml"

fx-CG50 AU
^^^^^^^^^^

.. code-block:: toml

    config_to = "preset/fx-CG50_AU.toml"

Graph 90+e
^^^^^^^^^^

.. code-block:: toml

    config_to = "preset/graph_90+e.toml"


The blank screen will look like, for all of theses presets:

.. image::
    https://github.com/uniwix/casioplot/blob/master/casioplot/images/calculator.png?raw=true
    :alt: Empty calculator screen
