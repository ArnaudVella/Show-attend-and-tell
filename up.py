#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, flash, redirect, url_for, render_template
from flask import send_file
from werkzeug import secure_filename
from PIL import Image
import os
import io
from final import final

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'

DOSSIER_UPS = './ups/'

def extension_ok(nomfic):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    """code ne fonctionne pas avec un png transparent"""
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg')


@app.after_request
def add_header(response):
    """
   évite la mise en cache, pas optimal, à modifier un jour
    
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
@app.route('/up/', methods=['GET', 'POST'])
def upload():
	img = Image.open('static/vide.png')
	img.save('static/fig.png', "PNG")
	
	@app.route('/up/', methods=['GET', 'POST'])
def upload():
	img = Image.open('static/vide.png')
	img.save('static/fig.png', "PNG")
	
	if request.method == 'POST':
		if 'fic' not in request.files:	# on vérifie qu'un fichier a bien été envoyé
            		flash(u'Vous avez oublié le fichier !', 'error')
            		return redirect(request.url)		
		

		img = request.files['fic']
		
		if extension_ok(img.filename): # on vérifie que son extension est valide
			nom = secure_filename(img.filename)
			img.save('./static/' + nom)			#sauvegarde/ouverture nécessaire pour img.size
			img = Image.open('./static/' + nom)
			os.remove('./static/' + nom)
			
			"""redimensionnement"""
			width, height = img.size
			if width > height:
				left = (width - height) / 2
				right = width - left
				top = 0
				bottom = height
			else:
				top = (height - width) / 2
				bottom = height - top
				left = 0
				right = width
			img = img.crop((left, top, right, bottom))
			img = img.resize([224, 224], Image.ANTIALIAS)
			
			"""conversion en png"""
			img.save('static/img.png',"PNG")
			flash(u'Image envoyée')
			final()
			return render_template('up_up.html')
			
		else:
			flash(u'Ce fichier ne porte pas une extension autorisée !', 'error')
		
			


	return render_template('up_up.html')
    

if __name__ == '__main__':
    app.run(debug=True)
    
    """si mis en ligne, ne fonctionne que pour un seul utilisateur (sinon autre écrase photo du précédent)"""
