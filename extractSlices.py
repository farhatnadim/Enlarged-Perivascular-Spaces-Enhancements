import itk
import argparse


def extract_slice(image, slice_number):
    """
    Extracts a specified slice from a 3D image.
    """
    extract_filter = itk.ExtractImageFilter.New(image)
    extract_filter.SetDirectionCollapseToSubmatrix()

    # Set up the extraction region [one slice]
    input_region = image.GetBufferedRegion()
    size = input_region.GetSize()
    size[2] = 1  # Extract along z direction
    start = input_region.GetIndex()
    start[2] = slice_number
    desired_region = input_region
    desired_region.SetSize(size)
    desired_region.SetIndex(start)

    extract_filter.SetExtractionRegion(desired_region)
    extract_filter.Update()  # Update the filter to get the output

    return extract_filter.GetOutput()


def apply_median_filter(image, radius):
    """
    Applies a median filter to a 2D image.
    """
    median_filter = itk.MedianImageFilter.New(image)
    index_radius = image.GetBufferedRegion().GetSize()
    index_radius[0] = radius  # Radius along x
    index_radius[1] = radius  # Radius along y
    index_radius[2] = 0  # Radius along z (not applicable for 2D)
    median_filter.SetRadius(index_radius)
    median_filter.UpdateLargestPossibleRegion()

    return median_filter.GetOutput()


def main():
    parser = argparse.ArgumentParser(description="Process A 2D Slice Of A 3D Image.")
    parser.add_argument("input_3D_image")
    parser.add_argument("output_2D_image")
    parser.add_argument("slice_number", type=int)
    args = parser.parse_args()

    Dimension = 3
    PixelType = itk.ctype("long")
    ImageType = itk.Image[PixelType, Dimension]

    reader = itk.ImageFileReader[ImageType].New()
    reader.SetFileName(args.input_3D_image)
    reader.Update()
    input_image = reader.GetOutput()

    # You can adjust the filter radius here
    filter_radius = 1

    # Extract and filter separately
    extracted_slice = extract_slice(input_image, args.slice_number)
    filtered_slice = apply_median_filter(extracted_slice, filter_radius)

    paste_filter = itk.PasteImageFilter.New(input_image)
    paste_filter.SetSourceImage(filtered_slice)
    paste_filter.SetDestinationImage(input_image)
    paste_filter.SetDestinationIndex(filtered_slice.GetBufferedRegion().GetIndex())

    itk.imwrite(paste_filter.GetOutput(), args.output_3D_image)


if __name__ == "__main__":
    main()