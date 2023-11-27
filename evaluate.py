import torch
import warnings
import yaml
import argparse
warnings.filterwarnings('ignore')
import sys
sys.path.append("/home/ujlee/Templates/Speech_disorder/recognition/kosr/")
from kosr.model import build_model
from kosr.utils import build_conf
from kosr.trainer import evaluate, load
from kosr.utils.optimizer import build_optimizer
from kosr.data.dataset import get_dataloader
from kosr.data.dataset import get_path
from kosr.data.dataset import FBankDataset
import os
#os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
#os.environ["CUDA_VISIBLE_DEVICES"]="0"
import tensorflow as tf
'''
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True 
session = tf.compat.v1.Session(config=config)

config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.9

session = tf.compat.v1.Session(config=config)

def mains():
    parser = argparse.ArgumentParser(description='End-to-End Speech Recognition Training')
    parser.add_argument('--conf', default='config/ksponspeech_transformer_base.yaml', type=str, help="configuration path for training")
    parser.add_argument('--load_model', default='checkpoint/best_wer.pth', type=str, help="evaluate from saved model")
    args = parser.parse_args()
    conf = build_conf(args.conf)
    
    #batch_size = conf['train']['batch_size']
    path = ['C:\\Users\\user\\Desktop\\works\\flask\\220223\\kosr\\testdata\\ID-03-32-N-QASJ-02-030054-M-77-SU.pcm']
    #test_dataloader = get_dataloader(conf['dataset']['test'], batch_size=8, conf=conf)
    test_dataloader = get_dataloader(conf['dataset']['test'], batch_size=1, conf=conf)
   # d1 =datasets.FBankDataset

   # d1.__

    model = build_model(conf)
    optimizer = build_optimizer(model.parameters(), **conf['optimizer'])
    
   # saved_epoch = load(args, model, optimizer)
    
   # pred = 
    pred = evaluate(model, test_dataloader)

    return pred

#if __name__ == '__main__':
    #mai
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='End-to-End Speech Recognition Training')
    parser.add_argument('--conf', default='config/ksponspeech_transformer_base.yaml', type=str, help="configuration path for training")
    parser.add_argument('--load_model', default='checkpoint/best_wer.pth', type=str, help="evaluate from saved model")
    args = parser.parse_args()
    main(args)
'''
def mains(path):
    parser = argparse.ArgumentParser(description='End-to-End Speech Recognition Training')
    parser.add_argument('--conf', default='kosr/config/ksponspeech_transformer_base.yaml', type=str, help="configuration path for training")
    parser.add_argument('--load_model', default='kosr/checkpoint/best_wer.pth', type=str, help="evaluate from saved model")
    args = parser.parse_args()
    conf = build_conf(args.conf)
    
    batch_size = conf['train']['batch_size']
    path = path#'C:\\Users\\user\\Desktop\\works\\flask\\220223\\kosr\\testdata\\ID-03-32-N-QASJ-02-030054-M-77-SU.pcm'
    
    #c1.get_path(path)
    #test_dataloader = get_dataloader(conf['dataset']['test'], batch_size=8, conf=conf)
    #get_path(path)
    test_dataloader = get_dataloader(conf['dataset']['test'], batch_size=1, conf=conf,path=path)
    #c1 = FBankDataset(conf['dataset']['test'],root_dir='',conf=conf,path=path)
    model = build_model(conf)
    optimizer = build_optimizer(model.parameters(), **conf['optimizer'])
    
    saved_epoch = load(args, model, optimizer)
    
    pred = evaluate(model, test_dataloader)

    return pred

    

