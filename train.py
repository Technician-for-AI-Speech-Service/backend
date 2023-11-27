import torch 
import gc
gc.collect()
torch.cuda.empty_cache()
import warnings
import yaml
import argparse
warnings.filterwarnings('ignore')
import sys
sys.path.append("/home/ujlee/Templates/kosr/")

from kosr.model import build_model
from kosr.utils import build_conf
from kosr.trainer import train_and_eval, load
from kosr.utils.loss import build_criterion
from kosr.utils.optimizer import build_optimizer
from kosr.data.dataset import get_dataloader
from kosr.utils.convert import vocab
import tensorflow as tf
        
import os 
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '1'

#config = tf.compat.v1.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.9

#session = tf.compat.v1.Session(config=config)


def main(args):
    conf = build_conf(args.conf)
    
    batch_size = conf['train']['batch_size']
    
    train_dataloader = get_dataloader(conf['dataset']['train'], batch_size=batch_size, mode='train', conf=conf)
    valid_dataloader = get_dataloader(conf['dataset']['valid'], batch_size=batch_size, conf=conf)
    test_dataloader = get_dataloader(conf['dataset']['test'], batch_size=batch_size, conf=conf)
    
    model = build_model(conf)
    criterion = build_criterion(conf)
    optimizer = build_optimizer(model.parameters(), **conf['optimizer'])
    
    saved_epoch = load(args, model, optimizer)
    
    train_and_eval(conf['train']['epochs'], model, optimizer, criterion, train_dataloader, valid_dataloader, conf['setting']['loss_type'], epoch_save=True, saved_epoch=saved_epoch)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='End-to-End Speech Recognition Training')
    parser.add_argument('--conf', default='config/ksponspeech_transformer_base.yaml', type=str, help="configuration path for training")
    parser.add_argument('--load_model', default='/home/ujlee/Templates/kosr/kosr/checkpoint/02-03-15:36/last.pth', type=str, help="continue to train from saved model")
    args = parser.parse_args()
    main(args)