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
                    if len(line) > 1:
                        timestamp = line[0].split(':')

                        # convert to hrs, mins and hrs
                        if len(timestamp) == 3:
                            hours = int(timestamp[0])
                            minutes = int(timestamp[1])
                            secs = int(timestamp[2])
                        elif len(timestamp) == 2:
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
                print(f'\n\nThere is some timing problem with the timestamps text file.\nProbably the timestamp order is wrong or of wrong format!\nProblem after the \'{chapters[i]["title"]}\' title!')
                print("trying to sort the times!")
                chapters.sort(key=lambda x : x.get("start_time"))
                
                for i in range(len(chapters)-1):
                    if not chapters[i]["start_time"] < chapters[i+1]["start_time"]:
                        print(f'\n\nThere is some problem with the timestamps text file.\nNot able to sort and fix! Sorting didn\'t fix\nProblem after the \'{chapters[i]["title"]}\' title!')
                        break
                else:
                    print("\nSorting the timestamps worked!")
                    return chapters
        else:
            print("\n\nChapters returned")
            return chapters
    except Exception as e:
        print("\nSomething is not right with the timestamps text file!\nProbably the timestamps are not in right format!\nerror:",e)

