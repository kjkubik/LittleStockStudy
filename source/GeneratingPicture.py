import random
import uuid
import numpy
from PIL import Image, ImageDraw 
import time

#output_image = uuid.uuid1()
# image
output_image = Image.open("./resources/outputPicture.png")
print(f'Processing output_image: {output_image}')

image = Image.new('RGB', (5000, 2000))
width, height = image.size
    
rectangle_width = 50
rectangle_height = 50

number_of_squares = random.randint(10,500)

draw_image = ImageDraw.Draw(image)

for i in range(number_of_squares):
    rectangle_x = random.randint(0,width)
    rectangle_y = random.randint(0,height)
    
    rectangle_shape = [(rectangle_x, rectangle_y),(rectangle_x + rectangle_width, rectangle_y + rectangle_height)]
    
    draw_image.rectangle(rectangle_shape, fill = (random.randint(100,255), random.randint(100,255), random.randint(100,255)))
    
    #time.sleep(10)
    
#image.save(f'./resources/{output_image}.png')
#image.save(f'./resources/{output_image}.ppm')    
print(output_image.format, output_image.size, output_image.mode)    

output_image.show()