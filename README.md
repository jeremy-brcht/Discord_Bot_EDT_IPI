# discord_bot_edt_ipi

## Installation

1. Ajouter un fichier `settings.py` à la racine du projet.
2. Ajouter et adapter le code suivant dans `settings.py` :

```
class MySettings:
    username = "<username>"
    password = "<password>"
    token = "<token>"
```

## Commandes

- **!edt** : Affiche l'emploi du temps de la semaine en cours
- **!edt \<jj/mm/aaaa>** : Affiche l'emploi du temps du jour indiqué
- **!edt \<numéro de semaine>,\<année>** : Affiche l'emploi du temps de la semaine indiquée
