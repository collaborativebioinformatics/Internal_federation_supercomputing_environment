import torchvision, os
from glob import glob

data_path = '/tmp/nvflare/data'

# LATER; TODO:
# nvflare simulator -n 2 -t 2 /tmp/nvflare/jobs/job_config/pt_lightning_client_api  --gpu "[0,1],[0,1]"

csv_by_subject = glob(f"../data/csv_by_subject/*.csv", recursive=True)
print("CSV by subject:", [os.path.basename(csv) for csv in csv_by_subject[:2]])

dicom = glob(f"../data/dicom/*.dcm", recursive=True)
subject_prefix = ["_".join(os.path.basename(dcm).split('_')[:2]) for dcm in dicom[:2]]

print("Subject prefixes found:", subject_prefix)

print("DICOM files found:", [os.path.basename(dcm).split('.')[0] for dcm in dicom[:2]])

to_rename = [os.path.basename(csv) for csv in csv_by_subject] # csv's
dicoms = [os.path.basename(dcm).split('.')[0] for dcm in dicom] # DICOM

# print("subjects with csv and dicom:", len(res))

# in the csv_by_subject folder rename the digits 0_24_.. to Annmarie79_Hickle134_... just like in the other folders for a common naming
for i, f in enumerate(to_rename):
    for j, d in enumerate(dicoms):
        if f.split('_')[2].replace('.csv', '') in d:
            print(f"Renaming {f} to {d}.csv")
            os.rename(f"../data/csv_by_subject/{f}", f"../data/csv_by_subject/{d}.csv")




# dataset = torchvision.datasets.CIFAR10(root=data_path, train=True, download=False)
# image, label = dataset[0]
# print("Dataset size:", len(dataset))
# print("First image class ID:", label)
# print("First image class name:", dataset.classes[label])
# image.show()