import itk
import os
import numpy as np
base_dir = r"D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed"
subject = 'MH429'

Nifti_dir = "Nifti/"
Brain_seg_dir = "Brain_Segmentation/"

# Load the NIfTI segmentation file
segmentation_file = 'Seg_Resliced.nii'
#segementation_file_full_path = os.path.join(base_dir, Brain_seg_dir,subject,segmentation_file)
segmentation_file_full_path = os.path.join(base_dir,segmentation_file)
segmentation_image = itk.imread(segmentation_file_full_path)

# Load the MRI image
#mri_file = 'T1w-MP2RAGE-0p55_T1_Images_390x300.16.nii.gz'
mri_file = 'T1w_over_T2w.nii'

#mri_file_path = os.path.join(base_dir, Nifti_dir,subject,mri_file)
mri_file_path = os.path.join(base_dir,mri_file)
mri_image = itk.imread(mri_file_path)

# Convert segmentation to a numpy array
segmentation_array = itk.array_from_image(segmentation_image)

# Set all labels except 2 and 41 to zero
segmentation_array[(segmentation_array != 2) & (segmentation_array != 41)] = 0

# Set labels 2 and 41 to one
segmentation_array[(segmentation_array == 2) | (segmentation_array == 41)] = 1

# Convert the numpy array back to an ITK image, preserving the original metadata
combined_segmentation_image = itk.image_from_array(segmentation_array.astype(np.uint8))
combined_segmentation_image.CopyInformation(segmentation_image)

# Mask the MRI image with the combined segmentation
mri_array = itk.array_from_image(mri_image)
#mri_array[segmentation_array == 0] = 0
#mri_array[segmentation_array == 1] = mri_array[segmentation_array == 1]**2
mri_array = mri_array * segmentation_array
# Convert the masked MRI array back to an ITK image, preserving the original metadata
masked_mri_image = itk.image_from_array(mri_array.astype(np.float32)) 
masked_mri_image.CopyInformation(mri_image)

# Write the combined segmentation to a new NIfTI file

combined_segmentation_file = 'combined_cerebral_white_matter_mask.nii'
#combined_segmentation_file_path = os.path.join(base_dir, Brain_seg_dir,subject,combined_segmentation_file)
combined_segmentation_file_path = os.path.join(base_dir,combined_segmentation_file)
itk.imwrite(combined_segmentation_image, combined_segmentation_file_path, True)

# Write the masked MRI to a new NIfTI file

masked_mri_file = 'white_matter_both_hemispheres.nii'
masked_mri_file_path = os.path.join(base_dir, Nifti_dir,subject,masked_mri_file)
masked_mri_file_path = os.path.join(base_dir,masked_mri_file)
itk.imwrite(masked_mri_image, masked_mri_file_path, True)

print(f"Combined segmentation saved as {combined_segmentation_file_path}")
print(f"Masked MRI saved as {masked_mri_file_path}")
