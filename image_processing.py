import sys
from byuimage import Image
def validate_commands(parameters_tuple):
    print(parameters_tuple)
    if parameters_tuple[0] == '-d' and len(parameters_tuple) == 2: 
        file_name = parameters_tuple[1]
        image = Image(file_name)
        return True
    # image_name = image_read(parameters_tuple)
    elif parameters_tuple[0] == '-k' and len(parameters_tuple) == 4:
        image = darken(parameters_tuple)
        image.save(parameters_tuple[2])
         
    elif parameters_tuple[0] == '-s' and len(parameters_tuple) == 3:
         image = sepia(parameters_tuple)
         image.save(parameters_tuple[2])

    elif parameters_tuple[0] == '-g' and len(parameters_tuple) == 3:
        image = gray_scale(parameters_tuple)
        image.save(parameters_tuple[2])

    elif parameters_tuple[0] == '-f' and len(parameters_tuple) == 3:
        image = flipped(parameters_tuple)
        image.save(parameters_tuple[2])

    elif parameters_tuple[0] == '-b' and len(parameters_tuple) == 7:
        image = make_borders(parameters_tuple)
        image.save(parameters_tuple[2])

    elif parameters_tuple[0] == '-m' and len(parameters_tuple) == 3:
        image = mirrored(parameters_tuple)
        image.save(parameters_tuple[2])

    elif parameters_tuple[0] == '-c' and len(parameters_tuple) == 7:
        image = compositing(parameters_tuple)
        image.save(parameters_tuple[5])

    elif parameters_tuple[0] == '-y' and len(parameters_tuple) == 6:
        image = green_screen(parameters_tuple)
        image.save(parameters_tuple[3])
    

    else:
        print("didn't work")
        return False 
    
# def image_read(parameters_tuple):
#      file_name = parameters_tuple[1]
     
#      return file_name

def flipped(parameters_tuple):
    image = Image(parameters_tuple[1])
    image_flipped = Image.blank(image.width, image.height)
    for y in range(0, image.height):
        for x in range(0, image.width):
            pixel = image.get_pixel(x, y)
            y = -y -1
            image_flipped.pixels[x, y] = (pixel.red, pixel.green, pixel.blue)

    return image_flipped
     
    
def darken(parameters_tuple):
     file_name = parameters_tuple[1]
     percent = float(parameters_tuple[3])
     image = Image(file_name)
     for pixel in image:
          pixel.red = pixel.red * (1 - percent)
          pixel.green = pixel.green * (1 -percent)
          pixel.blue = pixel.blue * (1 - percent)
     return image

def sepia(parameters_tuple):
     file_name = parameters_tuple[1]
     image = Image(file_name)
     for pixel in image:
        true_red = 0.393*pixel.red + 0.769*pixel.green + 0.189*pixel.blue
        true_green = 0.349*pixel.red + 0.686*pixel.green + 0.168*pixel.blue
        true_blue = 0.272*pixel.red + 0.534*pixel.green + 0.131*pixel.blue
        pixel.red = true_red
        pixel.green = true_green
        pixel.blue = true_blue
        if pixel.red > 255:
            pixel.red = 255
        if pixel.green > 255:
            pixel.green = 255
        if pixel.blue > 255:
            pixel.blue = 255
        
        
     return image

def make_borders(parameters_tuple):
    image = Image(parameters_tuple[1])
    thickness = int(parameters_tuple[3])
    image_bordered = Image.blank((image.width)+thickness*2, (image.height)+thickness*2)
    for y in range(0, image_bordered.height):
        for x in range(0, image_bordered.width):
            border_pixel = image_bordered.get_pixel(x,y)
            border_pixel.red = parameters_tuple[4]
            border_pixel.green = parameters_tuple[5]
            border_pixel.blue = parameters_tuple[6]
            #image_bordered.get_pixel(x,y) = (border_pixel.red, border_pixel.green, border_pixel.blue)

    for y in range(0, image.height):
        for x in range(0, image.width):
            image_pixel = image.get_pixel(x,y)
            border_pixel = image_bordered.get_pixel(x+thickness, y+thickness)
            border_pixel.red = image_pixel.red
            border_pixel.green = image_pixel.green
            border_pixel.blue = image_pixel.blue
        
    return image_bordered


