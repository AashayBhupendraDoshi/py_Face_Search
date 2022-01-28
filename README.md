# Python Face Search
## Introduction
This is a python based GUI application for single and multi face search. The GUI is built using PyQt5, the face detection algorithms are build using [InsightFace](https://github.com/deepinsight/insightface/tree/master/python-package) and the indexing and ANN algorithms are built using  [Faiss](https://github.com/facebookresearch/faiss) library using [HNSW](https://arxiv.org/abs/1603.09320) algorithm.

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
## Double Search
### Note
Process files and store them in 'process_files' directory
There will be an index file to track and keep recprd of all process files
Each directory will have media and task specific process files
Process files will be pickled pandas dataframes with three entries:
[file_name, directory_address, last_updated]
