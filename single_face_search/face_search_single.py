from utils.approximate_search import single_emb_search
from utils.general_utils import *
from utils.face_detection import face_detection


process_terminal_output = "Ready \n"
output_list = []
def run_single_search(file_addr, dir_addr):
    process_terminal_output = "Ready \n"
    check_file = image_support(file_addr)
    if check_file == -1:
        process_terminal_output += "File Does not Exist or Address Invalid \n"
    elif check_file == 0:
        process_terminal_output += "File format not support. Use one of the following image formats: \n"
        buff_format = ' '
        buff_format = buff_format.join(supported_image_formats)
        process_terminal_output += buff_format
        process_terminal_output += '\n'
    
    else:
        file_name, last_update = get_process_files(dir_addr, task='face_detection', media='image')
        detector = face_detection()
        if file_name == -1:
            process_terminal_output += "Directory not Processed \n"
            process_terminal_output += "Processing Directory \n"

            detector.process_dir_img(dir_addr)
            detector.process_dir_videos(dir_addr)

            process_terminal_output += "Done Processing Directory"

            file_name, last_update = get_process_files(dir_addr, 'face_detection', 'image')


        face_emb = detector.get_face_emb(file_addr)
        
        output_list = single_emb_search(file_name, face_emb, num_results=100)

    return output_list


        
    