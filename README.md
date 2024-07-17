# axidraw

This module interfaces with an Evil Mad Scientist Eggbot Axidraw plotter. It implements the machine as a modular Viam Gantry.



## Connecting

This module communicates to the gantry using a USB serial connection. The axidraw python API is imported to communicate with the device. 
Connect the eggbot stepper driver through a USB cable to any computer or board (such as the raspberry pi) running a viam server and configure the module to control it. You can control through the following:
- the "Test" section in the Configure tab, 
- the Control tab,
- a python script using the [Gantry Python SDK](https://docs.viam.com/components/gantry/)


## Configuration

To configure the axidraw, add the viam module through the viam modular registry. 
You can follow the instructions to add a module to your robot at https://docs.viam.com/extend/modular-resources/configure/

This module contains one modular resource corresponding to the `peter:eggbot:axidraw` module and can be configured like so. There are no attributes required to further configure the module. Note that the version field in the module and the name fields in both the module and component
can be selected to your liking.


### `peter:eggbot:axidraw`
```json
{
  "modules": [
    {
      "type": "registry",
      "name": "***",
      "module_id": "peter:axidraw",
      "version": "*.*.*"
    },
  ],
  "components": [
    {
      "name": "***",
      "namespace": "rdk",
      "type": "gantry",
      "model": "peter:eggbot:axidraw",
      "attributes": {} // can be empty
    }
  ]
}
```


