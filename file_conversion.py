import os
import tempfile
from pdf2image import convert_from_path
import img2pdf
from PIL import Image
import os


import shutil


def convert_pdf(file_path, output_path, dpi):
    temp_dir = tempfile.mkdtemp()

    try:
        images = convert_from_path(file_path, dpi, output_folder=temp_dir)

        # save images to temporary directory
        temp_images = []
        for i in range(len(images)):
            image_path = f"{temp_dir}/{i}.png"
            images[i].save(image_path, "PNG")
            temp_images.append(image_path)

        imgs = list(map(Image.open, temp_images))

        min_img_width = min(i.width for i in imgs)

        total_height = 0
        for i, img in enumerate(imgs):
            total_height += imgs[i].height

        merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))

        y = 0
        for img in imgs:
            merged_image.paste(img, (0, y))
            y += img.height

        merged_image.save(output_path)

        for img in imgs:
            img.close()
            if img.fp:
                img.fp.close()

    finally:
        shutil.rmtree(temp_dir)

    return output_path


def export_to_pdf(input_filepath):

    img_filepath = input_filepath + ".png"
    image = Image.open(img_filepath)
    output_path = input_filepath + ".pdf"
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(output_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    if os.path.exists(img_filepath):
        os.remove(img_filepath)

    print("Successfully created pdf")
