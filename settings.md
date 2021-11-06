# Settings
## How to set a setting

```python
from casioplot import *

casioplot_settings.<setting name>=<setting value>
clear_screen()  # Don't forget to refresh the screen to update the setting
```

## Available settings

For each setting, the default value is shown

### Height and Width

```python
casioplot_settings.height = 192
casioplot_settings.width = 384
```

### Output filename

```python
casioplot_settings.filename = "casioplot.png"
```

### Output image format

```python
casioplot_settings.image_format = "png"
```

## Shortcuts methods

### `default()` method

Restore the default configuration.

```python
casioplot_settings.default()
```

### Default settings for the calculator *CASIO Graph 90+e*

This will set the width and height of the calculator screen
and will add the head of the screen (where power states
are displayed on the calculator).

```python
casioplot_settings.casio_graph_90_plus_e()
```

### Automatically refresh method

```python
casioplot_settings.set(<setting name>, <setting value>)
```
