import datetime
import os
import sys
import hashlib
import numpy as np
import pandas as pd
import cv2
#import face_model
import insightface
from utils.general_utils import get_filelist_from_root, supported_image_formats, supported_video_formats

#assert insightface.__version__>='0.3'


class face_detection():
    def __init__(self):
        # Det-size is the image size
        self.det_size = 640
        self.gpu = -1
        self.supported_image_formats = supported_image_formats
        self.supported_video_formats = supported_video_formats
        self._init_model()

    def _init_model(self):
        self.model = insightface.app.FaceAnalysis()

        self.model.prepare(ctx_id = self.gpu, det_size = (self.det_size, self.det_size) )



    def process_dir_img(self, root_directory_address):
        # This method will recursively check all files within root directory
        # For images and videos, it will pre-process , annotate and generate
        # representations for the detected/annotated object.
        # It will create a dataframe to store these annotations.
        # This will later be extended for all forms of data
        
        file_list = get_filelist_from_root(root_directory_address)
        total_faces = []
        image_list = []
        df_list = []
        bbox=[]
        det_score = []
        embedding = []
        file_name = []
        original_resolution = []
        for vals in file_list:
            #if vals.split('.')[-1].lower() == 'jpg' and len(vals.split('.'))<3:
            #if vals.split('.')[-1].lower() in supported_image_formats and len(vals.split('.'))<3:
            if vals.split('.')[-1].lower() in self.supported_image_formats and len( os.path.split(vals)[-1].split('.') )<3:
                image_list += [vals]
        
        #print(len(image_list), image_list[0])

        for names in image_list:
            # Do not add root_directory_address since get_filelist_from_root returns
            # complete address from Linux Filesystem ROOT
            #image = cv2.imread(root_directory_address + names)
            image = cv2.imread(names)
            original_shape = image.shape
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            ############ Scaling Very Large Images if Necessary #########################
            # Scaling image to within set max dimension
            # Since images can be of different sizes, the maximum dimension needs to be
            # scaled to winthin set limit
            dimension_limit = self.det_size
            max_dim = max(image.shape)
            if max_dim > dimension_limit:
                ratio = dimension_limit/max_dim
                new_dimension = (int(ratio*image.shape[0]), int(ratio*image.shape[1]))
                image = cv2.resize(image, new_dimension, interpolation = cv2.INTER_AREA)
            #############################################################################

            faces = self.model.get(image)
            # Continue if nothing is detected
            if len(faces) == 0:
                continue
            else:
                total_faces += faces
                # Add file name column to know which file the matching entity in stored
                # The filename also contains the file address within the search (root) directory
                #df_list += [buff_df]
                file_name += [names]*len(faces)
                # Add original image resolution to dataframe
                original_resolution += [original_shape]*len(faces)

        for vals in total_faces:
            bbox += [vals.bbox]
            det_score += [vals.det_score]
            embedding += [vals.embedding]


            


        df_list = { 
                    'bbox': bbox,
                    'embeddings': embedding,
                    'file_name': file_name,
                    'original_resolution': original_resolution
                    }
        

        # Convert dictionary to pandas FataFrame
        df_list = pd.DataFrame(df_list)

        # Save dataframe to process_files directory
        df_hash = hashlib.md5(df_list.to_json().encode()).hexdigest()
        name  = str(df_hash)
        df_list.to_pickle('./process_files/' + name + '.pkl')

        # Update index file
        index_df = pd.read_pickle('./process_files/index_face_detection_image.pkl')
        buff_dict = {'file_name': [name + '.pkl'],
                    'directory_address': [root_directory_address],
                    'last_updated': [datetime.datetime.now()]
                    }
        buff_df = pd.DataFrame(buff_dict)

        #buff_df['file_name'] = name + '.pkl'
        #buff_df['directory_address'] = root_directory_address
        #buff_df['last_updated'] = datetime.datetime.now()
        if index_df.empty:
            index_df = buff_df
            #buff_df.to_pickle('./process_files/index_face_detection_image.pkl')

        else:
            index_df = pd.concat([index_df, buff_df], axis=0)
        
        index_df.to_pickle('./process_files/index_face_detection_image.pkl')

