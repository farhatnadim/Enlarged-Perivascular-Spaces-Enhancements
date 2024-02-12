import itk
import matplotlib.pyplot as plt    
import numpy as np
import seaborn as sns

def plot_histogram_seaborn(image_array, title="Histogram", bins=256):
    # Flatten the array
    flattened_array = image_array.ravel()

    # Create the histogram
    sns.histplot(flattened_array, bins=bins, kde=False, color='blue')
    plt.title(title)
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Load the MRI image
mri_file = '/mnt/d/PhD_Data/MSBRAIN/Converted/MH218/T1w-MP2RAGE-0p55_T1_Images_390x300.16.nii.gz'
mri_image = itk.imread(mri_file, itk.SS)

# Load the pre-resampled mask image (ensure it's in the same space as the MRI image)
mask_file = 'Resliced_combined_whitematter.nii.gz'
mask_image = itk.imread(mask_file, itk.UC)

# Convert images to numpy arrays
mri_array = itk.array_from_image(mri_image)
mask_array = itk.array_from_image(mask_image)

# Apply the mask: Keep only pixels under the mask (mask value should be non-zero)
masked_mri_array = mri_array * (mask_array != 0)

# Convert the masked array back to an ITK image
masked_mri_image = itk.image_from_array(masked_mri_array)
masked_mri_image.CopyInformation(mri_image)

# Write the masked MRI to a new NIfTI file
masked_mri_file = 'masked_mri.nii'
itk.imwrite(masked_mri_image, masked_mri_file)

print(f"Masked MRI saved as {masked_mri_file}")

plot_histogram_seaborn((masked_mri_array), title="Histogram of Masked MRI Image")