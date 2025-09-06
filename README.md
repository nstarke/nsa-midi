<video src="./nsa-midi.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

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

The NodeJS application depends on the [jazz](https://jazz-soft.net/) MIDI library, which does NOT work with NodeJS on ARM hosts.  I found this out when trying to set up the NodeJS application on a Raspberry Pi.  I think the Jazz NodeJS integration only supports x86_64.

It *might* work in a client-side, browser-based context on a Raspberry Pi, but I did not try that.

## Network Setup
For my set up, I have a small Intel x86_64 host connected via ethernet to the first port of the NSA Selector Eurorack Module, and then another ethernet connection from the second NSA Selector ethernet port to a switch.  Also plugged into that switch is a Raspberry Pi running an HTTP webserver.  Everything connected to that switch is on the same VLAN.

Both the Raspberry Pi and the Intel x86_64 host also have WLAN connections to the same Wireless network.  This is for SSHing into each of these hosts without sending traffic over the ethernet connection and thereby creating unintended audio artifacts as the Eurorack module converts the SSH traffic into sound.

## NodeJS Script Arguments
* `--device` - The MIDI Device to use.  You can see a list of MIDI inputs by running the application in `DEBUG` mode, or by running `aconnect -l` at the Linux Command Line.
* `--jsonMap` - A JSON Array of URLs to fetch.

## NodeJS Script Debug Mode
To enable DEBUG mode, which provides verbose output logging, set a process environment variable for `DEBUG`.

For example:
```bash
DEBUG=1 node index.js --device 'USB MIDI Device' --jsonMap current-track.json
```

## Python3 "download-media.py" Arguments
```bash
$ python3 download-media.py -h
usage: download-media.py [-h] query count {audio,video,image} output_dir

Process query parameters.

positional arguments:
  query                Search query string
  count                Number of items to return (must be an integer)
  {audio,video,image}  Type of item (must be one of: audio, video, image)
  output_dir           Directory to save the output files

options:
  -h, --help           show this help message and exit
```

* `query` is the string to search for media for on wikipedia
* `count` is the number of media files to download
* `type` is either `audio`, `video`, or `image` for what type of files to download from wikipedia.
* `output_dir` is the data directory to write the downloaded files to.

### Python3 Script Example
```bash
$ python3 download-media.py "ghosts" 10 video /var/www/html/ghosts
```

## Bash "get-urls.sh" script
```bash
$ bash get-urls.sh "http://webserver.example.local/url-path-with-autoindex/"
```
The script only takes one argument, and that is a `/` terminated absolute URL to an autoindex webserver address.
