# Record Maximal-Determinant ±1 Matrices (dimensions 51, 107, 111, 115)
This repository contains constructions of the matrices described in the paper [zenodo/records/22024187](https://zenodo.org/records/22024187). The circulant blocks are encoded by their first rows and assembled into full matrices using the `parse_mat(...)` function in [verify.py](verify.py).

## Usage
```bash
python3 -m pip install -r requirements.txt
python3 verify.py -i maxdet_records.csv
```
In order to store the reconstructed matrices in the current directory, use:
```bash
python3 verify.py -i maxdet_records.csv -o .
```

## CSV format
Each row describes a matrix of order $n = 3~\mathrm{mod}~4$. The strings `a` and `b` contain the first rows of the two circulant blocks defining the $n$-dimensional ±1 matrix. Column `D` is the normalized determinant: $|\det{X}| / 2^{n-1}$. The corresponding `_prev` fields describe the records accessed from the archived [MaxDet database](http://wayback.archive-it.org/219/20190316001107/http://www.indiana.edu/~maxdet/).

| Column(s) | Description |
| --- | --- |
| `n` | Dimension |
| `a` and `b` | First rows of the circulant blocks |
| `D` | Normalized determinant |
| `Type` | Type of the parametrization |
| `*_prev` | Previous benchmark |

## Expected verification output
|n | d | d > d_prev | det == det_csv | det_prev == det_prev_csv |
| ---: | ---: |:---:|:---:|:---:|
| 51 | 17776121037665193653653203125 | True | True | True |
| 107 | 25405109779472820154713362533412847329846084693257600588972842045966418068198 | True | True | True |
| 111 | 139781659519566648611004967987048891981864344843163654605529677292458895404455125 | True | True | True |
| 115 | 824875559997507123862490321617482346789417543713732896000289208985971332478680569108 | True | True | True |