from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
import sqlite3

def accueil_view(request):
    connexion = sqlite3.connect('./db.sqlite3')
    c = connexion.cursor()
    c.execute('SELECT * FROM films_paris ORDER BY annee_tournage DESC LIMIT 25')
    result = c.fetchall()
    c.close()
    connexion.close()
    dico = []
    for i in result:
        dico.append([
            i[0],
            i[1],
            i[2],
            i[3],
            i[4],
            i[5],
            i[6],
            i[7],
            i[8],
            i[9],
            i[10],
            i[11],
            i[12],
            i[13]
        ])
    context = {
        'result': dico,
        'message': 'Bienvenue ! Pour rechercher un film, remplissez comme vous le souhaitez les cases suivantes puis appuyez sur le bouton rechercher ;)'
    }
    return render(request, 'index.html', context)

@csrf_exempt
def rechercher(request):
    data = [
        request.POST.get('nom').lower(),
        request.POST.get('typ').lower(),
        request.POST.get('prod').lower(),
        request.POST.get('real').lower(),
        request.POST.get('arron').lower(),
        request.POST.get('annee')
    ]

    titles = ['nom_tournage', 'type_tournage', 'nom_producteur', 'nom_realisateur', 'ardt_lieu', 'annee_tournage']

    requete = ''
    first = True

    if data[5] not in ['2016','2017','2018','2019','2020','2021']:
        data[5] = ''

    for i in range(len(data)):
        value = str(data[i]).lower()
        if(value != ''):
            if first:
                requete += ' WHERE '
                first = False
            else:
                requete += ' AND '
            requete += ' ' + titles[i] + ' COLLATE Latin1_General_CI COLLATE NOCASE LIKE "%' + value + '%" COLLATE Latin1_General_CI COLLATE NOCASE'
    
    connexion = sqlite3.connect('./db.sqlite3')
    c = connexion.cursor()
    c.execute('SELECT * FROM films_paris ' + requete + ' ORDER BY annee_tournage DESC')
    result = c.fetchall()
    c.close()
    connexion.close()
    dico = []
    for i in result:
        dico.append([
            i[0],
            i[1],
            i[2],
            i[3],
            i[4],
            i[5],
            i[6],
            i[7],
            i[8],
            i[9],
            i[10],
            i[11],
            i[12],
            i[13]
        ])
    if len(dico) == 0:
        message = 'Pas de données pour cette requête'
    else:
        message = ''
    context = {
        'result': dico,
        'message': message
    }
    return render(request, 'index.html', context)


@csrf_exempt
def details(request, id):
    titles = ['id_lieu','annee_tournage','type_tournage','nom_tournage','nom_realisateur','nom_producteur','adresse_lieu','ardt_lieu','date_debut','date_fin','coord_x','coord_y','geo_shape','geo_point_2d']
    connexion = sqlite3.connect('./db.sqlite3')
    c = connexion.cursor()
    c.execute('SELECT * FROM films_paris WHERE id_lieu = "' + id + '" ORDER BY annee_tournage DESC')
    result = c.fetchall()
    c.close()
    connexion.close()
    if len(result) == 0:
        message = 'Pas de données pour cette requête'
    else:
        message = ''
    context = {
        'result': zip(titles, result[0]),
        'message': message,
        'name': result[0][3],
        'coord': [result[0][10], result[0][11]]
    }
    return render(request, 'details.html', context)