#        return df_list




    def process_dir_videos(self, root_directory_address):
        # This method will recursively check all files within root directory
        # For images and videos, it will pre-process , annotate and generate
        # representations for the detected/annotated object.
        # It will create a dataframe to store these annotations.
        # This will later be extended for all forms of data
        
        file_list = get_filelist_from_root(root_directory_address)
        total_faces = []
        video_list = []
        df_list = []
        bbox=[]
        det_score = []
        embedding = []
        file_name = []
        original_resolution = []
        frame = []
        for vals in file_list:
            #if vals.split('.')[-1].lower() == 'jpg' and len(vals.split('.'))<3:
            #if vals.split('.')[-1].lower() in supported_image_formats and len(vals.split('.'))<3:
            if vals.split('.')[-1].lower() in self.supported_video_formats and len( os.path.split(vals)[-1].split('.') )<3:
                video_list += [vals]
        
        print(len(video_list), video_list[0])

        for names in video_list:
            # Do not add root_directory_address since get_filelist_from_root returns
            # complete address from Linux Filesystem ROOT
            #image = cv2.imread(root_directory_address + names)
            #image = cv2.imread(names)
            cap = cv2.VideoCapture(names)
            #original_shape = image.shape
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            buff_frame = 0
            while cap.isOpened():

                ############ Scaling Very Large Images if Necessary #########################
                # Scaling image to within set max dimension
                # Since images can be of different sizes, the maximum dimension needs to be
                # scaled to winthin set limit
                ret, image = cap.read()
                if not ret:
                    break

                original_shape = image.shape
                dimension_limit = self.det_size
                max_dim = max(image.shape)
                if max_dim > dimension_limit:
                    ratio = dimension_limit/max_dim
                    new_dimension = (int(ratio*image.shape[0]), int(ratio*image.shape[1]))
                    image = cv2.resize(image, new_dimension, interpolation = cv2.INTER_AREA)
                #############################################################################

                faces = self.model.get(image)
                # Continue if nothing is detected
                if len(faces) == 0:
                    continue
                else:
                    total_faces += faces
                    # Add file name column to know which file the matching entity in stored
                    # The filename also contains the file address within the search (root) directory
                    #df_list += [buff_df]
                    file_name += [names]*len(faces)
                    # Add original image resolution to dataframe
                    original_resolution += [original_shape]*len(faces)
                    frame += [buff_frame]*len(faces)

                buff_frame+=1
                
                

        for vals in total_faces:
            bbox += [vals.bbox]
            det_score += [vals.det_score]
            embedding += [vals.embedding]


            


        df_list = { 
                    'bbox': bbox,
                    'embeddings': embedding,
                    'file_name': file_name,
                    'original_resolution': original_resolution,
                    'frame number': frame
                    }
        
        # Convert dictionary to pandas FataFrame
        df_list = pd.DataFrame(df_list)

        # Save dataframe to process_files directory
        df_hash = hashlib.md5(df_list.to_json().encode()).hexdigest()
        name  = str(df_hash)
        df_list.to_pickle('./process_files/' + name + '.pkl')

        # Update index file
        index_df = pd.read_pickle('./process_files/index_face_detection_video.pkl')
        buff_df = pd.DataFrame()
        buff_df['file_name'] = name + '.pkl'
        buff_df['directory_address'] = root_directory_address
        buff_df['last_updated'] = datetime.datetime.now()
        index_df = pd.concat([index_df, buff_df], axis=0)
        index_df.to_pickle('./process_files/index_face_detection_video.pkl')

#        return df_list

    def get_face_emb(self, file_addr):
        # Returns face embeddings as well as the bounding box from the selected image

        image = cv2.imread(file_addr)
        original_shape = image.shape
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        ############ Scaling Very Large Image if Necessary #########################
        # Scaling image to within set max dimension
        # Since images can be of different sizes, the maximum dimension needs to be
        # scaled to winthin set limit
        dimension_limit = self.det_size
        max_dim = max(image.shape)
        if max_dim > dimension_limit:
            ratio = dimension_limit/max_dim
            new_dimension = (int(ratio*image.shape[0]), int(ratio*image.shape[1]))
            image = cv2.resize(image, new_dimension, interpolation = cv2.INTER_AREA)
        #############################################################################

        faces = self.model.get(image)
        
        if len(faces) == 0:
        # Continue if nothing is detected
            return -1,-1,-1

        elif len(faces) > 1:
        # If more than 1 faces are detected
            return 1,1,1
        
        else:
            embedding = faces[0].embedding
            bbox = faces[0].bbox
            return embedding, bbox,0


