import numpy as np
import matplotlib.pyplot as plt
import random
from tqdm import tqdm
import argparse

def convert_units(value, unit):
    if unit == 'm':
        return value
    elif unit == 'cm':
        return value / 100
    elif unit == 'mm':
        return value / 1000
    elif unit == 'um':
        return value / 1e6
    elif unit == 'nm':
        return value / 1e9
    else:
        raise ValueError(f"Unknown unit: {unit}")

def generate_fresnel_zone_plate(wavelength, focal_length, num_rings):
    
    # Calculate the radius of each ring
    radii = [np.sqrt(n * wavelength * focal_length + (n ** 2) * (wavelength ** 2) / 4) for n in range(1, num_rings + 1)]
    
    # Calculate the minimum ring thickness
    min_ring_thickness = min(np.diff(radii))
    min_ring_thickness_px = 8  # Minimum ring thickness in pixels
    image_size = int((min_ring_thickness_px / min_ring_thickness) * radii[-1] * 2)
    
    # Normalize radii to the image size
    radii = np.array(radii)
    radii = (radii / radii[-1]) * (image_size // 2)

    # Create the zone plate image
    image = np.zeros((image_size, image_size))
    center = image_size // 2
    
    # Generate the zone plate using vectorized operations
    y, x = np.ogrid[:image_size, :image_size]
    distance = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    
    for k in tqdm(range(num_rings), desc="Generating Fresnel Zone Plate"):
        if k % 2 == 1:
            image[(distance >= radii[k-1]) & (distance < radii[k])] = 1

    # Set the border color to black
    image[:, [0, -1]] = 0
    image[[0, -1], :] = 0

    return image

def generate_photon_sieve(wavelength, focal_length, num_rings, random_spacing=False):
    
    # Calculate the radius of each ring
    radii = [np.sqrt(n * wavelength * focal_length + (n ** 2) * (wavelength ** 2) / 4) for n in range(1, num_rings + 1)]
    
    # Calculate the minimum ring thickness
    min_ring_thickness = min(np.diff(radii))
    min_ring_thickness_px = 8  # Minimum ring thickness in pixels
    image_size = int((min_ring_thickness_px / min_ring_thickness) * radii[-1] * 2)
    
    # Normalize radii to the image size
    radii = np.array(radii)
    radii = (radii / radii[-1]) * (image_size // 2)

    # Create the photon sieve image
    image = np.zeros((image_size, image_size))
    center = image_size // 2
    
    # Fill the center circle (first ring) with solid black
    radius_inner = 0
    radius_outer = radii[0]
    y, x = np.ogrid[-center:image_size-center, -center:image_size-center]
    mask = x**2 + y**2 <= radius_outer**2
    image[mask] = 0

    # Generate dots within each black ring (odd-indexed rings) starting from the second ring
    for k in tqdm(range(1, num_rings, 2), desc="Generating Photon Sieve"):  # Only use odd rings (dark regions)
        radius_inner = radii[k-1]
        radius_outer = radii[k]
        ring_thickness = radius_outer - radius_inner
        
        # Adjust dot density based on the radius
        dot_radius = max(int(ring_thickness / 2), min_ring_thickness_px // 2)
        dot_spacing_min = dot_radius * 3.0
        dot_spacing_max = dot_radius * 4.0
        dot_spacing_min_rand = dot_radius * 1.1
        dot_spacing_max_rand = dot_radius * 4.0
        circumference = 2 * np.pi * radius_outer
        if random_spacing:
            num_dots = max(1, int(circumference / ((dot_spacing_min_rand + dot_spacing_max_rand) * random.uniform(1.3, 1.5))))
        else:
            num_dots = max(1, int(circumference / ((dot_spacing_min + dot_spacing_max) / 2)))
        angles = np.linspace(0, 2 * np.pi, num_dots, endpoint=False)

        for angle in angles:
            if random_spacing:
                random_angle = angle + random.uniform(0, np.pi/num_dots)
                while True:
                    x = center + int((radius_inner + ring_thickness / 2) * np.cos(random_angle))
                    y = center + int((radius_inner + ring_thickness / 2) * np.sin(random_angle))
                    if 0 <= x < image_size and 0 <= y < image_size and image[y, x] == 0:
                        break
                    random_angle += random.uniform(0, np.pi/num_dots)
                rr, cc = np.ogrid[-dot_radius:dot_radius, -dot_radius:dot_radius]
                mask = rr**2 + cc**2 <= dot_radius**2
                y_min, y_max = max(0, y-dot_radius), min(image_size, y+dot_radius)
                x_min, x_max = max(0, x-dot_radius), min(image_size, x+dot_radius)
                image_slice = image[y_min:y_max, x_min:x_max]
                mask = mask[:image_slice.shape[0], :image_slice.shape[1]]
                image_slice[mask] = 1  # Place thick dot
            else:
                random_angle = angle
            x = center + int((radius_inner + ring_thickness / 2) * np.cos(random_angle))
            y = center + int((radius_inner + ring_thickness / 2) * np.sin(random_angle))
            if 0 <= x < image_size and 0 <= y < image_size:
                rr, cc = np.ogrid[-dot_radius:dot_radius, -dot_radius:dot_radius]
                mask = rr**2 + cc**2 <= dot_radius**2
                y_min, y_max = max(0, y-dot_radius), min(image_size, y+dot_radius)
                x_min, x_max = max(0, x-dot_radius), min(image_size, x+dot_radius)
                image_slice = image[y_min:y_max, x_min:x_max]
                mask = mask[:image_slice.shape[0], :image_slice.shape[1]]
                image_slice[mask] = 1  # Place thick dot

    # Set the border color to black
    image[:, [0, -1]] = 0
    image[[0, -1], :] = 0

    return image

def main():
    parser = argparse.ArgumentParser(description="Generate Fresnel Zone Plate and Photon Sieve image masks for a given wavelength, focal length and number of rings")
    parser.add_argument('-w', '--wavelength', type=float, required=True, help="Wavelength value")
    parser.add_argument('-wu', '--wavelength_unit', choices=['m', 'cm', 'mm', 'um', 'nm'], required=True, help="Wavelength unit")
    parser.add_argument('-f', '--focal_length', type=float, required=True, help="Focal length value")
    parser.add_argument('-fu', '--focal_length_unit', choices=['m', 'cm', 'mm', 'um', 'nm'], required=True, help="Focal length unit")
    parser.add_argument('-n', '--num_rings', type=int, required=True, help="Number of rings to generate (min 2). Values between 10 and 1000 are recommended")
    parser.add_argument('-g', '--generate', type=str, required=True, help="What to generate (f: Fresnel, p: photon-sieve, r: random photon-sieve). [Ex: -g fp to generate both Fresnel and photon-sieve]")
    parser.add_argument('-d', '--display', action='store_true', help="Display the generated images in a single plot using matplotlib")
    parser.add_argument('-s', '--save', action='store_true', help="Save the generated images as PNG files in the current directory")

    args = parser.parse_args()

    if not args.display and not args.save:
        print("Warning: Output is neither displayed nor saved.")

    wavelength = convert_units(args.wavelength, args.wavelength_unit)
    focal_length = convert_units(args.focal_length, args.focal_length_unit)
    num_rings = args.num_rings

    if num_rings <= 1:
        raise ValueError("Number of rings must be at least 1")

    images = {}

    if 'f' in args.generate:
        images['fresnel_zone_plate'] = generate_fresnel_zone_plate(wavelength, focal_length, num_rings)
    if 'p' in args.generate:
        images['photon_sieve'] = generate_photon_sieve(wavelength, focal_length, num_rings)
    if 'r' in args.generate:
        images['random_photon_sieve'] = generate_photon_sieve(wavelength, focal_length, num_rings, random_spacing=True)

    if args.display or args.save:
        plt.figure(figsize=(18, 6))
        for i, (title, image) in enumerate(images.items(), 1):
            plt.subplot(1, len(images), i)
            plt.imshow(image, cmap='gray')
            plt.title(title.replace('_', ' ').title())
            plt.axis('off')
            if args.save:
                filename = f"f{args.focal_length}{args.focal_length_unit}_w{args.wavelength}{args.wavelength_unit}_n{args.num_rings}"
                print(f"Saving {title} as '{title}_{filename}.png'")
                plt.imsave(f'{title}_{filename}.png', image, cmap='gray')
        if args.display:
            plt.show()

    # Calculate the diameter of the outer-most ring
    def format_diameter(diameter_m):
        if diameter_m >= 1:
            return f"{diameter_m:.2f}m"
        elif diameter_m >= 1e-2:
            return f"{diameter_m * 1e2:.2f}cm"
        elif diameter_m >= 1e-3:
            return f"{diameter_m * 1e3:.2f}mm"
        elif diameter_m >= 1e-6:
            return f"{diameter_m * 1e6:.2f}µm"
        elif diameter_m >= 1e-9:
            return f"{diameter_m * 1e9:.2f}nm"
        else:
            return f"{diameter_m * 1e12:.2f}pm"
        
    outer_ring_diameter = np.sqrt(num_rings * wavelength * focal_length + (num_rings ** 2) * (wavelength ** 2) / 4) * 2

    print(f"Lens diameter {format_diameter(outer_ring_diameter)}")

if __name__ == "__main__":
    main()