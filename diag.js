// save as midi-test.js and run: node midi-test.js
const JZZ = require('jzz');

let engines = [];
try { require('jazz-midi'); engines.push('jazz-midi'); } catch (e) { console.warn('jazz-midi not loaded:', e.message); }
try { require('jzz-rtmidi').register(JZZ); engines.push('jzz-rtmidi'); } catch (e) { console.warn('jzz-rtmidi not loaded:', e.message); }

JZZ().and(function () {
  const info = this.info();
  console.log('Candidate engines:', engines);
  console.log('Active engine:', info.engine);           // what JZZ actually uses
  console.log('Inputs:', info.inputs);                  // list of names
  console.log('Outputs:', info.outputs);

  // Try exact name from your `aconnect -l`:
  const WANT = 'USB MIDI Interface MIDI 1';             // client 20:0
  console.log('Trying to open by name:', WANT);
  JZZ().openMidiIn(WANT)
    .or(e => console.error('Open by name failed:', e))
    .and(function () {
      console.log('Opened by name:', this.name());
      this.connect(msg => console.log('MIDI:', msg.toString()));
    });

  // Also try first input by index for sanity:
  JZZ().openMidiIn(0)
    .or(e => console.error('Open by index(0) failed:', e))
    .and(function () {
      console.log('Opened by index(0):', this.name());
      this.connect(msg => console.log('MIDI:', msg.toString()));
    });
});

