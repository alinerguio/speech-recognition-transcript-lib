import os
import sys
import datetime
import pandas as pd
import speech_recognition as sr


def log_time_specifics(start_time, end_time, dataset, quantity_files):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_specifics_wit.txt'):
        f = open('execution_time_specifics_wit.txt', 'a')
    else:
        f = open('execution_time_specifics_wit.txt', 'w')
        
    f.write('\n' + dataset + ';' +  str(quantity_files) + ';' + str(process_time))
    f.close()


def iterate_folder(r, main_dir, key):
    all_folders = [folder for folder in os.listdir(main_dir) if '.' not in folder]
    
    for folder in all_folders:
        start_time = datetime.datetime.now()
        quantity_files = 0 

        curr_dir = main_dir + '/' + folder
        transc_folder = []

        all_files = [file for file in os.listdir(curr_dir) if '.wav' in file]

        if not(os.path.isdir('./transcriptions-wit/')):
            os.mkdir('./transcriptions-wit/')

        output_path = './transcriptions-wit/' + folder + '.csv'

        if os.path.isfile(output_path):
            files_transcripted = pd.read_csv(output_path)
            files_transcripted_list = files_transcripted.file.tolist()
            all_files = [file for file in all_files if file not in files_transcripted_list]


        for file in all_files:
            try:
                resp = transcribe(r, curr_dir + '/' + file, key)

                final_result = pd.DataFrame([{'transcriptions': resp, 'file': file, 'database': folder}])
                final_result.to_csv(output_path, mode='a', header=not os.path.exists(output_path))
            
            except Exception as e:
                print('Not possible to proceed to transcript file: ' + file)
                print(e)

            except KeyboardInterrupt:
                print('\nKeyboardInterrupt: stopping manually')
                end_time = datetime.datetime.now()
                log_time_specifics(start_time, end_time, folder, quantity_files)

                sys.exit()

        end_time = datetime.datetime.now()
        log_time_specifics(start_time, end_time, folder, quantity_files)
        

def transcribe(r, file, key):
    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        resp = r.recognize_wit(audio, key=key)
        print("Wit.ai thinks you said " + resp)
        return resp
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
        return None
    except sr.RequestError as e:
        print('Not possible to request now, file:' + file)
        return 'Retry or review code. Error: ' + str(e)


def log_time(start_time, end_time):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_wit.txt'):
        f = open('execution_time_wit.txt', 'a')
        f.write('\n' + str(process_time))
        f.close()
    else:
        f = open('execution_time_wit.txt', 'w')
        f.write(str(process_time))
        f.close()


if __name__ == '__main__':
    main_dir = '../data/'
    key = None

    r = sr.Recognizer()

    if key == None:
        if len(sys.argv) != 2:
            print('usage: python ' + sys.argv[0] + ' <wit-token>')
            exit(1)
        key = sys.argv[1]

    start_time = datetime.datetime.now()

    try:
        iterate_folder(r, main_dir, key)
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
    except Exception as e:
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
        print(e)