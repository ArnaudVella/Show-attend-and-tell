# Show, Attend and Tell 
<b> Update (25/05/2018)</b> Ceci est le code de mon projet de Master 1 Ingénieur Civil Electricien à la Faculté Polytechnique de Mons, 
dont l’objectif est de créer une page web permettant de décrire de façon automatisée le contenu d’une image uploadée.
Ce projet est basé sur le travail de Yunjey Choi, qui a implémenté la méthode exposée dans le papier [Show, Attend and Tell: Neural Image Caption Generation with Visual Attention](http://arxiv.org/abs/1502.03044) publié en février 2015 et qui introduit
un générateur de légende d’image basé sur un mécanisme d’attention.




## Références
implémentation de Yunjey Choi: https://github.com/yunjey/show-attend-and-tell

<br/>


## Entrainement du modèle

Github ne permettant pas d'importer des fichiers de plus de 500mb, il m'est impossible d'y partager le modèle pré-entrainé.
Vous pouvez néanmoins l'entrainer sur votre propre machine en suivant les instructions de Yunjey Choi.

Remarque:
l'entrainement du modèle nécessite au moins 47gb de mémoire ram, ou à défaut de mémoire virtuelle. Linux permet de gérer facilement la mémoire swap si nécessaire.
L'entrainement prend plusieurs juours pour arriver à terme, en fonction de votre machine et de l'utilisation ou pas de Tensorflow-GPU.
Une fois l'entrainement terminé, vous pouvez ne conserver que les dossiers data et model.

Vous pouvez à présent cloner ce repo:

```bash
$ git clone https://github.com/ArnaudVella/show-attend-and-tell.git
```
Et y ajouter les dossiers data et model.

Pour faire tourner la page web en local, il vous faut installer  Flask:
```bash
$ sudo pip install Flask
```
Vous pouvez à présent lancer le programme:
```bash
$ python up.py
```
et entrer l'adresse localhost:5000/up dans votre navigateur internet.


remarque:
Pour l'instant la page est à unage unique et l'application se plante lorsque vous re-uploadez une nouvelle image. pour éviter vous devez le relancer entre chaque nouvelle image. 

