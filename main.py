import functions


def main():

    # video's path
    video_path = functions.take_path_input("video")
    if video_path:

        # timestamps text file path
        text_path = functions.take_path_input("timestamps text file")
        if text_path:

            # check if the conversion of timestamps to required format was successfull
            converted = functions.convert_to_required_format(text_path)
            if converted:

                # final result. operation success or failed
                sucess = functions.embed_chapters(converted, video_path, text_path)

                if sucess:
                    print("\nHopefully! successfull\n")
                else:
                    print("\nSomething went wrong!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. reason: KeyboardInterrupt")
    except Exception as e:
        print("\nProgram terminated. Exception occured.\nerror is",e)