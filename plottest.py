import streamlit as st
import pandas as pd
import os
# import matplotlib.pyplot as plt
# from data import DIV2K
# from model.edsr import edsr
# from train import EdsrTrainer

depth = 16
scale = 4
downgrade = 'bicubic'

weights_dir = f'C:/Users/ADMIN/Documents/Visualization/weights'
weights_file = os.path.join(weights_dir, 'weights.h5')

os.makedirs(weights_dir, exist_ok=True)

div2k_train = DIV2K(scale=scale, subset = 'train')
div2k_valid = DIV2K(scale=scale, subset = 'valid')

train_ds = div2k_train.dataset(batch_size=16, random_transform=True)
valid_ds = div2k_valid.dataset(batch_size=1, random_transform=False, report_count=1)

trainer = EdsrTrainer(model=edsr(scale=scale, num_res_blocks=depth),
                      checpont_dir = f' .ckpt/edsr-{depth}-x{scale}')

trainer.train(train_ds, valid_ds.take(10),
              steps = 300000,
              evaluation_every=1000,
              save_best_only=True)

trainer.model.save_weights(weights_file)

model =edsr(scale=scale, num_res_blocks=depth)
model.load_weights(weights_file)

from model import resolve_single
from utils import load_image, plot_sample

def resolve_and_plot(lr_image_path):
    lr = load_image(lr_image_path)
    sr = resolve_single(model, lr)
    plot_sample(lr, sr)

resolve_and_plot('DS1.jpg')

