import sys

from PIL import Image

path_src = "./images-src/"
path_output = "./images-out/"

path_background = path_src + "background/"
path_skin = path_src + "skin/"
path_body = path_src + "body/"
path_eyes = path_src + "eyes/"
path_head = path_src + "head/"
path_shadows = path_src + "shadows/"

total_images = range(2)  # how many images you want to generate (make sure you have 6 pics for 1 image)

print("Generating {} files. Make sure you have {} files per each category background/skin/body/eyes/head/shadow."
      " (mandatory only background)".format(total_images.stop, total_images.stop))
print("\nIn folder ./background/ should be present files [background_0.png to skin_{}.png]".format(total_images.stop, total_images.stop))
print("In folder ./skin/ should be present files [skin_0.png to skin_{}.png]".format(total_images.stop, total_images.stop))
print("In folder ./body/ should be present files [body_0.png to body_{}.png]".format(total_images.stop, total_images.stop))
print("In folder ./eyes/ should be present files [eyes_0.png to eyes_{}.png]".format(total_images.stop, total_images.stop))
print("In folder ./head/ should be present files [head_0.png to head_{}.png]".format(total_images.stop, total_images.stop))
print("In folder ./shadows/ should be present files [shadows_0.png to shadows_{}.png]\n".format(total_images.stop, total_images.stop))

def method_name(initialFile, additionFile):
    try:
        additionalLayer = Image.open(additionFile, "r")
        initialFile.alpha_composite(additionalLayer)
    except:
        print("First payer is mandatory! {} occurred! {}".format(sys.exc_info()[0], sys.exc_info()[1]))


for n in total_images:
    print("\nGenerating file ", n)
    try:
        bg = Image.open(path_background + "background_{}.png".format(n), "r")
    except:
        print("\n{} occurred! {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        quit()

    method_name(bg, path_background + "background_{}.png".format(n))
    method_name(bg, path_skin + "skin_{}.png".format(n))
    method_name(bg, path_body + "body_{}.png".format(n))
    method_name(bg, path_eyes + "eyes_{}.png".format(n))
    method_name(bg, path_head + "head_{}.png".format(n))
    method_name(bg, path_shadows + "shadows_{}.png".format(n))

    file_output = path_output + "output_{}.png".format(n)
    bg.save(file_output)
    print("Saved output file nr: {}, {}".format(n, file_output))
