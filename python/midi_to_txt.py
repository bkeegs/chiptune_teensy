import midi
import os
from notefreq_list import list_notes, list_freq

freq_dict = {}
for i in range(len(list_notes)):
    freq_dict[list_notes[i]] = list_freq[i]

notes_list = ['C','CS','D','DS','E','F','FS','G','GS','A','AS','B']


note_dict = {}
counter = 24
for j in range(9):
    for i in range(len(notes_list)):
        note_dict[counter] = 'NOTE_' + notes_list[i] + str(j+1)
        counter += 1


base_path = "../music_files/"
music_dict = {'mario_theme':{'path':"/mario/",
                             'filename':"smb1-Theme.mid"},
              'zelda_ovw':{'path':"/zelda/",
                           'filename':"z4-ovw_edited.mid"},
              'tetris':{'path':"/tetris/",
                        'filename':"music-a-3-.mid"},
              'pkmn_opening':{'path':"/pkmn/",
                              'filename':"opening-2-.mid"},
              'pkmn_title':{'path':"/pkmn",
                             'filename':"title-screen.mid"},
              'pkmn_caught':{'path':"/pkmn/",
                             'filename':"wild-pokemon-caught.mid"},
              'pkmn_pallet':{'path':"/pkmn/",
                             'filename':"pallet-town-2-.mid"},
              'pkmn_rival':{'path':"/pkmn/",
                            'filename':"rival-theme-2-.mid"},
              'pkmn_center':{'path':"/pkmn/",
                             'filename':"pokemon-center-3-.mid"},
              'pkmn_wild':{'path':"/pkmn/",
                           'filename':"wild-pokemon-battle2.mid"},
              "pkmn_oak":{'path':"/pkmn/",
                          'filename':"oak-s-lab.mid"}}

# Some midi files use Note_On/Note_Off to mark start/stop
# Making a dictionary to track which files in our library use this convention
note_off_dict = {}
note_off_dict[0] = "mario_theme"
note_off_dict[1] = "zelda_ovw"

def ticks_to_microseconds(tick, conversion_factor):
    return tick*conversion_factor

#######################################################

# Pick which file in the library to use
music_name = 'tetris'
path = base_path + music_dict[music_name]['path']
filename = music_dict[music_name]['filename']
print "\nConverting from midi for {}".format(music_name)
print "Midi file: {}\n\n".format(filename)

# Read in midi_file
pattern = midi.read_midifile(path + filename)
pattern.make_ticks_abs()
# print pattern

# Get rid of drum tracks for pkmn opening
if music_name == 'pkmn_opening':
    del(pattern[-2:])

if music_name in note_off_dict.values():
    use_note_off_flag = 1
else:
    use_note_off_flag = 0

# Set default bpm to 120, then check if file specifies a different BPM
BPM = 120.
for entry in pattern[0]:
    if type(entry) == midi.SetTempoEvent:
        BPM = entry.bpm
        print "Updated BPM to ", entry.bpm

resolution = float(pattern.resolution)
microseconds_per_tick = 1e6*(60/BPM)/resolution

voice_list = []
end_note_found = 0

for track in pattern:
    print track
    current_voice = []
    current_time = 0
    for k in range(len(track)):
        if type(track[k]) is midi.NoteOnEvent:
            current_time = ticks_to_microseconds(tick=track[k].tick, conversion_factor=microseconds_per_tick)
            current_voice.append([current_time, note_dict[track[k].data[0]], track[k].data[1], track[k].tick])

            if use_note_off_flag:
                if type(track[k+1]) is midi.NoteOffEvent:
                    current_voice[-1][0] = (current_voice[-1][0], ticks_to_microseconds(tick=track[k+1].tick, conversion_factor=microseconds_per_tick))

        else:
            # print "not a note"
            pass

    if current_voice != []:

        print current_voice


        if not use_note_off_flag:
            for i in range(len(current_voice)):
                try:
                    current_voice[i]
                except IndexError:
                    break

                end_note_found = 0
                counter = 1
                if current_voice[i][-2] != 0:
                    while not end_note_found:
                        if current_voice[i+counter][1] == current_voice[i][1]:
                            end_note_found = 1
                            current_voice[i][0] = (current_voice[i][0], current_voice[i+counter][0])
                            del(current_voice[i+counter])
                        else:
                            counter += 1
        voice_list.append(current_voice)
            # break

print len(voice_list)

pitch_dict = {}
start_time_dict = {}
duration_dict = {}

for j in [0, 1, 2]:

    working = voice_list[j]

    pitch_working = []
    start_time_working = []
    duration_working = []

    for i in range(len(working)):
        print working[i]
        # print working[i]
        pitch_working.append(working[i][1])
        start_time_working.append(working[i][0][0])
        duration_working.append(working[i][0][1] - working[i][0][0])
        # volume.append(working[i][0][1])

    pitch_dict[j] = pitch_working
    start_time_dict[j] = start_time_working
    duration_dict[j] = duration_working

teensy_out_dir = "../generated_teensy_code/" + music_name + "_teensy/"

if not os.path.isdir(teensy_out_dir):
    os.mkdir(teensy_out_dir)

teensy_file = open(teensy_out_dir+ music_name + "_teensy.ino", 'w')
teensy_file.write("#include <pitches.h>\n\n")

for voice_num in range(len(pitch_dict.keys())):
    pitch_list = pitch_dict[voice_num]
    start_time_list = start_time_dict[voice_num]
    duration_list = duration_dict[voice_num]

    teensy_file.write("int melody{}[] = {{\n".format(voice_num))
    for i in range(len(pitch_list)):
        teensy_file.write("{},\n".format(pitch_list[i]))
    teensy_file.write("}};\n\n".format())

    teensy_file.write("int start_time{}[] = {{\n".format(voice_num))
    for i in range(len(start_time_list)):
        teensy_file.write("{},\n".format(start_time_list[i]))
    teensy_file.write("}};\n\n".format())

    teensy_file.write("int duration{}[] = {{\n".format(voice_num))
    for i in range(len(duration_list)):
        teensy_file.write("{},\n".format(duration_list[i]))
    teensy_file.write("}};\n\n".format())

practice_filename = "C:/Users/bkeegan/Desktop/tester_dev/repos/chiptune_teensy/teensy_code/bottom_matter/bottom_matter.ino"
practice_file = open(practice_filename, 'r')
x = practice_file.read()
print x
teensy_file.write(x)

teensy_file.close()







