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


base_path = "../music/"
music_dict = {'mario_theme':{'path':"/mario/",
                             'filename':"smb1-Theme.mid"},
              'zelda_ovw':{'path':"/zelda/",
                           'filename':"z4-ovw.mid"},
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

def ticks_to_microseconds(tick, conversion_factor):
    return tick*conversion_factor

#######################################################

# Pick which file in the library to use
music_name = 'mario_theme'
path = base_path + music_dict[music_name]['path']
filename = music_dict[music_name]['filename']

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

    print current_voice

    if current_voice != []:

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

out_dir = "../out/" + music_name + "/"

if not os.path.isdir(out_dir+'config.txt'):
    os.mkdir(out_dir)

config_file = open(out_dir+'config.txt', 'w')
# myfile.write("#include <pitches.h>\n")

for j in [0,1,2]:
    print "down here"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    pitch_file = open(out_dir+'pitch{}.txt'.format(j), 'w')
    start_time_file = open(out_dir+'start_time{}.txt'.format(j), 'w')
    duration_file = open(out_dir+'duration{}.txt'.format(j), 'w')
    volume_file = open(out_dir+'volume{}.txt'.format(j), 'w')

    working = voice_list[j]
    # print working
    # print voice_list

    start_time = []
    duration = []
    volume = []
    note = []

    for i in range(len(working)):
        print "\n\n", i
        print working[i]
        start_time.append(working[i][0][0])
        duration.append(working[i][0][1] - working[i][0][0])
        volume.append(working[i][0][1])
        note.append(working[i][1])

    config_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        pitch_file.write("{}\n".format(freq_dict[note[i]]))

    # start_time_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        start_time_file.write("{}\n".format(start_time[i]))

    # duration_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        duration_file.write("{}\n".format(duration[i]))

    # volume_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        volume_file.write("{}\n".format(volume[i]))

    pitch_file.close()
    start_time_file.close()
    duration_file.close()
    volume_file.close()

config_file.close()

