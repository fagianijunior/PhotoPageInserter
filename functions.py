import os
import cv2

models_dir = "./models/"
output_dir = "./output/"
image_width = 712
image_weight = 595

def crop_and_resize(img, w, h):
        im_h, im_w = img.shape[:2]
        res_aspect_ratio = w/h
        input_aspect_ratio = im_w/im_h

        if input_aspect_ratio > res_aspect_ratio:
            im_w_r = int(input_aspect_ratio*h)
            im_h_r = h
            img = cv2.resize(img, (im_w_r , im_h_r))
            x1 = int((im_w_r - w)/2)
            x2 = x1 + w
            img = img[:, x1:x2, :]
        if input_aspect_ratio < res_aspect_ratio:
            im_w_r = w
            im_h_r = int(w/input_aspect_ratio)
            img = cv2.resize(img, (im_w_r , im_h_r))
            y1 = int((im_h_r - h)/2)
            y2 = y1 + h
            img = img[y1:y2, :, :]
        if input_aspect_ratio == res_aspect_ratio:
            img = cv2.resize(img, (w, h))

        return img

def generate_calendar(model, photos_dir, same_photo=False):
    pic_idx = 0
    images = [cv2.imread(os.path.join(photos_dir, photo_name)) for photo_name in sorted(os.listdir(photos_dir))]

    for page_idx, page in enumerate(model.pages):
        page_image = cv2.imread(os.path.join("models", model.name, page['filename']))
        
        for picture in page['pictures']:
            picture_image = images[pic_idx]
            
            # Converte as pictures de origem no formato 6x5
            picture_cropped = crop_and_resize(picture_image, picture['size']['width'], picture['size']['height'])

            x = picture['possition']['x']
            y = picture['possition']['y']

            if picture['rotate'] == 180:
                picture_cropped = cv2.rotate(picture_cropped, cv2.ROTATE_180)

            page_image[y:y + picture['size']['height'], x:x + picture['size']['width']] = picture_cropped
            
            if same_photo == False:
                pic_idx = pic_idx + 1

        cv2.imwrite(os.path.join(output_dir, "page_" + str(page_idx) + ".png"), page_image)
    pic_idx = 0