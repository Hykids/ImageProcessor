from PIL import Image
import os


class ImageProcessor:
    def __init__(self, input_dir="image", output_dir="output"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def convert_image(self, infile, output_format="jpg"):
        """
        Convert the image to the specified format.
        """
        f, e = os.path.splitext(infile)
        outfile = os.path.join(self.output_dir, f + "." + output_format)
        if infile != outfile:
            try:
                with Image.open(os.path.join(self.input_dir, infile)) as im:
                    if im.mode == 'RGBA':
                        # 创建一个白色背景的RGB图像
                        background = Image.new("RGB", im.size, (255, 255, 255))
                        background.paste(im, mask=im.split()[3])  # 使用Alpha通道作为掩码
                        im = background
                    im.save(outfile)
                print(f"Converted {infile} to {outfile}")
            except OSError as e:
                print(f"Cannot convert {infile}: {e}")

    def compress_image(self, infile, output_format="jpg", quality=85, resize_factor=1):
        """
        Compress the image by adjusting the quality and optionally resizing.
        """
        f, e = os.path.splitext(infile)
        outfile = os.path.join(self.output_dir, f + "." + output_format)
        try:
            with Image.open(os.path.join(self.input_dir, infile)) as im:
                if resize_factor < 1:
                    new_size = (int(im.width * resize_factor), int(im.height * resize_factor))
                    im = im.resize(new_size)

                if im.mode == 'RGBA':
                    # 创建一个白色背景的RGB图像
                    background = Image.new("RGB", im.size, (255, 255, 255))
                    background.paste(im, mask=im.split()[3])  # 使用Alpha通道作为掩码
                    im = background

                im.save(outfile, output_format.upper(), quality=quality)
                print(f"Compressed {infile} to {outfile} with quality={quality} and resize_factor={resize_factor}")
        except OSError as e:
            print(f"Cannot compress {infile}: {e}")

    def process_all_images(self, output_format="jpg", quality=85, resize_factor=1):
        """
        Process all images in the input directory: convert and compress.
        """
        infiles = os.listdir(self.input_dir)
        for infile in infiles:
            self.convert_image(infile, output_format)
            self.compress_image(infile, output_format, quality, resize_factor)


# Example usage
if __name__ == '__main__':
    processor = ImageProcessor(input_dir="image", output_dir="output")

    # Convert and compress all images
    processor.process_all_images(output_format="jpg", quality=75, resize_factor=0.5)