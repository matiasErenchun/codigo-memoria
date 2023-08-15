import os
import random
import shutil


def split_images(root_folder, test_folder, train_folder, split_ratio=0.2):
    for folder_name, subfolders, filenames in os.walk(root_folder):
        image_files = [filename for filename in filenames if filename.lower().endswith('.jpg')]

        if len(image_files) >= 4:
            num_test_images = int(len(image_files) * split_ratio)
            test_images = random.sample(image_files, num_test_images)
            train_images = [filename for filename in image_files if filename not in test_images]
        else:
            test_images = []
            train_images = image_files

        for filename in test_images:
            image_path = os.path.join(folder_name, filename)
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            xml_path = os.path.join(folder_name, xml_filename)
            test_image_path = os.path.join(test_folder, filename)
            test_xml_path = os.path.join(test_folder, xml_filename)

            shutil.copy(image_path, test_image_path)
            shutil.copy(xml_path, test_xml_path)
            print(f"Copied to test: {filename}")

        for filename in train_images:
            image_path = os.path.join(folder_name, filename)
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            xml_path = os.path.join(folder_name, xml_filename)
            train_image_path = os.path.join(train_folder, filename)
            train_xml_path = os.path.join(train_folder, xml_filename)

            shutil.copy(image_path, train_image_path)
            shutil.copy(xml_path, train_xml_path)
            print(f"Copied to train: {filename}")


if __name__ == '__main__':
    root_folder = 'D:\\mm\\imagenes\\AAAAAAAAA'  # Change this to the root images folder path
    test_folder = 'D:\\mm\\imagenes\\test'  # Change this to the test folder path
    train_folder = 'D:\\mm\\imagenes\\train'  # Change this to the train folder path

    split_images(root_folder, test_folder, train_folder)