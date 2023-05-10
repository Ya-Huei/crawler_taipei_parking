import requests
import shutil
import ddddocr

def downloadValidateCode(rs, headers):
    r = rs.get('https://parkingfee.pma.gov.taipei/Home/GraphicsVerification',
               verify=False, stream=True, headers=headers)
    if r.status_code == 200:
        with open('code.png', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def getValidateCode():
    ocr = ddddocr.DdddOcr()
    with open('code.png', 'rb') as f:
        img_bytes = f.read()
    return ocr.classification(img_bytes)
