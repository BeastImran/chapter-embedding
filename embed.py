
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
            if not isdir(join(video_path,folder_contents[idx])):
                    mkdir(OUTPUT_VIDEO_PATH)
        else:
            print("\ncreated output folder\n")
            mkdir(OUTPUT_VIDEO_PATH)

        FFMETADATAFILE_FILE_PATH = join(OUTPUT_VIDEO_PATH, "FFMETADATAFILE.txt")
        EXTRACTION_CMD = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic', '-i', video, '-f', 'ffmetadata', FFMETADATAFILE_FILE_PATH]
        EMBEDDING_CMD = ['ffmpeg', '-hide_banner', '-loglevel', 'panic', '-i', video, '-i', FFMETADATAFILE_FILE_PATH, '-map_metadata', '1', '-codec', 'copy', OUTPUT_VIDEO_NAME]

        final_format = ""
        # covert to required format
        for i in range(len(chapters) - 1):

            chapter_info = chapters[i]
            title = chapter_info["title"]
            start_time = chapter_info["start_time"]
            end_time = chapters[i + 1]["start_time"] - 1

            final_format += f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={start_time}\nEND={end_time}\ntitle={title}\n\n"
        start_time = end_time + 1
        try:
            end_time = int(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                            "format=duration", "-of",
                                            "default=noprint_wrappers=1:nokey=1", video],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT).stdout)) * 1000
        except:
            print("\n\nFailed to get the end time of video using ffprobe!\n")
            return False
        title = chapters[-1]["title"]
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
