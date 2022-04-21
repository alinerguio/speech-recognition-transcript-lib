import os
import sys
import ast
import datetime
import pandas as pd
import speech_recognition as sr

def log_time_specifics(start_time, end_time, dataset, quantity_files):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_specifics_vosk.txt'):
        f = open('execution_time_specifics_vosk.txt', 'a')
    else:
        f = open('execution_time_specifics_vosk.txt', 'w')
        
    f.write('\n' + dataset + ';' +  str(quantity_files) + ';' + str(process_time))
    f.close()


def iterate_folder(r, main_dir):
    all_folders = [folder for folder in os.listdir(main_dir) if '.' not in folder]
    
    for folder in all_folders:
        start_time = datetime.datetime.now()
        quantity_files = 0 
        
        curr_dir = main_dir + '/' + folder
        transc_folder = []

        all_files = [file for file in os.listdir(curr_dir) if '.wav' in file]

        if not(os.path.isdir('./transcriptions-vosk/')):
            os.mkdir('./transcriptions-vosk/')

        output_path = './transcriptions-vosk/' + folder + '.csv'

        if os.path.isfile(output_path):
            files_transcripted = pd.read_csv(output_path)
            files_transcripted_list = files_transcripted.file.tolist()
            all_files = [file for file in all_files if file not in files_transcripted_list]

        for file in all_files:
            try:
                resp = transcribe(r, curr_dir + '/' + file)
                resp = ast.literal_eval(resp)

                final_result = pd.DataFrame([{'transcriptions': resp['text'], 'file': file, 'database': folder}])
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


def transcribe(r, file):
    with sr.AudioFile(file) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        return r.recognize_vosk(audio, language='pt')
    except Exception:
        return None


def log_time(start_time, end_time):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_vosk.txt'):
        f = open('execution_time_vosk.txt', 'a')
        f.write('\n' + str(process_time))
        f.close()
    else:
        f = open('execution_time_vosk.txt', 'w')
        f.write(str(process_time))
        f.close()


if __name__ == '__main__':
    main_dir = '../data/'
    r = sr.Recognizer()
    start_time = datetime.datetime.now()

    try:
        iterate_folder(r, main_dir)
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
    except Exception as e:
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
        print(e)


