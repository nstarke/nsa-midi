# NSA-MIDI
This repository contains a NodeJS Command Line Application that maps MIDI Notes to URLs to fetch when the associated MIDI note is received from a MIDI device.

## Why?
I built this application to work with [https://lectronz.com/products/thensaselector](https://lectronz.com/products/thensaselector), which is a Eurorack module that converts network traffic to audio.  

## Configuration
On Linux Systems, you will need `alsa-utils` installed:

```
sudo apt install alsa-utils
```

## Arguments
* `--device` - The MIDI Device to use.  You can see a list of MIDI inputs by running the application in `DEBUG` mode, or by running `aconnect -l` at the Linux Command Line.
* `--jsonMap` - A JSON Array of URLs to fetch.

## Debug Mode
To enable DEBUG mode, which provides verbose output logging, set a process environment variable for `DEBUG`.

For example:
```
DEBUG=1 node index.js --device 'USB MIDI Device' --jsonMap current-track.json
```

## Notes
The port on the target host will need to be open for the traffic to actually go over the wire and thus create sound on the NSA Selector.
