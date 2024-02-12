function plotMRIHistogram(mriData)
    % Flatten the 3D MRI data to a 1D array
    flattenedData = mriData(:);

    % Plot the histogram
    figure;
    histogram(flattenedData, 'BinWidth', 1); % Adjust 'BinWidth' as needed
    title('Histogram of Masked MRI Image');
    xlabel('Pixel Intensity');
    ylabel('Frequency');
end

