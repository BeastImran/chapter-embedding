# will use to take the path inputs and validate
def take_path_input(file):
    from os.path import isfile
    try:
        from magic import from_file
    except Exception as e:
        print("Brutal Error occured. Please install python-magic module!\ntry \"pip install python-magic\" to install.\nexception occured:",e)
        exit()


    video = file == "video"
    path = input(f"Enter the path for {file}: ")

    if isfile(path):
        if video:
            if "video" in from_file(path, mime=True):
                print("\nVideo file identified!\n")
                return path
            else:
                print("\nPlease enter a valid VIDEO file path!\n")
                return
        else:
            if "text" in from_file(path, mime=True):
                print("\nText file identified!\n")
                return path
            else:
                print("\nPlease enter a valid TEXT file path!\n")
                return
    else:
        print("\nMake sure you entered the right FILE PATH!\n")


# will return converted format as a list
def convert_to_required_format(path):
    try:
        chapters = []
        with open(path, 'r') as f:
            content = f.read()
            if len(content) > 0:
                for line in content.split('\n'):
                   
                    # extracting content
                    line = line.strip().split()
                    if len(line) > 0:
                        timestamp = line[0].split(':')

                        # convert to hrs, mins and hrs
                        if len(timestamp) == 3:
                            print("timestamp: 3")
                            hours = int(timestamp[0])
                            minutes = int(timestamp[1])
                            secs = int(timestamp[2])
                        elif len(timestamp) == 2:
                            print("timestamp: 2")
                            hours = 0
                            minutes = int(timestamp[0])
                            secs = int(timestamp[1])
                        

                        # calculating the required format time
                        minutes = (hours * 60) + minutes
                        seconds = secs + (minutes * 60)
                        final_time = (seconds * 1000)

                        title = ' '.join(line[1:])

                        print(f"{ final_time } : { title }")

                        chapter = {
                            "title": title,
                            "start_time": final_time
                        }
                        chapters.append(chapter)

            else:
                print("\nFile is empty!\n")
        
        for i in range(len(chapters)-1):
            if not chapters[i]["start_time"] < chapters[i+1]["start_time"]:
                print(f'There is some timing problem with the timestamps text file.\nProbably the timestamp order is wrong or of wrong format!\nProblem after the \'{chapters[i]["title"]}\' title!')
                break
        else:
            return chapters
    except Exception as e:
        print("\nSomething is not right with the timestamps text file!\nProbably the timestamps are not in right format!\nerror:",e)


# will output chapter embeded video to video's path + output directory
def embed_chapters(chapters, video, text_path):
    from os import listdir, mkdir
    from os.path import basename, join, isdir
    import subprocess


    try:
        video_name = basename(video)
        video_path = video.replace(video_name, '')
        OUTPUT_VIDEO_PATH = join(video_path,"output")
        OUTPUT_VIDEO_NAME = join(OUTPUT_VIDEO_PATH,basename(video_name))

        print(f"\nOUTPUT_VIDEO_NAME: {OUTPUT_VIDEO_NAME}\nOUTPUT_VIDEO_PATH: {OUTPUT_VIDEO_PATH}")
        if video_path == '':
            video_path = '.'
        folder_contents = listdir(video_path)
        if "output" in folder_contents:
            idx = folder_contents.index('output')
            if not isdir(folder_contents[idx]):
                try:
                    mkdir(OUTPUT_VIDEO_PATH)
                except:
                    print("Expected")
            else:
                pass
        else:
            print("\ncreated output folder\n")
            mkdir(OUTPUT_VIDEO_PATH)

        FFMETADATAFILE_FILE_PATH = join(OUTPUT_VIDEO_PATH, "FFMETADATAFILE.txt")
        EXTRACTION_CMD = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic', '-i', video, '-f', 'ffmetadata', FFMETADATAFILE_FILE_PATH]
        EMBEDDING_CMD = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic', '-i', video, '-i', FFMETADATAFILE_FILE_PATH, '-map_metadata', '1', '-codec', 'copy', OUTPUT_VIDEO_NAME]

        final_format = ""
        # covert to required format
        for i in range(len(chapters) - 1):

            chapter_info = chapters[i]
            title = chapter_info["title"]
            start_time = chapter_info["start_time"]
            end_time = chapters[i + 1]["start_time"] - 1

            final_format += f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={start_time}\nEND={end_time}\ntitle={title}\n\n"

        print("\nCreated the chapters final format\n")

        print("\nMetadata extraction started")
        subprocess.run(EXTRACTION_CMD)

        print("Metadata extraction completed\n")

        with open(FFMETADATAFILE_FILE_PATH, 'a+') as f:
            f.write(final_format)
        
        print("\nEmbedding started")
        subprocess.run(EMBEDDING_CMD)

        print("Embedding completed\n")
        return True

    except Exception as e:
        print("\nSomething went wrong during the embedding process!\nerror:",e)
        return False
