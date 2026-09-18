from glob import glob
import os

csv_files = glob("../data/csv_by_subject/*.csv")
dicom = glob("../data/dicom/*.dcm")
dna = glob("../data/dna/*.csv")

subject_prefix = [os.path.basename(csv).replace(".csv", "") for csv in csv_files]
splits = [subject_prefix[:len(subject_prefix)//2], subject_prefix[len(subject_prefix)//2:]]
print(subject_prefix[:5], len(subject_prefix))
print(len(splits[0]), len(splits[1]))

# copy half of all files to BB1, second half of all files to BB2
for f in splits[0]:
    # check if file exists in csv and dna folders
    if len(glob(f"../data/dicom/{f}*.dcm")) == 0:
        continue
    #print(glob(f"../data/dicom/{f}*.dcm")[0], len(glob(f"../data/dicom/{f}*.dcm")))
    print(os.path.exists(glob(f"../data/dicom/{f}*.dcm")[0]))
    if os.path.exists(f"../data/csv_by_subject/{f}.csv"):
        os.system(f"cp ../data/csv_by_subject/{f}.csv ../data/BB1/csv/") 
        match_dcm = glob(f"../data/dicom/{f}*.dcm")[0]
        os.system(f"cp {match_dcm} ../data/BB1/dicom/")
for f in splits[1]:
    # check if file exists in csv and dna folders
    if len(glob(f"../data/dicom/{f}*.dcm")) == 0:
        continue
    #print(glob(f"../data/dicom/{f}*.dcm")[0], len(glob(f"../data/dicom/{f}*.dcm")))
    print(os.path.exists(glob(f"../data/dicom/{f}*.dcm")[0]))
    if os.path.exists(f"../data/csv_by_subject/{f}.csv"):
        os.system(f"cp ../data/csv_by_subject/{f}.csv ../data/BB2/csv/") 
        match_dcm = glob(f"../data/dicom/{f}*.dcm")[0]
        os.system(f"cp {match_dcm} ../data/BB2/dicom/")



#for f in splits[1]:
#    if os.path.exists(f"../data/csv_by_subject/{f}.csv") and os.path.exists(glob.glob(f"../data/dna/{f}.dcm")):
#        os.system(f"cp ../data/csv_by_subject/{f}.csv ../data/BB2/csv/")
#        os.system(f"cp ../data/dna/{f}_dna.csv ../data/BB2/dna/")
