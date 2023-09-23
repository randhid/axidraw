# axidraw

This module interfaces with an Evil Mad Scientist Eggbot Axidraw plotter. It implements the machine as a mosular Viam Gantry.



## Connecting

This module communicated to the ganry using a USB serial connection, the axidraw python api is imported to communicate with the device. 
Connect the eggbot stepper driver to a 

## Configuration

To configure the axidraw, add the viam module through the viam modular registry. 
You can follow the instructions to add a module to your robot at https://docs.viam.com/extend/modular-resources/configure/

This module contains one modular resource the `peter:eggbot:gantry`. And can be configured like so. Note that the name fields in both the module and component
can be selected to your liking.


### `viam:eggbot:axidarw`
```json
{
  "modules": [
    {
      "name": "van_gogh",
      "executable_path": "path/to/run.sh"
    }
  ],
  "components": [
    {
      "model": "peter:eggbot:gantry",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
      "type": "gantry",
      "name": "rothko"
    }
  ]
}
```


