import logging
import datetime
import sys
import imutils
import cv2

from skimage.measure import compare_ssim

__author__ = 'cstolz'

logging.basicConfig(filename='pimonitor.log', level=logging.INFO)


def main():
    try:
        image1 = cv2.imread(image_name1)
        image2 = cv2.imread(image_name1)
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        score, diff = compare_ssim(image1_gray, image2_gray, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        for contour in contours:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("Original", image1)
        cv2.imshow("Modified", image2)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thresh)
        cv2.waitKey(0)

    except Exception as err:
        print err
        logging.error('[%s] %s', str(datetime.datetime.now()), err)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        image_name1 = sys.argv[1]
        image_name2 = sys.argv[2]

    else:
        image_name1 = 'cc1.png'
        image_name2 = 'cc2.png'
    main()