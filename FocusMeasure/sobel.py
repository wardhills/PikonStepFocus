import cv2
from matplotlib import pyplot as plt
import os
import csv
import pandas as pd

''' reference: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.html for the basic
opencv and https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/ for an example of how to use 
.var() to measure focus'''

def calc_grade(img):
    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)

    return laplacian, sobelx, sobely

def calc_grade_var(img):
    laplacian, sobelx, sobely = calc_grade(img)

    laplacian_var = laplacian.var()
    print('laplacian :', laplacian_var)

    sobelx_var = sobelx.var()
    print('sobelx     : ', sobelx_var)

    sobely_var = sobely.var()
    print('sobely     : ', sobely_var)

    sobelxy_var = (sobelx_var+sobely_var)/2
    print('sobelxy ave  : ', sobelxy_var)

    return laplacian_var, sobelx_var, sobely_var, sobelxy_var

def plot_grade(img, grade0, grade1, grade2):
    plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])

    plt.subplot(2,2,2),plt.imshow(grade0,cmap = 'gray')
    plt.title('Laplacian'), plt.xticks([]), plt.yticks([])

    plt.subplot(2,2,3),plt.imshow(grade1,cmap = 'gray')
    plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

    plt.subplot(2,2,4),plt.imshow(grade2,cmap = 'gray')
    plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

    plt.show()
    return

def record_output_create(path, f_name, headers):
    path_f_name = os.path.join(path, f_name)

    if os.path.isfile(path_f_name) == False:
        print(f_name, 'does not exist, creating')
        measurement_list = headers.split(',')
        record_output(path, f_name, measurement_list)
        return path_f_name

def record_output(path, name, fields):
    path_f_name = os.path.join(path, name)
    with open(path_f_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        #todo seperate the path and image name feilds

def dir_exam(directory, output_file='focus_quality.csv'):
    headers = 'image_name,Laplacian,Sobel_X,Sobel_Y,Sobel_Ave'  #todo  make these namesgeneric and usr settable
    record_output_create(directory,output_file, headers)

    for filename in os.listdir(directory):
        if filename.endswith(".bmp"):
            f = os.path.join(directory, filename)
            image = cv2.imread(f, 0)
            print(f)
            l, sx,sy,s_xy= calc_grade_var(image)
            values = [filename,l,sx,sy,s_xy]
            record_output(directory,output_file, values)
            continue
        else:
            continue

def file_exam(filename, directory='./'):
    f = os.path.join(directory, filename)
    image = cv2.imread(f, 0)
    #l,sx,sy,s_xy = calc_grade(image)
    l, sx, sy = calc_grade(image)
    plot_grade(image,l,sx,sy)
    return l,sx,sy,s_xy

def sort_csv(i_directory, i_filename, o_directory, o_filename, clmn):
    i_f = os.path.join(i_directory, i_filename)
    df = pd.read_csv(i_f)
    print(df)
    # print(column)
    df = df.sort_values(by=[clmn], ascending=False)
    print(df)
    o_f = os.path.join(o_directory, o_filename)
    df = df.reset_index(drop=True)
    df.to_csv(o_f, index=True)

if __name__ == "__main__":
##  To analyse the contents of a ldirectory use this code
    # directory = '/home/ward/Desktop/expsurdata'
    directory = '/home/ward/Desktop/Telescope_data/Saturn'
    #directory = '/home/ward/Desktop/Telescope_data/Saturn/pipp_20180806_162358'
    #directory = '/home/ward/Desktop/Telescope_data/Saturn/pipp_20180806_162358/20180805_193642 0'

    # i_file = 'focus_quality.csv'
    # i_dir = '/home/ward/Desktop/Telescope_data/Saturn'
    # # i_dir = '/home/ward/Desktop/Telescope_data/Saturn/pipp_20180806_162358/20180805_193642 0/'
    # o_dir = '/home/ward/PycharmProjects/cv_learn/'
    # o_file = 'focus_quality-sorted.csv'
    # col = 'Sobel_Y'

    #dir_exam(i_dir, i_file)
    #sort_csv(i_dir, i_file, o_dir, o_file, col)

    testimage = 'test_img.bmp'

    file_exam(testimage)


##todo add show best plot:: plot_grade(img, grade0, grade1, grade2)

    #name ='07_20180805_194039 0.bmp'
    #file_exam(directory, name)