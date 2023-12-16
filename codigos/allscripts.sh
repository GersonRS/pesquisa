#!/bin/bash

for j in 81 205 410 614 819 2048 4096 8192
do
	if ! python ligo.py $j
	then
		echo "\nNão foi possível executar o script ligo."
		exit 1
	fi
	for t in normal ligo
	do
		for i in 10 20 30 40 50 60 70 80 90 100
		do
            if ! python generateData.py $t $i $j
            then
                echo "\nNão foi possível executar o script para o $t de $i% com $j de janela."
                exit 1
            fi
		done
	done
done

#matlab -nodesktop -nodisplay -r ""
for j in 81 205 410 614 819 2048 4096 8192
do
	for t in normal ligo
	do
		for i in 10 20 30 40 50 60 70 80 90 100
		do
		    if ! matlab -nodisplay -nodesktop -r "try main('$t',$i,$j); catch; end; quit"
		    then
		      echo "Não foi possível executar o script matlab para o $t de $i% com $j de janela."
		      exit 1
		    fi
		done
	done
done

echo "\ndeu tudo certo"
