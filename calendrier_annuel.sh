#!/bin/bash
# Imprimer un calendrier annuel complet en francais

cal -y | perl -pe 's/Su /Di /g; s/Mo /Lu /g; s/Tu /Ma /g; s/We /Me /g; s/Th /Je /g; s/Fr /Ve /g; s/Sa /Sa /g; s/January/Janvier/g; s/February/Février/g; s/March/ Mars/g; s/April/ Avril/g; s/May/Mai/g; s/  June/Juin/g; s/ July/Juillet/g; s/ August/Août/g; s/September/ Septembre/g; s/October/Octobre/g; s/November/Novembre/g; s/December/Décembre/g'

echo
fortune