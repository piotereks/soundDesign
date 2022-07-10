ImproTool (python) next steps
# General principles
1. Dependency between pattern and rythm (default, configurable, on-the fly)
2. Implementation of rythm pattern (isobar, some manual patterns with CC codes?)

Define base pattern (as dataset) and play it
Adopt combination o patterns, scales and note leghts (pattern vs decorators)

3. Detect read song bpm and adopt played patterns
4. Pattern can be selected, can be random
5. Add keyboard or midi steering for scales, pattern, leghts
6. Add pattern selection depending on interval provided from keyboard
7. Later scales can be suggested, selected, randomised,
8. Predefined sets for different kind of music e.g. blues kater jazz, any others types
9. Add your scales to scale.py
Eventually Gather different backgrounds tracks for standard genres
Multi-instrument support
Tensor flow/magenta generations? Or maybe tensor selected impro patterns


Problems:
NA 1) How to deal with lengths of notes and tempo, specially when converting to midi events.
This calculation seem to be heart of playing.
Can isobar be used for that?

2) Midi clock support.

OK 3) when using isobar and timeline - how to add additional sounds  - timeline.background() instead of run()


What to do with Rythmn patterns:
(Idea: Express patterns with ticks)
For start just focus on standard patterns (not necessarily equally distributed,but start them first).
Skip for a moment Ornamentacje and maybe focus on diminuncje (which are about how to come from one tone to other, but
but have slightly higher resolution as patterns.


Standard patterns do as rule of beat (length of beat)
So, when you have measure 4/4 - there are quarter notes as main note (and beat) and there is 4 of quarter notes in beat.
Phrase can be like 4  bars (16 beats) or (most likely) 8  or 16 bars.

e.g. 3/4 give 3 quarternotes in bar.
e.g. 3/8 give 3 eights
e.g. 5/4 give 5 quarternotes.

Base is 4/4
Important rythms:
* 8x8ths/beat (accents 1,5,3,7)
* triple  (3-trios for 2x8th) => 12 trios/beat (accents 1,7,4,10)
* kwintuplet (5-kwin for 4x8ths)  => 10 kwintuplets (accents 1,6)
* 5/4 accents are 1,4,6
Accents
1234567890
x  x  x x x
1  2  3 4

Accents in 4/4 can be (128-level velocity) 105,80,95,80


"Diminucje" pochody dzwiękowe.
Express as half-beat e.g. 4/4  - only covers 2 quarter notes (could be theoretically decreased)
* 1/2
* 1/4 + 1/8 + 1/8
* 1/8 + 1/8 + 1/4
* 4x 1/8
*  1/8+.  1/16    4x 1/16
*  1/8  2x1/16    4x 1/16
*  8x 1/16

Decision to be taken:
* implement as part of isobar sequences (of velocity and duration - after aligning values)
NA * or using own structures (but maybe later applying to sequences)  - better to be as int/and fractint .

PSequence for time could be confusing since it changes with change of tempo (or resolution).
I want to have possibilitiy to calculate that on the fly.
Or maybe there is psequence easy recalculation....

# Synchronicity
Midi clock has
clock, start, stop, continue (as base).
is missing sync option though.
Check here is to evaluate what are the option of syncing.


Work on easy example first as prototype on how you want to play.


## Scheduling patterns with clock + actually synchronization
timeline.background() allows any timing (this is live).
This actually can be achieved by getting one track with click track and second track listening to that.
Synchronization by click gives to preserve tempo. How to synch with beats?
- scheduling of patterns work, but really this is about synchronization with e.g. ableton now.

## create loop with pattern ref replaced by other pattern (using sync) - Done

## check different sources of midi clock
### midi file being played (by mido, but also by diff mid players)
Received MIDI: program_change channel=0 program=0 time=0  = PC message might be used to sync since it goes at start

### midi clock tool
Currently metronome and play along open midi is done.

### ableton (both midi clock version, like "Ableton? sync protocol" or OSC
Ableton midi sync dump
2022-06-09 17:36:04.621986  - Received MIDI: continue time=0
2022-06-09 17:36:10.622986  - Received MIDI: stop time=0
2022-06-09 17:36:10.622986  - Received MIDI: songpos pos=31 time=0
2022-06-09 17:36:10.622986  - Received MIDI: continue time=0
2022-06-09 17:36:11.935008  - Received MIDI: stop time=0
2022-06-09 17:36:12.815977  - Received MIDI: songpos pos=0 time=0
2022-06-09 17:36:12.816971  - Received MIDI: start time=0
2022-06-09 17:36:15.021985  - Received MIDI: stop time=0
2022-06-09 17:36:18.888976  - Received MIDI: songpos pos=0 time=0
2022-06-09 17:36:18.888976  - Received MIDI: start time=0
2022-06-09 17:36:21.466991  - Received MIDI: stop time=0


### by beat-detection python libraries (if any)
### can tick be used for sync (check what happens if isobar tick is used on output where clock being sent)
This is not applicable. Tick is I guess to create one tick in time.

# Tracker
Tracker compose of series of pattern provided as list when scheduling timeline 
- this one is done
## Run tracker along with some ready midi file
I can play midi and play my part.


# User Predefined beats and pattern + apply scale
## Take your patterns, but play using specific scale.
Currently, patterns have ready midi notes.
## Extend isobar with your scales
## Appregios as scales?
## Work with classes always