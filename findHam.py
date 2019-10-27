def findHam():
    import cv2
    import numpy as np
    
    # read
    img_frontground = cv2.imread("my_picture.jpg", 1)
    img_background1 = cv2.imread("./pic4findHam/img_background1.jpeg", 1)
    img_background2 = cv2.imread("./pic4findHam/img_background2.jpeg", 1)
    img_background3 = cv2.imread("./pic4findHam/img_background3.jpeg", 1)
    img_background4 = cv2.imread("./pic4findHam/img_background4.jpeg", 1)
    img_background5 = cv2.imread("./pic4findHam/img_background5.jpeg", 1)
    
    #copy origin frontground for output
    img_origin = img_frontground.copy()
    
    # gray
    img_frontground_gray = cv2.cvtColor(img_frontground, cv2.COLOR_BGR2GRAY)
    img_background1_gray = cv2.cvtColor(img_background1, cv2.COLOR_BGR2GRAY)
    img_background2_gray = cv2.cvtColor(img_background2, cv2.COLOR_BGR2GRAY)
    img_background3_gray = cv2.cvtColor(img_background3, cv2.COLOR_BGR2GRAY)
    img_background4_gray = cv2.cvtColor(img_background4, cv2.COLOR_BGR2GRAY)
    img_background5_gray = cv2.cvtColor(img_background5, cv2.COLOR_BGR2GRAY)
    
    # find difference
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fgmask = fgbg.apply(img_background5_gray)
    fgmask = fgbg.apply(img_background4_gray)
    fgmask = fgbg.apply(img_background3_gray)
    fgmask = fgbg.apply(img_background2_gray)
    fgmask = fgbg.apply(img_background1_gray)
    fgmask = fgbg.apply(img_frontground_gray)

    #erode & dilate
    ret, fgmask_bin = cv2.threshold(fgmask,126,255,cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(fgmask_bin, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=10)
    
    #find contour
    image, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #img = cv2.drawContours(img_frontground, contours, -1, (0,255,0),1)
    
    # find max contour 
    max_area=1
    max_area_contour=0
    for i, cnt in enumerate(contours):
        temp = cv2.contourArea(cnt)
        if temp>max_area:
            max_area=temp
            max_area_contour=i
    
    #draw HamPosi
    if max_area_contour==0:
        HamPosi=[[1,1]]
    else:
        HamPosi = sum(contours[max_area_contour])/len(contours[max_area_contour])    
#    img = cv2.drawContours(img_frontground, contours, max_area_contour, (0,255,0),1)
    img_findHam=cv2.circle(img_frontground, (int(HamPosi[0][0]),int(HamPosi[0][1])), 5, (0,255,0), thickness=-1)
    
    # display
    #cv2.imshow('frame',fgmask)
    #cv2.imshow('frame',fgmask_bin)
    #cv2.imshow('frame',erosion)
#    cv2.imshow('frame',img_findHam)

    # output
    bg_diff_path  = './findHam.jpg'
    cv2.imwrite(bg_diff_path,img_findHam)
    
    cv2.imwrite('./pic4findHam/img_background5.jpeg',img_background4)
    cv2.imwrite('./pic4findHam/img_background4.jpeg',img_background3)
    cv2.imwrite('./pic4findHam/img_background3.jpeg',img_background2)
    cv2.imwrite('./pic4findHam/img_background2.jpeg',img_background1)
    cv2.imwrite('./pic4findHam/img_background1.jpeg',img_origin)
    
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
#findHam()