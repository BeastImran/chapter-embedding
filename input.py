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
