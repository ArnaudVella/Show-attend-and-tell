import io
from PIL import Image
from scipy import ndimage

import matplotlib.pyplot as plt
import skimage.transform
import tensorflow as tf

#from bleu import evaluate
from core.vggnet import Vgg19
#from resize import resize_image
from utils import *
from core import utils




class CaptioningSolver(object):
    def __init__(self, model, data, val_data, **kwargs):
        """
        Required Arguments:
            - model: Show Attend and Tell caption generating model
            - data: Training data; dictionary with the following keys:
                - features: Feature vectors of shape (82783, 196, 512)
                - file_names: Image file names of shape (82783, )
                - captions: Captions of shape (400000, 17)
                - image_idxs: Indices for mapping caption to image of shape (400000, )
                - word_to_idx: Mapping dictionary from word to index
            - val_data: validation data; for print out BLEU scores for each epoch.
        Optional Arguments:
            - n_epochs: The number of epochs to run for training.
            - batch_size: Mini batch size.
            - update_rule: A string giving the name of an update rule
            - learning_rate: Learning rate; default value is 0.01.
            - print_every: Integer; training losses will be printed every print_every iterations.
            - save_every: Integer; model variables will be saved every save_every epoch.
            - pretrained_model: String; pretrained model path
            - model_path: String; model path for saving
            - test_model: String; model path for test
        """

        self.model = model
        self.data = data
        self.val_data = val_data
        self.n_epochs = kwargs.pop('n_epochs', 10)
        self.batch_size = kwargs.pop('batch_size', 100)
        self.update_rule = kwargs.pop('update_rule', 'adam')
        self.learning_rate = kwargs.pop('learning_rate', 0.01)
        self.print_bleu = kwargs.pop('print_bleu', False)
        self.print_every = kwargs.pop('print_every', 100)
        self.save_every = kwargs.pop('save_every', 1)
        self.log_path = kwargs.pop('log_path', './log/')
        self.model_path = kwargs.pop('model_path', './model/')
        self.pretrained_model = kwargs.pop('pretrained_model', None)
        self.test_model = kwargs.pop('test_model', './model/lstm/model-1')

        # set an optimizer by update rule
        if self.update_rule == 'adam':
            self.optimizer = tf.train.AdamOptimizer
        elif self.update_rule == 'momentum':
            self.optimizer = tf.train.MomentumOptimizer
        elif self.update_rule == 'rmsprop':
            self.optimizer = tf.train.RMSPropOptimizer

        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)


    def test(self, data, split='train', attention_visualization=True, save_sampled_captions=True):
		'''
		Args:
			- data: dictionary with the following keys:
			- features: Feature vectors of shape (5000, 196, 512)
			- file_names: Image file names of shape (5000, )
			- captions: Captions of shape (24210, 17)
			- image_idxs: Indices for mapping caption to image of shape (24210, )
			- features_to_captions: Mapping feature to captions (5000, 4~5)
			- split: 'train', 'val' or 'test'
			- attention_visualization: If True, visualize attention weights with images for each sampled word. (ipthon notebook)
			- save_sampled_captions: If True, save sampled captions to pkl file for computing BLEU scores.
		'''
		features = data['features']

        # build a graph to sample captions
		alphas, betas, sampled_captions = self.model.build_sampler(max_len=20)    # (N, max_len, L), (N, max_len)

		config = tf.ConfigProto(allow_soft_placement=True)
		config.gpu_options.allow_growth = True
		with tf.Session(config=config) as sess:
			saver = tf.train.Saver()
			saver.restore(sess, self.test_model)
			features_batch, image_files = sample_coco_minibatch(data, self.batch_size)
			
			
			feed_dict = { self.model.features: features_batch }
			alps, bts, sam_cap = sess.run([alphas, betas, sampled_captions], feed_dict)  # (N, max_len, L), (N, max_len)
			decoded = decode_captions(sam_cap, self.model.idx_to_word)
			if attention_visualization:
				n=0
				plt.clf()
				print "Sampled Caption: %s" %decoded[n]
				img = ndimage.imread(data['file_names'])
				plt.subplot(4, 5, 1)
				plt.imshow(img)
				plt.axis('off')
				
				words = decoded[n].split(" ")
				for t in range(len(words)):
					if t > 18:
						break
					plt.subplot(4, 5, t+2)
					plt.text(0, 1, '%s(%.2f)'%(words[t], bts[n,t]) , color='black', backgroundcolor='white', fontsize=8)
					plt.imshow(img)
					alp_curr = alps[n,t,:].reshape(14,14)
					alp_img = skimage.transform.pyramid_expand(alp_curr, upscale=16, sigma=20)
					plt.imshow(alp_img, alpha=0.85)
					plt.axis('off')
				plt.savefig('./static/fig.png')
                   
                   

            #~ if save_sampled_captions:
                #~ all_sam_cap = np.ndarray((features.shape[0], 20))
                #~ num_iter = int(np.ceil(float(features.shape[0]) / self.batch_size))
                #~ print num_iter
                #~ for i in range(num_iter):
                    #~ features_batch = features[i*self.batch_size:(i+1)*self.batch_size]
                    #~ feed_dict = { self.model.features: features_batch }
                    #~ all_sam_cap[i*self.batch_size:(i+1)*self.batch_size] = sess.run(sampled_captions, feed_dict)
                #~ all_decoded = decode_captions(all_sam_cap, self.model.idx_to_word)
                #~ save_pickle(all_decoded, "./data/%s/%s.candidate.captions.pkl" %(split,split))
                
   
