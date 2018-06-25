import matplotlib.pyplot as plt
import cPickle as pickle
import tensorflow as tf
from core.solver import CaptioningSolver
from core.model import CaptionGenerator
#from core.utils import load_coco_data
#from core.bleu import evaluate
import io
import os
import numpy as np
from PIL import Image
from scipy import ndimage
import skimage.transform
from core.vggnet import Vgg19
from core import utils


plt.rcParams['figure.figsize'] = (8.0, 6.0)  # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

def final():
	tf.reset_default_graph()
	img_path='./static/img.png'
	
	def get_image_features(image_path):
				g1 = tf.Graph()  ## This is one graph
				with g1.as_default():
					vgg_model_path = 'showattendtell/data/imagenet-vgg-verydeep-19.mat'
					vggnet = Vgg19(vgg_model_path)  # prepare model for feature extraction
					vggnet.build()
			
					with tf.Session(config=utils.config) as sess:
						tf.global_variables_initializer().run()
						image_path=image_path
						image_batch = np.array([np.array(Image.open(image_path))]).astype(np.float32)
						return sess.run(vggnet.features, feed_dict={vggnet.images: image_batch})
	
	#feats = np.ndarray([1, 196, 512], dtype=np.float32)
	feats = get_image_features(img_path)
	
	
	data = {}
	data['features'] = feats
	data['file_names'] = img_path   
	with open('./data/train/word_to_idx.pkl', 'rb') as f:
	    word_to_idx = pickle.load(f)
	
	model = CaptionGenerator(word_to_idx, dim_feature=[196, 512], dim_embed=512,
	                                   dim_hidden=1024, n_time_step=16, prev2out=True, 
	                                             ctx2out=True, alpha_c=1.0, selector=True, dropout=True)
	                                             
	print "one"
	                                             
	solver = CaptioningSolver(model, data, data, n_epochs=15, batch_size=128, update_rule='adam',
	                                      learning_rate=0.0025, print_every=2000, save_every=1, image_path='./image/val2014_resized',
	                                pretrained_model=None, model_path='./model/lstm', test_model='./model/lstm/model-20', print_bleu=False, log_path='./log/')																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												
	                             
	
	print "two"
	
	solver.test(data)
	




