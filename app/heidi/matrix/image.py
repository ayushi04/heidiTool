import numpy as np
from PIL import Image

def generateHeidiImage(heidi_matrix,transform_dict):
    print('-----GENERATEiMAGE : generateHeidiImage ------')
    arr=np.zeros((heidi_matrix.shape[0],heidi_matrix.shape[1],3))
    for i in range(heidi_matrix.shape[0]):
        for j in range(heidi_matrix.shape[1]):
            if heidi_matrix[i][j] in transform_dict.keys():
                arr[i][j]=transform_dict[heidi_matrix[i][j]]
            else:
                arr[i][j]=[255,255,255]
    tmp=arr.astype(np.uint8)
    img_top100 = Image.fromarray(tmp)
    return img_top100,tmp


# Input:
# Matrix Map:- {('sl', 'sw'): array([[1, 0, 0, ..., 0, 0, 0],
# Legend :- 
#  dataset  subspace        dimensions            color
# 0   static/uploads/iris2.csv         1              [sl]    [51, 98, 107] 
# 1   static/uploads/iris2.csv         2              [sw]    [240, 74, 28] 
def createImage(matrix_map, legend):
    #write code to create image for each matrix in matrix map, color value is present in legend for each matrix
    image_map = {}
    for subspace in matrix_map:
        # subspace = matrix_map[key]
        for index, row in legend.iterrows():
            if row['dimensions'] == list(subspace):
                color = row['color']
                break

        # update matrix set non null value to color
        matrix = matrix_map[subspace]
        color_matrix=np.zeros((matrix.shape[0],matrix.shape[1],3))
        
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i][j]:
                    color_matrix[i][j]=color
                else:
                    color_matrix[i][j]=[255,255,255]
        color_matrix = color_matrix.astype(np.uint8)
        image = Image.fromarray(color_matrix)
        # Save the image to a file
        image.save('static/output_image.png')
        image_map[subspace] = image
    return image_map

def consolidateImage(image_map):
    consolidateImage = None
    for (subspace, image) in image_map.items():
        if consolidateImage is None:
            consolidateImage = image
        else:
            consolidateImage.paste(image, (0, 0))
    return consolidateImage
            
    
