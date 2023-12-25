from PIL import Image, ImageFont, ImageDraw

font = ImageFont.load_default()


message = "epic text"
with Image.open("img/watermark.png") as img:
    width, height = img.size

    txt = Image.new("RGB", img.size,(255,255,255))

    fnt = ImageFont.truetype("arial.ttf", 60)
    #nordic.ttf

    d = ImageDraw.Draw(txt)

    _,_,w,h = d.textbbox((0,0), message, font=fnt)

    d.text(((width-w)/2, (height-h)/2), message,font= fnt,fill=(255, 255, 255))

    out = Image.alpha_composite(base, txt)
    out.save("WatermarkedImage")
    out.show
#"VideoMaker/Screenshot_2.png"