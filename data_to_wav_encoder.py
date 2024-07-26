import numpy as np
from scipy.io.wavfile import write
import random
import os.path


# ------------------------------------------------------------------------------

def remap_amplitude(frequency):
    """
    Remap amplitude based on frequency: greater amplitude at higher frequencies
    To counteract Dreams' smoothing function which boosts the lower frequencies!
    :param frequency:   int     frequency in Hz
    :return:            int     amplitude multiplier (between min amplitude and max amplitude)
    """
    # input bands
    frequency_min = 0
    frequency_max = 10000
    # output bands
    amplitude_min = 0.05
    amplitude_max = 1

    # get input bands fraction
    x = (frequency - frequency_min) / (frequency_max - frequency_min)
    x = max(0, x)
    x = min(1, x)

    # return output bands fraction
    return amplitude_min + (x * (amplitude_max - amplitude_min))


def generate_random_input_data_8bit(num_bytes):
    """
    Generate random blueprint for an audio file of num_samples samples,
    between min_bits and max_bits bits per sample
    :param num_bytes:   int
    :return:            list
    """
    data = []
    while len(data) < num_bytes * 8:
        # Generate one bit
        data.append(random.randint(0, 1))

    return data


def z_get_bytes(data):
    """
    Chunk image data into its constituent bytes
    :param data:    list    binary image data
    :return:        list
    """
    output = []
    i = 0
    while i < len(data):
        # Get one byte of data from input list
        byte = data[i:i+8]
        output.append(byte)

        # Next byte
        i += 8
    return output


def create_wav_file(data, filename, sample_length_seconds=1.0, samplerate=44100):
    """
    Encode image into .wav file
    :param data:                    list        Image binary data
    :param filename:                string      Output filename
    :param sample_length_seconds:   int         Length of output file in seconds
    :param samplerate:              int         Sample rate of generated output file
    :return:                        list        Waveform amplitude series of output file
    """
    output = []
    t = np.linspace(0., sample_length_seconds, int(sample_length_seconds * samplerate))  # time space for 1 sample

    # Shift output by half a sample length of silence so the midpoints are hit every 30*samplelength frames
    output += list(np.zeros(int(sample_length_seconds * samplerate/2)))

    i = 0
    while i < len(data):
        # Get one byte of data from input list
        byte = data[i:i+8]
        # Initialise an empty sample of length t
        output_sample = np.zeros_like(t)

        for j in range(8):
            bit = byte[j]
            if bit:
                # Generate sine wave with frequency corresponding to bit's position in the byte
                frequency = frequency_bands_hz[j]
                output_sample += max_amplitude * remap_amplitude(frequency) * np.sin(2. * np.pi * frequency * t)

        # Normalise to prevent amplitude from clipping above 1
        output += list(output_sample / sum_of_amplitudes)

        # Next byte
        i += 8

    # Convert list to np array for conversion to .wav
    data_full = np.asarray(output)

    # Save file
    path = os.path.join("Output_files", filename)
    write(path, samplerate, data_full.astype(np.int16))
    print('Saved file ' + path)

    return data_full


# ------------------------------------------------------------------------------

# Define constants
max_amplitude = np.iinfo(np.int16).max
samplerate = 44100

frequency_bands_hz = [
    70,
    200,
    400,
    750,
    1750,
    3250,
    6000,
    15000
]

sum_of_amplitudes = sum([remap_amplitude(x) for x in frequency_bands_hz])
print('Sum of amplitudes: ' + str(sum_of_amplitudes))

max_bytes_per_file = 88
