# Settings
## How to set a setting

```python
from casioplot import *

casioplot_settings.set(<setting_name> = <setting_value>)
```

## Available settings

For each setting, the default value is shown

### Height and Width

```python
from casioplot import *

casioplot_settings.set(height = 192)
casioplot_settings.set(width = 384)
```

### Output filename

```python
from casioplot import *

casioplot_settings.set(filename = "casioplot.png")
```

### Output image format

```python
from casioplot import *

casioplot_settings.set(image_format = "png")
```

## Shortcuts methods

### `default()` method

Restore the default configuration.

```python
from casioplot import *

casioplot_settings.default()
```

### Default settings for the calculator *CASIO Graph 90+e*

This will set the width and height of the calculator screen
and will add the head of the screen (where power states
are displayed on the calculator).

```python
from casioplot import *

casioplot_settings.casio_graph_90_plus_e()
```

The blank screen will look like:

![Casio Graph 90+e empty](CASIO_Graph_90+e_empty.png)
