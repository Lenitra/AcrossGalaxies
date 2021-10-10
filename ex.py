from captcha.image import _Captcha, ImageCaptcha

image = ImageCaptcha(width=280, height=90)

capt_text = "Something"
data = image.generate(capt_text)

image.write(capt_text, "static/imgs/CAPTCHA.png")