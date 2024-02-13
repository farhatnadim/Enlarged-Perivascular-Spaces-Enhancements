'''This code will test 3 vesselness filters on the same image and compare the results'''
import skimage as ski

'''read 3D nifti image'''
import nibabel as nib
#read the image with itk 
import itk
import numpy as np
import matplotlib.pyplot as plt
import os

def load_image(filename : str) -> np.ndarray : 
    '''This function loads a 3D nifti image and returns the image data'''
    # try and catch block to check if the file exists
    try:
        img = itk.imread(filename)
    except FileNotFoundError:
        print("File not found")
        return
    return img, itk.GetArrayFromImage(img)
#after loading the image we can now use the vesselness filter
#First we are going to use the Frangi filter
def vesselnes_filter(image : np.ndarray, filter_type : str, csf : bool ) -> np.ndarray:
    '''This function applies the Frangi filter to a 3D image and returns the filtered image'''
    # apply the Frangi filter to the image
    switcher = {
        "Frangi": ski.filters.frangi(image,black_ridges=csf),
        "Sato": ski.filters.sato(image,black_ridges=csf),
        "Meijering": ski.filters.meijering(image,black_ridges=csf)
    }
    # get the function from switcher dictionary
    vesselness = switcher.get(filter_type, lambda: "Invalid filter")
    # return the filtered image
    return vesselness
filters_type = ["Sato", "Frangi", "Meijering"]
for filter_type in filters_type:
    print(filter_type)
# loads the image using nibabel and get the image data
# TODO: add way to track the tests and the results
# TODO : add argparse 

  
# start the pipeline
# load the image
# pass the image data to the Frangi filter
# save the filtered image with the metadata
    contrasts_list = ['T1w_over_T2w']
    MAIN_PATH = 'D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed'
# load the image
    for contrast in contrasts_list:
        in_filename = MAIN_PATH + os.sep+contrast+'.nii'
        itk_image, np_image = load_image(in_filename)
        #use the Frangi filter
        frangi_img = vesselnes_filter(np_image, filter_type,False )
    #save the filtered image with nibabel keeping the metadata
        out_filename =  MAIN_PATH + os.sep + contrast + filter_type + '.nii'
        out_image = itk.GetImageFromArray(np.ascontiguousarray(frangi_img))

        itk.imwrite(out_image, out_filename)


