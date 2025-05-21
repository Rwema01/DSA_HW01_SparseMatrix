#!/usr/bin/env python3
"""
Custom Sparse Matrix Handler

Provides a SparseMatrix class capable of reading from formatted files,
performing matrix operations (addition, subtraction, multiplication),
and saving the result.

Expected file format:
rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
"""

import sys

class SparseMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = {}  # {(row, col): value}

    @classmethod
    def load_from(cls, filename):
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise Exception(f"Failed to open file: {e}")

        if len(lines) < 2 or not lines[0].startswith("rows=") or not lines[1].startswith("cols="):
            raise ValueError("Input file has wrong format")

        try:
            num_rows = int(lines[0].split("=")[1])
            num_cols = int(lines[1].split("=")[1])
        except Exception:
            raise ValueError("Input file has wrong format")

        matrix = cls(num_rows, num_cols)

        for entry in lines[2:]:
            if not (entry.startswith("(") and entry.endswith(")")):
                raise ValueError("Invalid file format")

            try:
                r, c, v = map(lambda x: int(x.strip()), entry[1:-1].split(","))
            except:
                raise ValueError("Invalid file format")

            if not (0 <= r < num_rows and 0 <= c < num_cols):
                raise ValueError("Invalid file format")

            matrix.set(r, c, v)
        return matrix

    def get(self, row, col):
        return self.data.get((row, col), 0)

    def set(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Invalid matrix index")

        if value == 0:
            self.data.pop((row, col), None)
        else:
            self.data[(row, col)] = value

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match")

        result = SparseMatrix(self.rows, self.cols)

        for (r, c), val in self.data.items():
            result.set(r, c, val)

        for (r, c), val in other.data.items():
            result.set(r, c, result.get(r, c) + val)

        return result

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match")

        result = SparseMatrix(self.rows, self.cols)

        for (r, c), val in self.data.items():
            result.set(r, c, val)

        for (r, c), val in other.data.items():
            result.set(r, c, result.get(r, c) - val)

        return result

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions not aligned for multiplication")

        result = SparseMatrix(self.rows, other.cols)

        other_map = {}
        for (r, c), val in other.data.items():
            other_map.setdefault(r, []).append((c, val))

        for (i, k), val1 in self.data.items():
            if k in other_map:
                for j, val2 in other_map[k]:
                    result.set(i, j, result.get(i, j) + val1 * val2)

        return result

    def __str__(self):
        output = [f"rows={self.rows}", f"cols={self.cols}"]
        for (r, c) in sorted(self.data):
            output.append(f"({r}, {c}, {self.data[(r, c)]})")
        return "\n".join(output)

def interactive_session():
    print("Sparse Matrix Calculator")
    print("1: Add")
    print("2: Subtract")
    print("3: Multiply")

    action = input("Choose (1/2/3): ").strip()
    if action not in ('1', '2', '3'):
        print("Invalid selection.")
        return

    f1 = input("First matrix file: ").strip()
    f2 = input("Second matrix file: ").strip()

    try:
        A = SparseMatrix.load_from(f1)
        B = SparseMatrix.load_from(f2)
    except Exception as err:
        print(f"Error reading matrix: {err}")
        return

    try:
        if action == '1':
            result = A + B
        elif action == '2':
            result = A - B
        else:
            result = A @ B
    except Exception as err:
        print(f"Operation error: {err}")
        return

    save = input("Save result to file? (y/n): ").strip().lower()
    if save == 'y':
        out_path = input("Output file path: ").strip()
        try:
            with open(out_path, 'w') as f:
                f.write(str(result))
            print("Saved.")
        except Exception as err:
            print(f"Failed to write file: {err}")
    else:
        print("Result:")
        print(result)

if __name__ == "__main__":
    interactive_session()