def gray_scale(parameters_tuple):
     file_name = parameters_tuple[1]
     image = Image(file_name)
     for pixel in image:
          average = (pixel.red + pixel.green + pixel.blue) / 3
          pixel.red = average
          pixel.green = average
          pixel.blue = average
          
     return image 

def mirrored(parameters_tuple):
    image = Image(parameters_tuple[1])
    image_flipped = Image.blank(image.width, image.height)
    for y in range(0, image.height):
        for x in range(0, image.width):
            pixel = image.get_pixel(x, y)
            x = -x -1
            image_flipped.pixels[x, y] = (pixel.red, pixel.green, pixel.blue)

    return image_flipped

def compositing(parameters_tuple):
    image1 = Image(parameters_tuple[1])
    image2 = Image(parameters_tuple[2])
    image3 = Image(parameters_tuple[3])
    image4 = Image(parameters_tuple[4])
    thickness = int(parameters_tuple[6])
    # image = Image.blank(image1.width, image1.height)
    
    image_bordered = Image.blank((image1.width+thickness)*2 + thickness, (image1.height+thickness)*2 + thickness)
    for y in range(0, image_bordered.height):
        for x in range(0, image_bordered.width):
            border_pixel = image_bordered.get_pixel(x,y)
            border_pixel.red = 0
            border_pixel.green = 0
            border_pixel.blue = 0
            #image_bordered.get_pixel(x,y) = (border_pixel.red, border_pixel.green, border_pixel.blue)

    for y in range(0, image1.height):
        for x in range(0, image1.width):
            image_pixel1 = image1.get_pixel(x,y)
            border_pixel = image_bordered.get_pixel(x+thickness, y+thickness) #gets you where you'll put it
            border_pixel.red = image_pixel1.red
            border_pixel.green = image_pixel1.green
            border_pixel.blue = image_pixel1.blue

    for y in range(0, image2.height):
        for x in range(0, image2.width):
            image_pixel2 = image2.get_pixel(x,y)
            border_pixel = image_bordered.get_pixel(x+thickness*2 + image1.width, y+thickness) 
            border_pixel.red = image_pixel2.red
            border_pixel.green = image_pixel2.green
            border_pixel.blue = image_pixel2.blue   
    
    for y in range(0, image3.height):
        for x in range(0, image3.width):
            image_pixel3 = image3.get_pixel(x,y)
            border_pixel = image_bordered.get_pixel(x+thickness, y+thickness*2 + image1.height) 
            border_pixel.red = image_pixel3.red
            border_pixel.green = image_pixel3.green
            border_pixel.blue = image_pixel3.blue   

    for y in range(0, image4.height):
        for x in range(0, image4.width):
            image_pixel4 = image4.get_pixel(x,y)
            border_pixel = image_bordered.get_pixel(x+thickness*2 + image1.width , y+thickness*2 + image1.height) 
            border_pixel.red = image_pixel4.red
            border_pixel.green = image_pixel4.green
            border_pixel.blue = image_pixel4.blue

    return image_bordered 

def detect_green(parameters_tuple, fp):
    factor = float(parameters_tuple[5])
    threshold = int(parameters_tuple[4])
    # for y in range(0, foreground_image.height):
    #     for x in range(0, foreground_image.width):

    average = (fp.red + fp.green + fp.blue) / 3
    if fp.green >= factor * average and fp.green > threshold:
        return True
    else:
        return False
            
def green_screen(parameters_tuple):
    back_image = Image(parameters_tuple[2])
    fore_image = Image(parameters_tuple[1])
    final = Image.blank(back_image.width,back_image.height)
    for y in range(back_image.height):
        for x in range(back_image.width):
            fp = final.get_pixel(x,y)
            bp = back_image.get_pixel(x,y)
            fp.red = bp.red
            fp.green = bp.green
            fp.blue = bp.blue
    for y in range(fore_image.height):
        for x in range(fore_image.width):
            fp = fore_image.get_pixel(x, y)
            print(fp)
            if not detect_green(parameters_tuple, fp):
                np = final.get_pixel(x,y)
                np.red = fp.red
                np.green = fp.green
                np.blue =fp.blue
    return final
    
    

    




    

    

def main(args):
    
    parameters_tuple = args[1:]
    print(f'here are the parameters{parameters_tuple}')
    
    if validate_commands(parameters_tuple):
        print("true")
    else:
        print("false")  

if __name__ == "__main__":
    main(sys.argv)
       
