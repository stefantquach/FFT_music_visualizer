import pyaudio
import argparse
import wave
import time
import curses
from curses import wrapper
import numpy as np

CHUNK = 1024

p = pyaudio.PyAudio()

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True)

args = parser.parse_args()

# open file
wf = wave.open(args.input, 'rb')
n_channels = wf.getnchannels()


# Print the visualizer
# data is a 1D array of [0, 1) normalized values
def print_visualizer(data, scr):
    # getting screen length and height
    length = 20
    height = 10
    # print(data)
    
    num_buckets = len(data)
    bucket_width = length//num_buckets

    bucket_str = "#"*bucket_width
    for i in range(num_buckets):
        # printing out the column
        bucket_height = int(data[i]*height)
        for j in range(bucket_height):
            # scr.addstr(i*bucket_width, j, bucket_str)
            a= 0
    
    # scr.refresh()


def UGETCHAR_(scr):
    h = scr.getch()
    if h == 3:
        raise KeyboardInterrupt
    if h == 26:
        raise EOFError
    return h



# if __name__ == '__main__':
def main(stdscr):
    # initialize curses
    # stdscr = curses.initscr()
    # curses.noecho()
    # curses.cbreak()
    # stdscr.keypad(True)
    stdscr.nodelay(True)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),                
                    rate=wf.getframerate(),                
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        UGETCHAR_(stdscr)
        int_data = np.frombuffer(data, dtype=np.uint16)
        if int_data.size < CHUNK*n_channels:
            # pad with zeros
            int_data = np.pad(int_data, (0, CHUNK*n_channels - int_data.size), 'constant')
        int_data = int_data.reshape(CHUNK, n_channels)
        avg_data = np.mean(int_data, 1) # take average across channels
        # print(avg_data.shape)
        # raw_fft_mag = np.abs(np.fft.rfft(avg_data))
        raw_fft_mag = np.zeros(len(avg_data))
        # stdscr.addstr(1,2, "POOPOO")
        print_visualizer(raw_fft_mag, stdscr)
        
        stdscr.refresh()

        stream.write(data)
        data = wf.readframes(CHUNK)

    # stream.stop_stream()
    # stream.close()
    wf.close()

    p.terminate()

    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()
    # curses.endwin()


wrapper(main)
# main(0)