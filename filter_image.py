'''this script is used to filter an image using itk and the gradient aniostropic diffusion filter'''
import itk
import os
# load the image
def load_image(filename : str) -> itk.image : 
    '''This function loads a 3D nifti image and returns the image data'''
    # try and catch block to check if the file exists
    try:
        img = itk.imread(filename)
    except FileNotFoundError:
        print("File not found")
        return
    return img, itk.GetArrayFromImage(img)

# filter the image using the gradient aniostropic diffusion filter
def filter_image(image : itk.image, number_of_iterations : int, conductance : float) -> itk.image:
    '''This function applies the gradient aniostropic diffusion filter to a 3D image and returns the filtered image'''
    # apply the gradient aniostropic diffusion filter to the image
    g_filter = itk.GradientAnisotropicDiffusionImageFilter.New(image)
    g_filter.SetNumberOfIterations(number_of_iterations)
    g_filter.SetTimeStep(conductance)
    g_filter.Update()
    # return the filtered image
    return g_filter.GetOutput()

# save the filtered image with the metadata
def save_image(output_image : itk.image, input_image: itk.image, filename : str) -> None:
    '''This function saves a 3D nifti image with the metadata'''
    # save the filtered image with the metadata
    output_image.CopyInformation(input_image)
    itk.imwrite(output_image, filename)
    
# main function
def main():
    # load the image
    root_dir = r'D:\PhD_Data\MSBRAIN\Test_Software\EPC\Processed'
    orig_filename = 'Vesselness.nii'
    #insert g_filter in the filename
    in_filename = os.path.join(root_dir, orig_filename)
    out_filename = os.path.join(root_dir,orig_filename.replace('.nii','g_filter.nii'))
    
    itk_image, np_image = load_image(in_filename)
    # filter the image
    g_filter = filter_image(itk_image, 5, 0.034)
    # save the filtered image with the metadata
    save_image(g_filter, itk_image, out_filename)
    print(f"Filtered image saved as {out_filename}")
    
if __name__ == "__main__":
    main()