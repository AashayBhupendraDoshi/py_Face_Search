import time
import numpy as np
import pandas as pd
import faiss

def single_emb_search(process_file_addr, query_emb, num_results):
    # process_file_addr: complete address of process file
    # query_emb: search vector oof shape [1, vector_length]
    process_file = pd.read_pickle('./process_files/' + process_file_addr)
    #face_embeddings = process_file['embeddings']
    #Expand Dims of Query to [1, dims]
    query_emb = np.expand_dims(query_emb, axis=0)
    
    # Reshape process_file['embeddings'] to [n, dims]
    embs = np.stack(process_file['embeddings'], axis=0)
    #embs = []
    #for vals in process_file['embeddings']:
    #    embs +=[vals]
    #embs = np.array(embs)
    #print(embs.shape)
    #print(embs.shape, query_emb.shape)
    if num_results > len(embs):
        num_results = len(embs)

    dims = query_emb.shape[1]
    maxM = 16
    index = faiss.IndexHNSWFlat(dims, maxM)
    # training is not needed
    # this is the default, higher is more accurate and slower to
    # construct
    index.hnsw.efConstruction = 40
    # to see progress
    index.verbose = True
    index.add(embs)

    t0 = time.time()
    #query = np.expand_dims(embs[50],1).T
    D, I = index.search(query_emb, num_results)
    t1 = time.time()
    #print(t1-t0)
    # Remove -1 from I
    I = [i for i in I[0] if i!=-1]
    #process_file[I[0]]
    # Filter out data
    #output = process_file.loc[I[0]]
    output = process_file.loc[I]
    #output = process_file[process_file.index.isin(I[0])]

    return output

def double_emb_search_01(process_file_addr, emb1, emb2, num_results):
    # Dumb Method, Approximate Results on top of approximate search
    emb_1_result = single_emb_search(process_file_addr, emb1, 10000)
    emb_2_result = single_emb_search(process_file_addr, emb2, 10000)
    common_files = set(emb_1_result['file_name']).intersection(emb_2_result['file_name'])
    
    emb_1_result = emb_1_result[emb_1_result['file_name'].isin(common_files)]
    emb_2_result = emb_2_result[emb_2_result['file_name'].isin(common_files)]

    # Remove duplicates incase a person is detected twice in a single image
    emb_1_result = emb_1_result.drop_duplicates(subset=['file_name'])
    emb_2_result = emb_2_result.drop_duplicates(subset=['file_name'])

    # Shift Index to 'file_name
    emb_1_result = emb_1_result.reset_index().set_index('file_name')
    emb_2_result = emb_2_result.reset_index().set_index('file_name')

    # Reindex Based On Columns
    emb_1_result = emb_1_result.reindex(common_files)
    emb_2_result = emb_2_result.reindex(common_files)

    # Shift Index back
    emb_1_result = emb_1_result.reset_index().set_index('index')
    emb_2_result = emb_2_result.reset_index().set_index('index')

    emb_1_result = emb_1_result.reset_index(drop=True)
    emb_2_result = emb_2_result.reset_index(drop=True)


    print(emb_1_result.iloc[:10])
    print(emb_2_result.iloc[:10])

    emb_1_result['embeddings2'] = emb_2_result['embeddings']
    emb_1_result['bbox2'] = emb_2_result['bbox']


    # Pad to fixed size of 100
    if len(emb_1_result)>100:
        emb_1_result = emb_1_result.iloc[:100]
    if len(emb_1_result)<100:
        padding = 100 - len(emb_1_result)
        emb_1_result = pd.concat([emb_1_result,emb_1_result.iloc[:padding]])
        emb_1_result = emb_1_result.reset_index(drop=True)

    return emb_1_result



def double_emb_search_02(process_file_addr, emb1, emb2, num_results):
    process_file = pd.read_pickle('./process_files/' + process_file_addr)
    
    # Calcculate similarity score for emb1 and store
    emb1_dot = np.dot(emb1, emb1)
    emb1 = np.expand_dims(emb1, axis=1)
    #b = np.matmul(a.embeddings, np.expand_dims(emb1, axis=1))
    #np.expand_dims(emb1, axis=1).shape
    embs = np.stack(process_file['embeddings'], axis=0)
    sim_score1 = np.matmul(embs, emb1)
    sim_score1 = sim_score1/emb1_dot
    process_file['sim_score1'] = sim_score1

    # Calcculate similarity score for emb2 and store
    emb2_dot = np.dot(emb2, emb2)
    emb2 = np.expand_dims(emb2, axis=1)
    sim_score2 = np.matmul(embs, emb1)
    sim_score2 = sim_score2/emb2_dot
    process_file['sim_score2'] = sim_score2

    #Reshape Dims to [1, dims]
    emb1 = emb1.T
    emb1 = emb2.T
    
    final_dict = {}
    file_name = []
    emb = []
    emb2 = []
    bbox = []
    bbox2 = []
    original_resolution = []
    total_sim_score = []
    i=0
    while i < len(process_file):
        buff_name = process_file['file_name'].iloc[i]
        j = i+1
        # Find all detections in an image
        while process_file['file_name'].iloc[i] == buff_name:
            j+=1
        
        print(i,j)
        # if only one person is detected go to the next image
        if j==i+1:
            i=j+2
            continue
            
        
        #Else Continue with the process
        #image_wise_df = a.iloc[i:j]
        max_score_emb1 = -1
        max_score_emb2 = -1
        sim1_loc = i
        sim2_loc = i+1
        for k in range(i,j):
            buff_sim1 = process_file['sim_score1'].iloc[k]
            buff_sim2 = process_file['sim_score2'].iloc[k]
            
            if buff_sim1 > buff_sim2 and buff_sim1 > max_score_emb1:
                max_score_emb1 = buff_sim1
                sim1_loc = k

            if buff_sim2 > buff_sim1 and buff_sim2 > max_score_emb2:
                max_score_emb2 = buff_sim2
                sim2_loc = k
        
        file_name += [process_file['file_name'].iloc[i]]
        emb += [process_file['embeddings'].iloc[sim1_loc]]
        emb2 += [process_file['embeddings'].iloc[sim2_loc]]
        bbox += [process_file['bbox'].iloc[sim1_loc]]
        bbox2 += [process_file['bbox'].iloc[sim2_loc]]
        original_resolution += [process_file['original_resolution'].iloc[i]]
        total_sim_score += [ max_score_emb1 + max_score_emb2]
        
        i=j+1
        
        
    output = pd.DataFrame()
    output['file_name'] = file_name
    output['embeddings'] = emb
    output['embeddings2'] = emb2
    output['bbox'] = bbox
    output['bbox2'] = bbox2
    output['score'] = total_sim_score
    output['original_resolution'] = original_resolution

    output = output.sort_values(by=['score'], ascending = False)#, inplace=True)
    output = output.reset_index(drop=True)

    print(output)
    return output