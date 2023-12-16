#!/bin/bash

#matlab -nodesktop -nodisplay -r ""
for j in 8192
do
  for i in 30 40 50 60 70 80 90 100
  do
    if ! matlab -nodisplay -nodesktop -r "try main('uniform',$i,$j); catch; end; quit"
    then
      echo "Não foi possível executar o script matlab para uniforme $i%"
      exit 1
    fi
    if ! matlab -nodisplay -nodesktop -r "try main('normal',$i,$j); catch; end; quit"
    then
      echo "Não foi possível executar o script matlab para normal $i%"
      exit 1
    fi
  done
done

echo "\ndeu tudo certo"
