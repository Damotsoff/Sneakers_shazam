from PIL import Image


def crop_image(input_image, coords, cropped_image):
    x, y, w, h = coords
    croped_sneaker = Image.open(input_image)
    croped_sneaker = croped_sneaker.crop((x, y, x + w, y + h))
    resized_image = croped_sneaker.resize((224, 224))
    resized_image.save(cropped_image)

def get_data(path_to_result_file):
    name = []
    coords = []
    result_dict = {}
    with open(path_to_result_file) as f:
        lines = f.read().split('\n')
        lines = [i for i in list(filter(None, lines)) if not i.strip().startswith('Detection')]
        for line, text in enumerate(lines):
            if 'jpg' in text:
                name.append(text.split(':')[0])
            elif text.startswith('sneaker'):
                coord_line = text.split('(')[1].strip().replace(')', '')
                coords.append(coord_line)
            out = [l.split() for l in coords[:1]]
            int_coords = [tuple(int(x) for x in out[i] if x.isnumeric()) for i in range(len(out))]
        result_dict.update({name[0]: int_coords})
    return result_dict
