import numpy as np

# Hint: what size is the output?
X = np.array([[ 0.04, 0.30, 0.23, 0.21 ],
              [ 0.03, 0.34, 0.15, 0.06 ],
              [ 0.02, 0.20, 0.11, 0.07 ],
              [ 0.14, 0.22, 0.35, 0.17 ]])
X_padded = np.zeros((6, 6))
X_padded[1:-1, 1:-1] = X
# loop through rows using index i and columns using index j to produce output:
Y = {}
i = 0
j = 0

F = np.array([[ 0.9, 0.8, 0.3 ],
              [ 0.6, 0.2, 0.4 ],
              [ 0.1, 0.7, 0.5 ]])

for i in range(len(X)):
    for j in range(len(X[0])):
        Y[i, j] = np.sum(X_padded[i:(i+3), j:(j+3)] * F)

print(Y)

# Validation for Cell 0,0 of the output, which is 0.319
# We start at 0.2 in the filter (middle) because the edges are multipled by 0, which is the 'padding'
print((0.04 * 0.2) + (0.3 * 0.4) + (0.03 * 0.7) + (0.34 * 0.5))
