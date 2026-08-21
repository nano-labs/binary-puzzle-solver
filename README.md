# Binary Puzzle Solver
A binary puzzle is a challenging puzzle that requires logical reasoning. 

## The rules

Each cell must contain either a zero or a one. No more than two identical numbers may be directly adjacent or directly below each other. Each row and each column is unique and contains an equal number of zeros and ones.


### Usage
```python
_ = None
binary = [
    [_, _, _, _, 1, _, 1, 1, _, 0, _, _],  # 1
    [_, _, _, 0, _, 0, _, _, 0, _, _, _],  # 2
    [0, _, _, _, _, _, _, _, _, _, _, 0],  # 3
    [_, _, 1, _, _, 0, _, _, _, _, _, 0],  # 4
    [_, _, _, _, 1, _, _, _, _, _, 1, _],  # 5
    [_, _, 1, _, 1, _, _, _, _, 0, _, _],  # 6
    [0, _, _, _, _, _, _, _, _, _, _, _],  # 7
    [_, _, _, 1, 1, _, _, _, _, _, 0, _],  # 8
    [0, _, 0, _, _, 1, _, _, 1, _, 0, 0],  # 9
    [_, 1, _, _, _, 1, _, _, _, _, _, 0],  # 10
    [_, _, _, _, 0, _, _, _, 1, 1, _, _],  # 11
    [1, _, _, 0, 0, _, _, _, _, _, _, 1],  # 12
]

s = BinarySolver(binary)
s.solve()
```

![Run](https://github.com/nano-labs/binary-puzzle-solver/blob/main/imgs/binary-solver.gif)

![puzzle](https://github.com/nano-labs/binary-puzzle-solver/blob/main/imgs/puzzle.jpeg)
