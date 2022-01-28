# Python Face Search
## Introduction
![](https://github.com/AashayBhupendraDoshi/py_Face_Search/blob/main/images/double_result.png)
This is a python based GUI application for single and multi face search. The GUI is built using PyQt5, the face detection algorithms are build using [InsightFace](https://github.com/deepinsight/insightface/tree/master/python-package) and the indexing and ANN algorithms are built using  [Faiss](https://github.com/facebookresearch/faiss) library. All the unary search (,i.e., the complete single search and individual searches in the multi-search algorithm) using [HNSW](https://arxiv.org/abs/1603.09320) algorithm.

## Installation:

* Clone the project:

    ```
    git clone https://github.com/AashayBhupendraDoshi/py_Face_Search.git

    ```

* For installing all packages in `requirements.txt` file, run following command in your project directory:
    ```
    pip3 install -r requirements.txt
    ```
## Single Search
To run the single search simply run:
    ```
    python3 ./single_face.py
    ```

You will then be prompted with a basic GUI to select the image of the person to search and the directory to search the images of the person into.
You can then click run to start searching  the images. The results will shown as a list of clickable results with the file address relative to the root directory along with the bounding boxes.
![](https://github.com/AashayBhupendraDoshi/py_Face_Search/blob/main/images/single.gif)
<p align="center">
  <img src="https://github.com/AashayBhupendraDoshi/py_Face_Search/blob/main/images/single.gif">
</p>

## Double Search
Run the following command:
    ```
    python3 ./double_face.py
    ```

The GUI will be similar to the single_search application
![](https://github.com/AashayBhupendraDoshi/py_Face_Search/blob/main/images/double.gif)

### Note
- Process files and store them in 'process_files' directory
- There will be an index file to track and keep recprd of all process files
- Each directory will have media and task specific process files
- Process files will be pickled pandas dataframes with three entries: [file_name, directory_address, last_updated]
