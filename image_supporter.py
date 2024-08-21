from PIL import Image


class ImageFormatter:
    def __init__(self, default_image_type):
        self.default_image_type = default_image_type

    def transform_image(self, image_path):
        with Image.open(image_path) as img:
            print("original image format: ", img.format)
            img_rgb = img.convert('RGB')
            new_image_path = image_path.split(".")[0] + "." + self.default_image_type
            img_rgb.save(new_image_path, format=self.default_image_type)
            print("new image format: ", img_rgb.format)
            print("image transformed to ", new_image_path)
            return new_image_path

    def compact_image(self, image_path, quality):
        with Image.open(image_path) as img:
            img.save(image_path, quality=quality)
            return image_path

