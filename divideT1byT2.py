'''this script is used to divide T1 by T2 to get the T1/T2 ratio image'''
'''reads images using itk transforms them to numpy arrays and divides them'''
''''saves the result as a nifti image'''
import itk
import numpy as np
import os
# load the images
# load the fixed image
fixed_image = itk.imread('D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T1w_resampled.nii')
#load the moving image
moving_image = itk.imread('D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T2w_reg.nii')
# convert the images to numpy arrays

fixed_image_np = itk.array_from_image(fixed_image)
moving_image_np = itk.array_from_image(moving_image)
# divide the images
fixed_image_np = fixed_image_np/moving_image_np
# 0,1,2
# 0,2,1
# 1,0,2
# 1,2,0
# 2,0,1
# 2,1,0
fixed_image = itk.GetImageFromArray(np.ascontiguousarray(fixed_image_np))
fixed_image.SetOrigin(moving_image.GetOrigin())
fixed_image.SetSpacing(moving_image.GetSpacing())
fixed_image.SetDirection(moving_image.GetDirection())

# save the result
out_filename = 'D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T1w_over_T2w.nii'

#save the result with the metadata
itk.imwrite(fixed_image, out_filename)
