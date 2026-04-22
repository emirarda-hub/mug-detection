import pandas as pd
import os
import torch


from dataset import ObjDetectionDataset
from torch.utils.data import DataLoader

from model import build_model
from args import get_args
from training import train_model



def collate(batch):
    images, targets = zip(*batch)
    return list(images), list(targets)

def main():
    args = get_args()

    #1. Read your dataframes

    train_df = pd.read_csv("data/CSVs/train_df.csv")
    val_df = pd.read_csv(os.path.join(args.csv_dir,"val_df.csv"))

    # 2. Prepare datasets
    train_dataset = ObjDetectionDataset(train_df)
    val_dataset = ObjDetectionDataset(val_df)

    # 3. Create Data loaders
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, collate_fn=collate, num_workers=0, pin_memory=False)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, collate_fn=collate, num_workers=0, pin_memory=False)

    images , targets = next(iter(train_loader))
    print("Loader OK.")   

    from utils import show_batch

    show_batch(images, targets)
    print("Batch images saved.")
    

    # 4 INITIALIZING MODEL
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = build_model(args.backbone, num_classes=args.num_classes +1)

    #5. Train the model

    train_model(model, train_loader, val_loader, device)



if __name__ == "__main__" :
    main()

