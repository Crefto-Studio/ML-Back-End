from PIL import Image
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import boto3


S3_BUCKET = 'autodraw' 
folder = 'features/'
file_name = "feature_extraction_6.csv"

s3 = boto3.client('s3',
         aws_access_key_id='AKIAYHBCWEYTNPL6AYV4',
         aws_secret_access_key= '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')

obj = s3.get_object(Bucket= S3_BUCKET, Key= folder+ file_name)

class FeatureExtractor:
    def __init__(self):
        
        # Use VGG-16 as the architecture and ImageNet for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        
    def extract(self, img):
        
        # Resize the image
        img = img.resize((224, 224))
        # Convert the image color space
        img = img.convert('RGB')
        
        # Reformat the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Extract Features
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)
    
def perdict_img(file):
    
    fe = FeatureExtractor()
    np_array = np.array(file)     
    img = Image.fromarray(np_array, mode='L')
    
    # Extract its features
    query = fe.extract(img)
  
    features = pd.read_csv(obj['Body'])

    # Calculate the similarity (distance) between images
    features_data = features.drop(columns = ['image'])

    features_data = features_data.values

    dists = np.linalg.norm(features_data - query, axis=1)

    # Extract 30 images that have lowest distance
    ids = np.argsort(dists)[:10]
  
    lookalike_imgs = features.iloc[ids,:]['image']

    scores = pd.DataFrame({'image': lookalike_imgs,
                        'score': dists[ids]})


    scores = scores.reset_index(drop=True) 

    scores = scores.to_json(orient='index')


    # scores is a dataframe object contrain 2 columns image name and its score
    # scores contains the 10 least score images according to input image
    # |____image_name______|____score_____|  
    # |______456.png_______|____8.235_____| 
    # |______789.png_______|____7.258_____| 
    # |______752.png_______|____7.123_____| 
    # |______982.png_______|____6.123_____| 

    # Visualize the result
    # axes=[]
    # fig=plt.figure(figsize=(8,8))
    # for a in range(1*10): #in case we want 20 images --> for a in range(1*20)
    #     score = scores['score'][a]
    #     axes.append(fig.add_subplot(2, 5, a+1)) # axes.append(fig.add_subplot(2, 10, a+1))
    #     subplot_title=str(scores['image'][a])
    #     axes[-1].set_title(subplot_title)  
    #     plt.axis('off')
    #     plt.imshow(Image.open(Image_Data_Path+ 'dataset/'+ scores['image'][a]))
    # fig.tight_layout()
    # plt.show()
    return scores

