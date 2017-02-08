import midi
import os

list_freq = ['31',
'33',
'35',
'37',
'39',
'41',
'44',
'46',
'49',
'52',
'55',
'58',
'62',
'65',
'69',
'73',
'78',
'82',
'87',
'93',
'98',
'104',
'110',
'117',
'123',
'131',
'139',
'147',
'156',
'165',
'175',
'185',
'196',
'208',
'220',
'233',
'247',
'262',
'277',
'294',
'311',
'330',
'349',
'370',
'392',
'415',
'440',
'466',
'494',
'523',
'554',
'587',
'622',
'659',
'698',
'740',
'784',
'831',
'880',
'932',
'988',
'1047',
'1109',
'1175',
'1245',
'1319',
'1397',
'1480',
'1568',
'1661',
'1760',
'1865',
'1976',
'2093',
'2217',
'2349',
'2489',
'2637',
'2794',
'2960',
'3136',
'3322',
'3520',
'3729',
'3951',
'4186',
'4435',
'4699',
'4978']


list_notes = ['NOTE_B0',
'NOTE_C1',
'NOTE_CS1',
'NOTE_D1',
'NOTE_DS1',
'NOTE_E1',
'NOTE_F1',
'NOTE_FS1',
'NOTE_G1',
'NOTE_GS1',
'NOTE_A1',
'NOTE_AS1',
'NOTE_B1',
'NOTE_C2',
'NOTE_CS2',
'NOTE_D2',
'NOTE_DS2',
'NOTE_E2',
'NOTE_F2',
'NOTE_FS2',
'NOTE_G2',
'NOTE_GS2',
'NOTE_A2',
'NOTE_AS2',
'NOTE_B2',
'NOTE_C3',
'NOTE_CS3',
'NOTE_D3',
'NOTE_DS3',
'NOTE_E3',
'NOTE_F3',
'NOTE_FS3',
'NOTE_G3',
'NOTE_GS3',
'NOTE_A3',
'NOTE_AS3',
'NOTE_B3',
'NOTE_C4',
'NOTE_CS4',
'NOTE_D4',
'NOTE_DS4',
'NOTE_E4',
'NOTE_F4',
'NOTE_FS4',
'NOTE_G4',
'NOTE_GS4',
'NOTE_A4',
'NOTE_AS4',
'NOTE_B4',
'NOTE_C5',
'NOTE_CS5',
'NOTE_D5',
'NOTE_DS5',
'NOTE_E5',
'NOTE_F5',
'NOTE_FS5',
'NOTE_G5',
'NOTE_GS5',
'NOTE_A5',
'NOTE_AS5',
'NOTE_B5',
'NOTE_C6',
'NOTE_CS6',
'NOTE_D6',
'NOTE_DS6',
'NOTE_E6',
'NOTE_F6',
'NOTE_FS6',
'NOTE_G6',
'NOTE_GS6',
'NOTE_A6',
'NOTE_AS6',
'NOTE_B6',
'NOTE_C7',
'NOTE_CS7',
'NOTE_D7',
'NOTE_DS7',
'NOTE_E7',
'NOTE_F7',
'NOTE_FS7',
'NOTE_G7',
'NOTE_GS7',
'NOTE_A7',
'NOTE_AS7',
'NOTE_B7',
'NOTE_C8',
'NOTE_CS8',
'NOTE_D8',
'NOTE_DS8']


freq_dict = {}
for i in range(len(list_notes)):
    freq_dict[list_notes[i]] = list_freq[i]

print freq_dict

notes_list = ['C','CS','D','DS','E','F','FS','G','GS','A','AS','B',]

note_dict = {}
counter = 24
for j in range(9):
    for i in range(len(notes_list)):
        note_dict[counter] = 'NOTE_' + notes_list[i] + str(j+1)
        counter += 1


base_path = "../music/"


# path = "/mario/"
# filename = "smb1-Theme.mid"

# path = "/pkmn/"
# filename = "opening-2-.mid"
#
# path = "/pkmn/"
# filename = "title-screen.mid"
#
# path = "/pkmn/"
# filename = "wild-pokemon-caught.mid"
#
# path = "/pkmn/"
# filename = "pallet-town-2-.mid"
#
# path = "/pkmn/"
# filename = "rival-theme-2-.mid"
#
# path = "/tetris/"
# filename = "music-a-3-.mid"
#
# path = "/pkmn/"
# filename = "pokemon-center-3-.mid"
#
# path = "/pkmn/"
# filename = "wild-pokemon-battle2.mid"
#
# path = "/pkmn/"
# filename = "oak-s-lab.mid"

path = "/zelda/"
filename = "z4-ovw.mid"

note_off_dict = {}
note_off_dict[0] = "smb1-Theme.mid"

path = base_path + path

pattern = midi.read_midifile(path + filename)
pattern.make_ticks_abs()
print pattern

# Get rid of drum tracks for pkmn
if filename == "opening-2-.mid":
    del(pattern[-2:])

if filename in note_off_dict.values():
    use_note_off_flag = 1
else:
    use_note_off_flag = 0


BPM = 120.
for entry in pattern[0]:
    if type(entry) == midi.SetTempoEvent:
        BPM = entry.bpm
        print "Updated BPM to ", entry.bpm


def ticks_to_microseconds(tick, conversion_factor):
    return tick*conversion_factor


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
                # print current_voice
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

out_dir = "./out/"+path[2:-1]+"_"+filename[:-3]+"/"

config_file = open(out_dir+'config.txt', 'w')
# myfile.write("#include <pitches.h>\n")

for j in [0,1,2]:
    print "down here"


    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    melody_file = open(out_dir+'melody{}.txt'.format(j), 'w')
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
        melody_file.write("{}\n".format(freq_dict[note[i]]))

    # start_time_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        start_time_file.write("{}\n".format(start_time[i]))

    # duration_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        duration_file.write("{}\n".format(duration[i]))

    # volume_file.write("{}\n".format(len(working)))

    for i in range(len(working)):
        volume_file.write("{}\n".format(volume[i]))

    melody_file.close()
    start_time_file.close()
    duration_file.close()
    volume_file.close()

config_file.close()

