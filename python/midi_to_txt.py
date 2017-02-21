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
                              'filename':"opening-2-no_drums.mid"},
              'pkmn_title':{'path':"/pkmn/",
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
                           'filename':"wild-pokemon-battle.mid"},
              "pkmn_oak":{'path':"/pkmn/",
                          'filename':"oak-s-lab.mid"}}

def ticks_to_microseconds(tick, conversion_factor):
    return tick*conversion_factor

#######################################################
for key in music_dict.keys():
    # Pick which file in the library to use
    music_name = key
    path = base_path + music_dict[music_name]['path']
    filename = music_dict[music_name]['filename']
    print "\nConverting from midi for {}".format(music_name)
    print "Midi file: {}\n\n".format(filename)

    # Read in midi_file
    pattern = midi.read_midifile(path + filename)
    pattern.make_ticks_abs()

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

    def remove_values_from_list(the_list, val):
       return [value for value in the_list if type(value) != val]



    for track in pattern:
        current_voice = []
        current_time = 0

        # Clean up track so only has NoteOn and NoteOff Events
        track = [entry for entry in track if ((type(entry) == midi.NoteOnEvent) or (type(entry) == midi.NoteOffEvent))]

        for k in range(len(track)):

            if track[k].data != []:

                if (type(track[k]) is midi.NoteOnEvent) and (track[k].data[1] != 0):
                    current_time = ticks_to_microseconds(tick=track[k].tick, conversion_factor=microseconds_per_tick)
                    current_voice.append([current_time, note_dict[track[k].data[0]], track[k].data[1], track[k].tick])

                    if (track[k+1].data[1] == 0) or (type(track[k+1]) is midi.NoteOffEvent): # pseudo-note off event found:
                        current_voice[-1][0] = (current_voice[-1][0], ticks_to_microseconds(tick=track[k+1].tick, conversion_factor=microseconds_per_tick))
                    else:
                        for entry in track[k-5:k+5]:
                            print entry
                        print 'k = ', k
                        print "No end note found!"
                        exit()

        if current_voice != []:
            voice_list.append(current_voice)

    pitch_dict = {}
    start_time_dict = {}
    duration_dict = {}

    for j in [0, 1, 2]:

        working = voice_list[j]

        pitch_working = []
        start_time_working = []
        duration_working = []

        for i in range(len(working)):
            pitch_working.append(working[i][1])
            start_time_working.append(working[i][0][0])
            duration_working.append(working[i][0][1] - working[i][0][0])

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

    # Now that timing and pitch arrays have been added to the new .ino file, add the "footer
    # This contains all main code being executed on the Teensy
    teensy_footer_filename = "../include/teensy_exec_code.txt"
    teensy_footer_file = open(teensy_footer_filename, 'r')
    teensy_code = teensy_footer_file.read()
    teensy_file.write(teensy_code)

    teensy_file.close()







