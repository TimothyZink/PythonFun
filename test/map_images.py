import glob
import csv
import shutil

output_folder = 'test/results/'
output_file = 'test/results/labels.csv'

ext = 'txt'

root_path = 'test/'

# get all the files in a directory and subdirecotries
images = glob.glob(f'{root_path}**/*.{ext}', recursive=True)

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Type1'])
    for image in images:
        split_path = image.replace('\\', '/').split('/')
        name = split_path[-1].replace(f'.{ext}', '')
        parent = split_path[-2]
        writer.writerow([name, parent])
        # copy the image
        shutil.copy(image, f'{output_folder}')


