# 5-NN, Rocchio
Python version: 3.5.2
## Usage

These programs require DV and docs at first with using 

```bash  
python3 DV_divide.py 
```
the DV is divided into two parts that are TestData and TrainData.

5-NN can be used with  
```bash  
python3 KNN.py 
```
I found 41.80446765303162 % ratio with 5-NN it has a very low ratio with anasayfa around 3 % after finishing that category ratio increase.

Rocchio can be used with  
```bash  
python3 Rocchio.py 
```
As it is much faster than the KNN because it creates centroid instead of checking each training document. its ratio is 3.685432385374347 %

