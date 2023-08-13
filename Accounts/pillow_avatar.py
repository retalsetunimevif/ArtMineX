from PIL import Image, ImageDraw

avatar = Image.new(mode='RGB', size=(500, 500), color='grey')
# rectangle = ImageDraw.Draw(avatar)
# rectangle.rectangle(xy=[200, 200, 300, 300], fill='red', outline='black', width=2)
circle = ImageDraw.Draw(avatar)
circle.ellipse(xy=[(150, 100),(350, 300)], fill='black')
circle2 = ImageDraw.Draw(avatar)
circle2.ellipse(xy=[(50, 290),(450, 1050)], fill='black')

avatar.save('avatar.jpg')