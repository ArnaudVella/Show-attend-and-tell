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
	
	if request.method == 'POST':
		img = request.files['fic']
		
		if img: # on vérifie qu'un fichier a bien été envoyé
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
		else:
			flash(u'Vous avez oublié le fichier !', 'error')  # ne fonctionne pas!!!!
			


	return render_template('up_up.html')
    
@app.route('/up/view/')
def liste_upped():
    images = [img for img in os.listdir(DOSSIER_UPS) if extension_ok(img)] # la liste des images dans le dossier
    return render_template('up_liste.html', images=images)

@app.route('/up/view/<nom>')
def upped(nom):
    nom = secure_filename(nom)
    if os.path.isfile(DOSSIER_UPS + nom): # si le fichier existe
        return send_file(DOSSIER_UPS + nom, as_attachment=True) # on l'envoie
    else:
        flash(u'Fichier {nom} inexistant.'.format(nom=nom), 'error')
        return redirect(url_for('liste_upped')) # sinon on redirige vers la liste des images, avec un message d'erreur

if __name__ == '__main__':
    app.run(debug=True)
    
    """si mis en ligne, ne fonctionne que pour un seul utilisateur (sinon autre écrase photo du précédent)"""
