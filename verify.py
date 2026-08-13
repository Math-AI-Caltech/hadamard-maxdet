import os
from typing import List

import pandas as pd

import numpy as np
import sympy as sp

def parse_mat(a: np.ndarray, b: np.ndarray, mat_type: str) -> np.ndarray:
    m = a.shape[0]

    j = np.arange(m)
    i = np.arange(m)
    A = a[(j[np.newaxis, :] - i[:, np.newaxis]) % m]
    B = b[(j[np.newaxis, :] - i[:, np.newaxis]) % m]

    m = A.shape[0]
    j = np.ones((m,1), dtype = int)

    if mat_type == "0":
        return np.block([
            [-np.ones((1,1), dtype = np.int64), j.T, -j.T],
            [j, A, B],
            [-j, B.T, -A.T]])

    if mat_type == "1":
        return np.block([
            [np.ones((1,1), dtype = np.int64), j.T, -j.T],
            [j, A, B],
            [-j, B.T, -A.T]])

    return np.block([
        [A, B, -j],
        [B, A.T, j],
        [j.T, -j.T, 1]])

def parse_row(a: str) -> np.ndarray:
    return np.asarray([*map(lambda x:+1 if x=="+" else -1, a)])

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

color_fn = lambda s,w:f"{GREEN if s else RED}{f"{str(s):>{w}}"}{RESET}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = "MaxDet verifier")
    parser.add_argument("-i", "--input", type = str, default = "maxdet_records.csv", help = "Path to csv containing records.")
    parser.add_argument("-o", "--output", type = str, required = False, help = "Path to a directory where reconstructed matrices will be stored.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    print(f"{'n':>5} {'d':>80} {'d > d_prev':>12} {'det == det_csv':>14} {'det_prev == det_prev_csv':>24}")
    print("-" * 139)

    for row in df.itertuples():
        d_ref = 0
        mat = parse_mat(
            a = parse_row(row.a),
            b = parse_row(row.b),
            mat_type = str(row.Type))
        d = abs(sp.Matrix(mat).det_bareis()) / 2**(int(row.n)-1)

        mat_prev = parse_mat(
            a = parse_row(row.a_prev),
            b = parse_row(row.b_prev),
            mat_type = str(row.Type_prev))
        d_prev = abs(sp.Matrix(mat_prev).det_bareis()) / 2**(int(row.n)-1)
        print(
            f"{row.n:>5d} "
            f"{int(d):>80d} "
            f"{color_fn(d > d_prev, 8)} "
            f"{color_fn(d == row.D, 14)} "
            f"{color_fn(d_prev == row.D_prev, 24)}")

        if args.output is not None:
            np.save(os.path.join(args.output, f"{row.n}.npy"), mat)
            np.save(os.path.join(args.output, f"{row.n}_prev.npy"), mat_prev)