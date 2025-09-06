const fs = require("fs");
const JZZ = require('jzz');
const minimist = require('minimist');
const fetch = require('node-fetch');

const info = JZZ().info();

if (process.env['DEBUG']) {
  console.log('Inputs:');
  info.inputs.forEach((input, index) => {
    console.log(`${index}: ${input.name}`);
  });
}

const args = minimist(process.argv.slice(2));

if (!args.device || !args.jsonMap) {
  console.log('Usage: node index.js --jsonMap <path to JSON map file> --device <MIDI device name>');
  console.log('Example: node index.js --jsonMap current-track.json --device "USB MIDI Interface MIDI 1"');
  process.exit(1);
}

const jsonMap = JSON.parse(fs.readFileSync(args.jsonMap, 'utf8').toString());

const device = args.device;

if (!info.inputs.map((i) => { return i.name; }).includes(device)) {
  console.log(`Specified midi in device (${device}) not found, exiting`);
  process.exit(1);
}

if (process.env['DEBUG']) {
  console.log(`Chosen URLs: \n${jsonMap.join(', \n')}\n`);
}

const j = JZZ()
  .openMidiIn(device)
  .or('Cannot open MIDI In!')
  .and(() => {
    if (process.env['DEBUG']) {
      console.log('Listening for MIDI...');
    }
  });
  
j.connect((msg) => {
  // Listen to all incoming MIDI messages
  const [status, note, velocity] = msg;

  // Check if it's a Note On (0x90–0x9F) and velocity > 0
  if ((status & 0xf0) === 0x90 && velocity > 0) {
    const url = jsonMap[note % jsonMap.length]
    if (process.env['DEBUG']) {
      console.log(`Note On received: note=${note}, velocity=${velocity}, url=${url}`);
    }
    fetch(url);
  }
});
