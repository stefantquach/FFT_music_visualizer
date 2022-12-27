import pyaudio
import argparse
import wave
import time
import curses
from curses import wrapper
import numpy as np

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
    length = curses.COLS
    height = curses.LINES
    print(data)
    
    num_buckets = len(data)
    bucket_width = length//num_buckets

    bucket_str = "#"*bucket_width
    for i in range(num_buckets):
        # printing out the column
        bucket_height = int(data[i]*height)
        for j in range(bucket_height):
            scr.addstr(i*bucket_width, j, bucket_str)
            # a= 0
    
    scr.refresh()

# if __name__ == '__main__':
def main(stdscr):
    # initialize curses
    # stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    visualizer_data = []

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        int_data = np.frombuffer(data, dtype=np.uint16)
        if int_data.size < frame_count*n_channels:
            # pad with zeros
            int_data = np.pad(int_data, (0, frame_count*n_channels - int_data.size), 'constant')
        int_data = int_data.reshape(frame_count, n_channels)
        avg_data = np.mean(int_data, 1) # take average across channels
        # print(avg_data.shape)
        raw_fft_mag = np.abs(np.fft.rfft(avg_data))
        # print_visualizer(raw_fft_mag, stdscr)
        # stdscr.addstr(1,2, "POOPOO")
        visualizer_data = raw_fft_mag

        # To play out data, just leave this in
        return (data, pyaudio.paContinue)

    def UGETCHAR_(scr):
        h = scr.getch()
        if h == 3:
            raise KeyboardInterrupt
        if h == 26:
            raise EOFError
        return h


    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                 channels=wf.getnchannels(),                
    #                 rate=wf.getframerate(),                
    #                 output=True,                
    #                 stream_callback=callback)

    # stream.start_stream()

    i = 0
    # while stream.is_active():
    while True:
        UGETCHAR_(stdscr) # exit when ctrl+C
        # print_visualizer(visualizer_data, stdscr)
        stdscr.addstr(1,2, "POOPOO %d" % i)
        stdscr.refresh()
        
        time.sleep(0.1)

    # stream.stop_stream()
    # stream.close()
    wf.close()

    p.terminate()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


# # wrapper(main)
# main(0)