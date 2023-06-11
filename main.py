import cv2
import sys


def move(arr):
    if len(arr) == 0:
        return None
    
    if type(arr) == list:
        out = arr[0]
        arr.pop(0)
        return out

def main():

    usage ="Usage: python3 main.py [filename] -out [width] [height]\nNote if no filename is given, the program will use the camera.\nNote if no width and height is given, the program will use the default width and height.\nNote if no height is given, the program will calculate the height based on the width."

    # read arguments

    args = sys.argv
    filename = None
    outWidth = 0
    outHeight = 0
    if len(args) > 0:
        args.pop(0)
        while len(args) > 0:
            match args[0]:
                case "-out":
                    args.pop(0)
                    outWidth = int(move(args))
                    try:
                        outHeight = int(move(args))
                    except:
                        outHeight = 0
                case "-h":
                    print(usage)
                    return 0
                case "-help":
                    print(usage)
                    return 0
                case default:
                    filename = move(args)

    characters = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
    

    if not filename:
        # # Read camera
        cap = cv2.VideoCapture(0)

        # # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Unable to read camera feed")

        _, frame = cap.read()
    else:
        # # Read image from file
        frame = cv2.imread(filename)

    # # Check if frame is empty
    if frame is None:
        print("Unable to open image")
        sys.exit()

    if outWidth != 0 and outHeight != 0:
        frame = cv2.resize(frame, (outWidth, outHeight))
    elif outWidth != 0 and outHeight == 0:
        frame = cv2.resize(frame, (outWidth, int(frame.shape[0] * outWidth / frame.shape[1])))
    else:
        scale_percent = 0.25
        frame = cv2.resize(frame, (0, 0), fx=scale_percent, fy=scale_percent)

    outstring = ""
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):

            BGRcolor = frame[i][j]
            color = BGRcolor[::-1]

            hsb = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            brightness = hsb[i][j][2]

            charcolor = hsb.copy()
            charcolor[i][j][2] = 255
            charcolor = cv2.cvtColor(charcolor, cv2.COLOR_HSV2RGB)
            charcolor = charcolor[i][j]

            character = characters[int(brightness / 25.5)]

            outstring += f"\033[48;2;{color[0]};{color[1]};{color[2]}m\033[38;2;{charcolor[0]};{charcolor[1]};{charcolor[2]}m{character}{character}"
        outstring += "\x1b[0m\n"
    print(outstring)

    cap.release()

    return 0


if __name__ == "__main__":
    main()