import numpy as np
from scipy.io.wavfile import write
import random
import os.path
import matplotlib.pyplot as plt
from data_to_wav_encoder import *
from functions_image import *

"""
Encode image into a one-channel**greyscale) .wav file for import into Dreams for PS4/PS5 via the audio importer
bandwidth is limited by the decoder's slow refresh rate but it works as a proof of concept!

TODO: at the moment encodes the whole image into one file, 
      split larger images into multiple files to get around dreams' 60s audio clip max length  
"""

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Test - Random input data
# num_bytes = 89
# input_data = generate_random_input_data_8bit(num_bytes)
#
# sample_length_frames = [10]
#
# for sample_length in sample_length_frames:
#     output_data = create_wav_file(data=input_data,
#                                   filename=str(samplerate) + '_' + str(sample_length) + '_frames_per_byte.wav',
#                                   sample_length_seconds=sample_length/30,
#                                   samplerate=samplerate)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Image to 8bit data

# image_filename = 'Planets_32px.jpg'
image_filename = 'diagonal_gradient_9px.jpg'
image = Image.open(os.path.join('Images', image_filename)).convert('L')
image_data_8bit = encode_greyscale_image_to_8bit(image)

bits_written = 0
part = 1
while bits_written < len(image_data_8bit):
    # Create one .wav up to size max_bytes_per_file
    slice_start = bits_written
    slice_end = slice_start + (max_bytes_per_file * 8)
    data_slice = image_data_8bit[slice_start:slice_end]

    output_filename = str(part) + '_' + image_filename.split('.')[0] + '.wav'

    output_data = create_wav_file(data=data_slice,
                                  filename=output_filename,
                                  sample_length_seconds=10/30,
                                  samplerate=samplerate
                                  )

    bits_written += len(data_slice)
    part += 1
