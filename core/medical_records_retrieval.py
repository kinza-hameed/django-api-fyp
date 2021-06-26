import cv2
import re
from django.core.mail import message
import pytesseract
import re
from datetime import datetime
import string

def do(p_name):
    information = {"safely_executed": False}
    information = {
        "patName" : p_name,
        # "age" : age,
        "safely_executed" : True,
        'a' : 'aaaaaaaaa',
        'b' : 'bbbbbbbbb'
    }
    return information,message


def CBC_OCR(image, line_items_coordinates):

    information = {"safely_executed": False}
    print(information)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'#calling general OCR

    # get co-ordinates to crop the image
    c = line_items_coordinates[10]# by changing this value we are getting the mark regions
    # print("c",c)
    # cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][0]:c[1][1], c[0][0]:c[1][0]] #making chunks for fasting the computation

    # convert the image to black and white for better OCR
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
    
# pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    # print(text)
    labName=re.findall('The Aga Khan University Hospital, Karachi',text)
    print("lab Name:",labName[0])

    c = line_items_coordinates[9]# by changing this value we are getting the mark regions

# cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

# convert the image to black and white for better OCR

    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
    # print(text)

# re.search: Returns a Match object if there is a match anywhere in the string
    patName=re.search(r':(.*?) Age',text).group(1)
    print("Patient Name:",patName)
    age= re.search(r'Gender : (.*?)Y',text).group(1)
    print("Age of patient:",age)

#re.findall: Returns a list containing all matches
#Check if the string contains either "female" or "male"
    gender=re.findall("Female|Male",text)# this or that finding
    print("Gender:",gender[0])

    date_pattern=re.search(r'Requested on: (.*?) ',text).group(1)
    # print("Date:",date_pattern)
# date format change to mysql format 

    date_pattern = date_pattern.replace('/','-')
    datetimeobject = datetime.strptime(date_pattern,'%d-%m-%Y')
    date = datetimeobject.strftime('%Y-%m-%d')
    # print(newformat)
    print("Date:",date)

    c = line_items_coordinates[8]# by changing this value we are getting the mark regions

# cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    


# convert the image to black and white for better OCR
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 12 -c preserve_interword_spaces=1 '))
    # print(text)

    mystring=text.replace('\n','').replace('\r','')
    # print(mystring)


    TestName=re.findall('COMPLETE BLOOD COUNT',mystring)
    print("Test Name:",TestName[0])

    HAEMOGLOBIN=float(re.search(r']HAEMOGLOBIN(.*?) g/dl',mystring).group(1))
    print('HAEMOGLOBIN:',HAEMOGLOBIN)

    word ='[COMPLETE BLOOD COUNT][HAEMOGLOBIN HAEMATOCRIT]'

    mystring = mystring.replace(word, "")
    print(mystring)
    HAEMATOCRIT=float(re.search(r'HAEMATOCRIT(.*?)%',mystring).group(1))
    print('HAEMATOCRIT:',HAEMATOCRIT)
    
    c = line_items_coordinates[7]# by changing this value we are getting the mark regions

# cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

# convert the image to black and white for better OCR
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 12 -c preserve_interword_spaces=1 '))

    mystring=text.replace('\n','').replace('\r','')

#removing spaces

    mystring=mystring.translate({ord(c): None for c in string.whitespace})

#correcting M.C.V. terminology
    mystring = mystring.replace("M.C.Y." or "M.C.V.", "M.C.V.")

    RBC=float(re.search(r'R.B.C.(.*?)x10E12/L',mystring).group(1))
    print('R.B.C.:',RBC)

    MCV=float(re.search(r'M.C.V.(.*?)f',mystring).group(1))
    print('M.C.V.:',MCV)

    MCH=float(re.search(r'M.C.H.(.*?)pg',mystring).group(1))
    print('M.C.H.:',MCH)

    MCHC=float(re.search(r'M.C.H.C(.*?)g/dL',mystring).group(1))
    print('M.C.H.C:',MCHC)

    RDW=float(re.search(r'R.D.W(.*?)%',mystring).group(1))
    print('R.D.W:',RDW)

    c = line_items_coordinates[6]# by changing this value we are getting the mark regions

# cropping image img = image[y0:y1, x0:x1]
    img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

# convert the image to black and white for better OCR
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)

# pytesseract image to string to get results
    text = str(pytesseract.image_to_string(thresh1, config='--psm 12 '))


#removing line breaks
    mystring=text.replace('\n','').replace('\r','')
#removing spaces

    mystring=mystring.translate({ord(c): None for c in string.whitespace})


    WBC=float(re.search(r'W.B.C.(.*?)x10E9/L',mystring).group(1))
    print('W.B.C.:',WBC)

    NEUTROPHILS=float(re.search(r'NEUTROPHILS(.*?)%',mystring).group(1))
    print('NEUTROPHILS:',NEUTROPHILS)

    LYMPHOCYTES=float(re.search(r'LYMPHOCYTES(.*?)%',mystring).group(1))
    print('LYMPHOCYTES:',LYMPHOCYTES)

    EOSINOPHILS=float(re.search(r'EOSINOPHILS(.*?)%',mystring).group(1))
    print('EOSINOPHILS:',EOSINOPHILS)

    MONOCYTES=float(re.search(r'MONOCYTES(.*?)%',mystring).group(1))
    print('MONOCYTES:',MONOCYTES)

    BASOPHILS=float(re.search(r'BASOPHILS(.*?)%',mystring).group(1))
    print('BASOPHILS:',BASOPHILS)

    PLATELETS=float(re.search(r'PLATELETS(.*?)x10E9/L',mystring).group(1))

    print('PLATELETS:',PLATELETS)


    information = {
        "labName" : labName,
        "patName" : patName,
        "age" : age,
        "gender" : gender[0],
        "date" : date,
        "safely_executed" : True,
        "HAEMOGLOBIN" : HAEMOGLOBIN,
        "HAEMATOCRIT" : HAEMATOCRIT,
        "RBC" : RBC,
        "MCV" : MCV,
        "MCH" : MCH,
        "MCHC" : MCHC,
        "RDW" : RDW,
        "WBC" : WBC,
        "NEUTROPHILS" : NEUTROPHILS,
        "LYMPHOCYTES" : LYMPHOCYTES,
        "EOSINOPHILS" : EOSINOPHILS,
        "MONOCYTES" : MONOCYTES,
        "BASOPHILS" : BASOPHILS,
        "PLATELETS" : PLATELETS
    }
    return information