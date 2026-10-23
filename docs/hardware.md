# The instrument: Essex EUP-111 with adsilent 2

The user's instrument determines how performance can be captured.
This document records what is known, what is assumed, and the experiments that settle the rest.

## Summary

The adsilent 2 is a **MIDI controller built into an acoustic piano**.
Optical sensors under the keys produce USB MIDI that a browser can read through the Web MIDI API.
That makes symbolic performance capture (exact pitches, onsets, releases, velocities, pedal) available **without audio transcription**.
For this project it is the most consequential hardware fact.

## The piano

Essex EUP-111(E): a 111 cm upright designed by Steinway and built for the Essex line.
It has a wooden action, a tapered solid-spruce soundboard, and 3 pedals with **no true sostenuto** [reported: dealer spec sheets, see references H2–H3].
The middle pedal on Essex uprights is typically a practice muffler or bass sustain; to be checked on the actual instrument.

## adsilent 2 (Excellent Piano Installs GmbH, Germany)

Source: *adsilent 2 User's Guide v1.00* (2023), read in full [confirmed, reference H1].

### Hardware

| Item | Detail |
|---|---|
| Key sensing | A rail of optical sensors under the keys measures key movement. Calibrated per key. "Viewing range" setting moves the trigger depth (5 levels). |
| Pedal sensing | Sensors on pedals; damper (right) pedal can be **proportional** or on/off (factory default: proportional). |
| Mute | A mechanical mute rail stops the hammers before the strings. |
| Computer port | **USB-C, device ("slave") only**, USB-MIDI. "Computer will install the required MIDI driver"; supported OS: macOS and Windows 11. Max cable length 3 m. |
| Bluetooth | BLE MIDI, **not supported on Windows**. |
| Audio | 2 headphone jacks, 3.5 mm LINE OUT, 3.5 mm LINE IN. |
| Internal recorder | 20 banks of about 15,000 events each, stored as MIDI. |

### MIDI implementation (from the chart on p. 26)

| Function | Transmitted | Notes |
|---|---|---|
| Channel | 1 (keyboard) | Channel 2 = internal recorder playback. Channels 3 and 4 = "pedal resonance data". |
| Note numbers | 21–108 | The full 88 keys. |
| Note-on velocity | yes | |
| **Note-off (release) velocity** | **yes** | Uncommon. Release speed carries articulation information (how a note ends, not just when). |
| CC64 damper | yes | Proportional mode means continuous values, probably 0–127 (to verify). |
| CC66 sostenuto | yes | Only meaningful if a pedal has a sensor mapped to it. |
| CC67 soft | yes | |
| Program change, SysEx | yes | |
| Aftertouch, pitch bend, clock | no | |

Factory default **"Continuous Note-On: On"** is not explained in the guide.
It might mean note-offs are sent as note-on with velocity 0, which would conflict with release velocity.
Experiment H1 settles this.

## What this means for the project

1. **Performance capture is symbolic from the start** [speculative until H1].
   Pitch accuracy is effectively perfect: a key either moved or it didn't.
   No polyphonic transcription model is needed for the user's own playing.
2. **Measurement validity still needs thought.** The sensors measure *key* motion, not the hammer or the string.
   - *Velocity* is the instrument's estimate of key speed mapped to 1–127 through a calibration and an "expression" curve (8 levels).
     It is a relative loudness proxy.
     It is comparable within one session and calibration state, not across recalibrations, and is not in dB.
   - *Onset time* is when the key crosses the sensor threshold, a few milliseconds from when the hammer would strike.
     The offset may depend on velocity.
     That doesn't matter for timing *relative* to the user's own other notes, which is what practice analysis needs.
   - *Release velocity* and *proportional damper* make articulation and pedalling analysis possible.
     Most consumer setups can't do this.
3. **Acoustic mode is still covered, if** the sensors report MIDI with the mute rail disengaged.
   The guide recommends calibrating "with the mute rail turned off (piano playing loud)", which suggests the sensors work regardless of the rail.
   Not stated explicitly. Experiment H2.
4. **Audio recording is optional.** Practising on the real acoustic piano and capturing it with a microphone is useful for listening back.
   It is also how one would study tone and resonance, which MIDI can't represent.
   Alignment with MIDI is then a simple synchronisation problem, not transcription.
5. **Windows MIDI caveat** [reported, verify in Session 2]: classic Windows MIDI (WinMM) lets only one application open a device at a time.
   If MuseScore or a DAW holds the adsilent, the browser can't.
   The newer Windows MIDI Services stack is meant to allow multiple clients; check whether it is active on this machine.

## Experiments

### H1. Basic MIDI capture (≈10 minutes, user)

1. Connect the adsilent 2 USB-C port to the PC with a USB-C to USB-A or USB-C cable.
2. Open <https://studiocode.dev/midi-monitor/> or <https://www.midimonitor.org/> in Chrome or Edge. Any Web MIDI monitor works; the project will make its own in Session 8.
3. Record, and copy the log into `experiments/h1-midi-capture/notes.md`:
   - The device name the browser reports.
   - One soft note and one loud note: the note-on velocity, and whether note-off arrives as `0x8n` with a release velocity or as note-on with velocity 0.
   - One slow release and one fast release of the same key: does the release velocity differ?
   - Damper pedal pressed slowly: a stream of CC64 values or only 0/127?
   - Left and middle pedals: which CC numbers, if any?
   - Anything on channels 2–4.

### H2. Acoustic mode (2 minutes)

Same as H1 with the mute rail **off**. Does MIDI still arrive?
Does the velocity distribution look similar?

### H3. Velocity response (later, Session 8)

Play a slow crescendo on one key, repeated 3 times.
Plot velocity against intended dynamic to see the usable range and the noise.
This establishes how many dynamic levels the measurement can honestly distinguish.

### H4. Timing jitter (later, Session 8)

Record an isochronous pattern played against a click, and the same MIDI played back.
Compare inter-onset-interval variance to separate human variability from capture jitter.
Expected capture jitter: about 1 ms over USB full-speed [speculative].

## Open questions

- Does MIDI arrive while the mute rail is off? (H2)
- What does "Continuous Note-On" do? (H1)
- What is the middle pedal on this EUP-111, and does it have a sensor?
- Can the browser and another app (e.g. MuseScore) use the device at the same time on this Windows install?
- How stable are velocities over weeks, given that the guide recommends periodic recalibration?
  If the project tracks dynamics over time, it must record calibration events.
