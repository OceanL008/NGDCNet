import os
import cv2
import numpy as np
from skimage import io
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from vif import compare_vifp

# Specify the path to the folder containing the clean and denoised images
clean_image_folder = ''

denoised_image_folder = ''


# Specify the path to the TXT file used to save the PSNR and SSIM results
result_file_path = ''

# Initialize cumulative variables used to calculate mean PSNR and mean SSIM
total_psnr = 0.0
total_ssim = 0.0

# Get all image files in the Clean Images folder
clean_image_files = os.listdir(clean_image_folder)

# Opening TXT files to write PSNR and SSIM results
with open(result_file_path, 'w') as result_file:
    for clean_image_file in clean_image_files:
        # The complete path to construct a clean image and the corresponding denoised image
        clean_image_path = os.path.join(clean_image_folder, clean_image_file)
        denoised_image_path = os.path.join(denoised_image_folder, clean_image_file.replace('.jpg', '_50.jpg'))
        
        # Read clean and denoised images
        clean_image = cv2.imread(clean_image_path)
        
        denoised_image = cv2.imread(denoised_image_path)

        # Calculating PSNR
        psnr = peak_signal_noise_ratio(clean_image, denoised_image)

        # Calculating SSIM
        clean_image_gray = cv2.cvtColor(clean_image, cv2.COLOR_BGR2GRAY)
        denoised_image_gray = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
        
        ssim = structural_similarity(clean_image_gray, denoised_image_gray, channel_axis=None)
        

        with open(result_file_path, 'a') as result_file:
            result_file.write(f"{clean_image_file}: PSNR = {psnr:.2f} dB, SSIM = {ssim:.4f}\n")

        total_psnr += psnr
        total_ssim += ssim
        

# Calculate average PSNR and average SSIM
average_psnr = total_psnr / len(clean_image_files)
average_ssim = total_ssim / len(clean_image_files)


with open(result_file_path, 'a') as result_file:
    result_file.write(f"\nAverage PSNR = {average_psnr:.2f} dB, Average SSIM = {average_ssim:.4f}\n")

print(f"PSNR and SSIM results have been saved to the {result_file_path}")

