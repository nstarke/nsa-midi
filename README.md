# NSA-MIDI
This repository contains a NodeJS Command Line Application that maps MIDI Notes to URLs to fetch when the associated MIDI note is received from a MIDI device.

Additionally, there are two other scripts.  There is a `download-media.py` script that downloads random media from Wikipedia (image, audio, video).  The idea is to download static content to a webserver and then serve that static content over HTTP.  Then the NodeJS script can retrieve those files from the webserver over HTTP, and when the media is sent over the wire, the Eurorack module will convert the media to audio. Since the files are transferred in cleartext, the structure of the files are preserved and can create order in the output sound.

The NodeJS Script expects a file path to a JSON file.  That JSON file needs to be an array of URLs for the NodeJS script to retrieve when the corresponding MIDI notes are received.  To aid in creating these JSON files, I have added a `get-urls.sh` script to the repository.  This script will create a JSON array of absolute URLs from a webserver index that can then be redirected to a file.  Then you supply the file path to this new file to the NodeJS script.



## Why?
I built this application to work with [https://lectronz.com/products/thensaselector](https://lectronz.com/products/thensaselector), which is a Eurorack module that converts network traffic to audio.  

## Configuration
On Linux Systems, you will need `alsa-utils` and `jq` installed:

```
sudo apt install alsa-utils jq
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
