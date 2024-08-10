# Fresnelier

## Overview

Fresnelier is a CLI Python script designed to generate image masks for **Fresnel Zone Plates** and **Photon Sieves**

### What is a Fresnel Zone Plate?

A **Fresnel Zone Plate** (FZP) is a diffractive optical element that focuses light through constructive interference at specific focal points. Unlike traditional lenses, which rely on refraction, FZPs use a series of concentric rings that alternate between transparent and opaque regions, creating zones that cause light to converge.

### What is a Photon Sieve?

A **Photon Sieve** is an advanced variation of the Fresnel Zone Plate. Instead of using continuous rings, the Photon Sieve has a series of holes positioned at specific locations similar to a FZP. This design can achieve higher resolution and better control over the focal properties compared to traditional zone plates, but allows lesser light to pass through compared to a FZP.

## Features

- Create high-resolution images of Fresnel Zone Plates for given parameters like wavelength, focal length, and the number of rings.
- Create Photon Sieves based on the same parameters, with an option to randomize the placement of 'sieves'.
- Display the generated patterns directly (matplotlib) or save them as PNG files for further use.
- Dynamic output image scaling (automatic)
- Automatically compute the diameter of the outermost ring for the generated pattern.

## Dependencies

This script relies on the following Python libraries:

- `numpy`: For numerical computations.
- `matplotlib`: For image visualization and saving.
- `random`: For generating random patterns in the Photon Sieve.
- `tqdm`: For displaying a progress bar during pattern generation.
- `argparse`: For command-line argument parsing.

You can install the required dependencies using pip:

```bash
pip install numpy matplotlib tqdm
```

## Usage

### Command-Line Arguments

```bash
python fresnelier.py -w [wavelength] -wu [unit] -f [focal length] -fu [unit] -n [num. of rings] -g [generation options] (optional ->) -d [display] -s [save]
```

- `-w` or `--wavelength`: Wavelength value (required).
- `-wu` or `--wavelength_unit`: Unit for wavelength (`m`, `cm`, `mm`, `um`, `nm`) (required).
- `-f` or `--focal_length`: Focal length value (required).
- `-fu` or `--focal_length_unit`: Unit for focal length (`m`, `cm`, `mm`, `um`, `nm`) (required).
- `-n` or `--num_rings`: Number of rings to generate (required).
- `-g` or `--generate`: What to generate: `f` for Fresnel, `p` for Photon Sieve, `r` for Random Photon Sieve. You can combine these (e.g., `fp` to generate both Fresnel and Photon Sieve).
- `-d` or `--display`: Display the generated images in a plot (optional).
- `-s` or `--save`: Save the generated images as PNG files (optional).

### Example

To generate both Fresnel Zone Plate and Photon Sieve patterns for a 980nm wavelength, 1mm focal length, and 100 rings, and display and save the results:

```bash
python fresnelier.py -w 980 -wu nm -f 1 -fu mm -n 100 -g fp -d -s
```

#### Output

##### Terminal
```bash
Generating Fresnel Zone Plate: 100%|████████████████████████████████████████████████| 100/100 [00:00<00:00, 165.24it/s]
Generating Photon Sieve: 100%|████████████████████████████████████████████████████████| 50/50 [00:00<00:00, 197.44it/s]
Saving fresnel_zone_plate as 'fresnel_zone_plate_f1.0mm_w980.0nm_n100.png'
Saving photon_sieve as 'photon_sieve_f1.0mm_w980.0nm_n100.png'
```
##### Display
![image](https://github.com/user-attachments/assets/302a306b-ed83-437c-aca9-34f2c6e1b7db)

##### Files
- fresnel_zone_plate_f1.0mm_w980.0nm_n100.png (443 KB)
- photon_sieve_f1.0mm_w980.0nm_n100.png (462 KB)


## Future Improvements

- Support for custom image scaling options
- Support for more randomization options (currently a fixed algorithm)
- Option to generate inverted mask/ custom colored mask
- Support for phased FZP generation (phase controlled by RGB values of the pixels)
