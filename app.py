import os
import music_tag
import argparse


def process_arguments():
    parser = argparse.ArgumentParser(description="Application for merging .lrc file to its audio file")
    parser.add_argument('--path', help="Directory to scan and merge .lrc and its audio file")
    return parser.parse_args()



def search_files_by_extension(directory, extension):
    matching_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            if filename.endswith(f".{extension}"):
                matching_files.append(full_path)
    return matching_files

def setLyrics(mpath,lpath):
    music = music_tag.load_file(mpath)
    if not music['lyrics']:
        music['lyrics'] = getLrc(lpath)
        music.save()
        print('done')

def getLrc(file_path):
    try:
        with open(file_path, 'r') as file:
            lrc_content = file.read()
            return lrc_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    args = process_arguments()
    if(not args.path):
        print("No path specified..")
        print("use --path [path]")
        exit()
    directory_path = args.path

    lrcFiles = search_files_by_extension(directory_path, ".lrc")

    if lrcFiles:
        for file_path in lrcFiles:
            filename_only = os.path.basename(file_path)
            if os.path.exists(file_path.replace('.lrc','.mp3')):
                setLyrics(file_path.replace('.lrc','.mp3'),file_path)
            elif os.path.exists(file_path.replace('.lrc','.flac')):
                setLyrics(file_path.replace('.lrc','.flac'),file_path)
            elif os.path.exists(file_path.replace('.lrc','.m4a')):
                setLyrics(file_path.replace('.lrc','.m4a'),file_path)
            else:
                print("Unknown format ", file_path);

    else:
        print(f"No files with the extension '.{file_extension}' found.")