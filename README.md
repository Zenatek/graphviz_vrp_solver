# Graphviz vrp solver

Tool per risolvere problemi VRP partendo da un file excel contenente base di carico, matrix_distances, destinazioni e domanda giornaliera.
La soluzione trovata viene visualizzata su un grafo colorato per ogni tratta utilizzando la libreria grafica graphviz ed esportata in pdf.

### Dependencies

```
python3.7, localsolver version 9.0, pandas, xlrd, graphviz
```

## Usage

```
cd src

python3.7 vrp.py input_file [output_file] [time_limit] [nb_trucks] [truck_capacity] [Demands_for_day]
```

## Example

```
python3.7 vrp.py ../distanze.xls result 5 9 39 DomandaGiorno18
```

## Results

Nella cartella results vengono salvati i file .pdf del grafo e il output_file con il numero ottimale dei truck, la distanza totale percorsa e il percorso di ogni truck.
