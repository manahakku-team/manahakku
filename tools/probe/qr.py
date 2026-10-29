import qrcode
for name,url in [('qr-web','https://manahakku-team.github.io/manahakku/'),('qr-apk','https://github.com/manahakku-team/manahakku/releases/latest')]:
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=24,border=2);q.add_data(url);q.make(fit=True)
    q.make_image(fill_color=(23,32,90),back_color=(255,255,255)).save('out/'+name+'.png')
print('done')
