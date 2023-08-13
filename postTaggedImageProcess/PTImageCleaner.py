import os


def remove_images_without_xml(root_folder):
    total_deleted=0
    for folder_name, subfolders, filenames in os.walk(root_folder):
        print(f"{folder_name}:{len(filenames)}")
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                image_path = os.path.join(folder_name, filename)
                xml_filename = os.path.splitext(filename)[0] + '.xml'
                xml_path = os.path.join(folder_name, xml_filename)

                if not os.path.exists(xml_path):
                    total_deleted+=1
                    os.remove(image_path)
                    print(f"Deleted: {image_path}")
    print(f"total deleted {total_deleted}")


if __name__ == '__main__':
    root_folder = 'D:\\mm\\imagenes\\AAAAAAAAA'  # Change this to the root folder path
    remove_images_without_xml(root_folder)