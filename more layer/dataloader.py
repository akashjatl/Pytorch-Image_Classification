from PIL import Image
from torch.utils.data import Dataset
import os
from glob import glob
import torch
import torchvision.transforms as transforms

# Dataset Class for Setting up the data loading process
# Stuff to fill in this script: _init_transform()


class inaturalist(Dataset):
    def __init__(self, root_dir,  transform=True):
        self.data_dir = root_dir
        # self.mode = mode
        self.transforms = transform
        self._init_dataset()
        if transform:
            self._init_transform()

    def _init_dataset(self):
        self.files = []
        self.labels = []
        dirs = sorted(os.listdir(self.data_dir))
        # if self.mode == 'train':
        for dir in range(len(dirs)):
            files = sorted(
                glob(os.path.join(self.data_dir, dirs[dir], '*.jpg')))
            self.labels += [dir]*len(files)
            self.files += files
            
        
        # elif self.mode == 'val':
        #     for dir in range(len(dirs)):
        #         files = sorted(
        #             glob(os.path.join(self.data_dir, 'val', dirs[dir], '*.jpg')))
        #         self.labels += [dir]*len(files)
        #         self.files += files
        # else:
        #     print("No Such Dataset Mode")
        #     return None
        

    def _init_transform(self):
        self.transform = transforms.Compose([
            transforms.RandomResizedCrop(128),
            transforms.RandomHorizontalFlip(),
            transforms.PILToTensor(),
            transforms.ConvertImageDtype(torch.float)

        ])

    def __getitem__(self, index):
        img = Image.open(self.files[index]).convert('RGB')
        label = self.labels[index]

        if self.transforms:
            img = self.transform(img)

        label = torch.tensor(label, dtype=torch.long)

        return img, label

    def __len__(self):
        return len(self.files)
