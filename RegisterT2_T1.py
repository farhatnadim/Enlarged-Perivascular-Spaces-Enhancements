'''this code reigsters the T2w image to the T1w image'''
import os
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

# load the images
# load the fixed image
fixed_image = sitk.ReadImage(('D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T1w.nii'),sitk.sitkFloat32)
#load the moving image
moving_image = sitk.ReadImage('D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T2w.nii',sitk.sitkFloat32)
# initial transform

initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, sitk.Euler3DTransform(), sitk.CenteredTransformInitializerFilter.GEOMETRY)
# set the registration method
registration_method = sitk.ImageRegistrationMethod()
# set the similarity metric
registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.01)
# set the bicubic interpolator
registration_method.SetInterpolator(sitk.sitkBSpline)
# set the optimizer 
registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
registration_method.SetOptimizerScalesFromPhysicalShift()

#setup for multi-resolution
registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
# Set the initial moving and optimized transforms.
optimized_transform = sitk.Euler3DTransform()    
registration_method.SetMovingInitialTransform(initial_transform)
registration_method.SetInitialTransform(optimized_transform, inPlace=False)
final_transform_v4 = registration_method.Execute(fixed_image, moving_image)
# apply the transformation
resampler = sitk.ResampleImageFilter()
resampler.SetReferenceImage(fixed_image)
resampler.SetInterpolator(sitk.sitkBSpline)
resampler.SetDefaultPixelValue(0)
resampler.SetTransform(final_transform_v4)
out = resampler.Execute(moving_image)
# save the registered image
sitk.WriteImage(out, 'D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\T2w_reg.nii')