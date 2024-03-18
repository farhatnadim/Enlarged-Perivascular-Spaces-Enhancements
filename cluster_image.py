# use spectral clusertering to further segment the vesselness 3D image
# and save the result with the same metadata as the original image

from sklearn.cluster import SpectralClustering
import numpy as np
import os
import itk
import matplotlib.pyplot as plt

# load the image the image using the itk library 
def load_image(filename : str) -> np.ndarray : 
    '''This function loads a 3D nifti image and returns the image data'''
    # try and catch block to check if the file exists
    try:
        img = itk.imread(filename)
    except FileNotFoundError:
        print("File not found")
        return
    return img, itk.GetArrayFromImage(img)

# use spectral clusertering to segment the vesselness 3D image

_, X = load_image('D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\white_matter_both_hemispheresSatonormal_meanp5.nii')
print(X.shape)
#linearize the image
x = X.reshape(-1,1)
print(x.shape)
# perform spectral cluserting 2D image 
spectral = SpectralClustering(n_clusters=3,n_jobs=12,affinity='nearest_neighbors', random_state=0, assign_labels='discretize')
spectral.fit(x)
# plot the result
#plt.figure(figsize=(10, 5))
##plt.subplot(121)
#plt.title('Spectral Clustering')
print(spectral.labels_.shape)
# reshape the labels to the original image shape
labels = spectral.labels_.reshape(X.shape)
# save the results as itk image
label_img = itk.GetImageFromArray(labels)
label_img.SetOrigin(_.GetOrigin())
label_img.SetSpacing(_.GetSpacing())
label_img.SetDirection(_.GetDirection())
# save the result with the metadata
itk.imwrite(label_img,'D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed\white_matter_both_hemispheresSatonormal_meanp5_seg.nii')