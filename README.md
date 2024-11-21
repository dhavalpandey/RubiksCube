## Introduction

This project is a rubiks cube model in Python that uses the implementation of the cube within the class Cube as a 3x3x6 array. I have used advanced maths concepts of **Matrix Rotation** and **Permutation Groups** to accurately represent and manipulate the cube's state (using cuber notation). This file outlines the mathematical and computational thinking I used when creating model.

## **Mathematical Foundations**

### **Cube Geometry and Representation**

The Rubik's Cube is modeled as a three-dimensional array, with each of the six faces represented as a 3x3 grid. This geometric representation allows for precise manipulation of the cube's state, enabling the simulation of face rotations and the resulting adjustments to adjacent faces.

-   **Faces Indexing:**

-   `state[0]`: Up (**U**) face

-   `state[1]`: Down (**D**) face

-   `state[2]`: Left (**L**) face

-   `state[3]`: Right (**R**) face

-   `state[4]`: Front (**F**) face

-   `state[5]`: Back (**B**) face

Each face is initialized with a uniform color in the solved state:

-   U: White (`'W'`)

-   D: Yellow (`'Y'`)

-   L: Orange (`'O'`)

-   R: Red (`'R'`)

-   F: Green (`'G'`)

-   B: Blue (`'B'`)

### **Matrix Rotation**

Rotating a face of the cube is like performing a 90-degree rotation on a 3x3 matrix. This rotation is achieved through matrix transposition and row reversal operations.

-   **Clockwise Rotation:**

1. Transpose the matrix.

2. Reverse each row of the transposed matrix.

Mathematically:

M' = (\text{Transpose}(M))^{\text{reversed rows}}

-   **Counterclockwise Rotation:**

1. Transpose the matrix.

2. Reverse the order of the rows in the transposed matrix.

Mathematically:
M' = \text{ReverseRowOrder}(\text{Transpose}(M))

### **Cyclic Permutations for Edge Adjustments**

Each face rotation affects not only the face itself but also the adjacent edge pieces of neighboring faces. These changes are modeled using cyclic permutations.

-   **Permutation Cycle:**

When a face is rotated, the corresponding edge rows or columns from adjacent faces are shifted in a cycle. For example, a clockwise rotation of the Up (U) face cycles the top rows of the Left (L), Front (F), Right (R), and Back (B) faces.

\text{L}\_0 \rightarrow \text{F}\_0 \rightarrow \text{R}\_0 \rightarrow \text{B}\_0 \rightarrow \text{L}\_0

## **Mathematical Thinking Implementation**

### **Structure**

-   **State Initialization:**

The cube's initial state is either a solved state or a provided configuration.

-   **Move Implementation:**

Moves are implemented based on standard Rubik's Cube notation (e.g., 'U', "U'", 'D', etc.), each corresponding to a specific rotation and edge adjustment.

-   **Face Rotation Function:**

A reusable function `rotate_face` handles the rotation of any face, applying the appropriate matrix operations based on the direction of rotation.

### **Functionality Details**

#### **rotate_face(face, clockwise=True)**

Performs a 90-degree rotation on a given face.

-   **Clockwise Rotation:**

Transposes the face matrix and reverses each row.

-   **Counterclockwise Rotation:**

```python
def  rotate_face(face, clockwise=True):

    """Rotate a 3x3 face 90 degrees clockwise or counterclockwise."""

    if clockwise:

    return [list(row) for row in  zip(*face[::-1])]

    else:

    return [list(row) for row in  zip(*face)][::-1]
```

Transposes the face matrix and reverses the order of the rows.

**display_move(move) function**
Applies a single move to the cube's state by:

1.  Rotating the specified face using rotate_face.

    **Code Reference:**
    `state[0]  = rotate_face(state[0], clockwise=True)`

    **Explanation:**

    -   **Clockwise Rotation**

        -   **Transpose**: Converts rows to columns.
        -   **Reverse Rows**: Completes the 90-degree rotation.

        M' = \text{ReverseRows}(\text{Transpose}(M))

    -   **Counterclockwise Rotation**:

        -   **Transpose**: Converts rows to columns.
        -   **Reverse Row Order**: Completes the 90-degree rotation in the opposite direction.

        [ M' = \text{ReverseRowOrder}(\text{Transpose}(M)) ]

2.  Performing cyclic replacements of edge rows or columns on adjacent faces.

    **Code Reference:**

    ```python
    state[2][0], state[4][0], state[3][0], state[5][0]  =  (
    state[5][0], state[2][0], state[4][0], state[3][0])
    ```

    **Explanation:**

    -   **Permutation Cycle**:

        -   **Affected Faces**: Left (**L**), Front (**F**), Right (**R**), Back (**B**).
        -   **Edge Pieces**: Top rows (`row index 0`) of each face.

        The permutation follows:

        [ \text{L}_0 \rightarrow \text{F}_0 \rightarrow \text{R}_0 \rightarrow \text{B}_0 \rightarrow \text{L}_0 ]

        -   **Before Move**:

            -   `L_0`: Top row of Left face.
            -   `F_0`: Top row of Front face.
            -   `R_0`: Top row of Right face.
            -   `B_0`: Top row of Back face.

        -   **After Move**:

            -   `L_0` takes the value of `B_0`.
            -   `F_0` takes the value of `L_0`.
            -   `R_0` takes the value of `F_0`.
            -   `B_0` takes the value of `R_0`.

3.  Step-by-Step Example: Applying Move 'U':
    **Initial State:**

    Assume a solved cube where each face has uniform colors.

    **Code Execution:**

    1.  **Rotate Up Face Clockwise:**

        ```python
        state[0]  = rotate_face(state[0], clockwise=True)
        ```

        -   **Mathematical Operation**:

            -   Transpose the Up face matrix.
            -   Reverse each row of the transposed matrix.

        -   **Result**: The Up face is now rotated 90 degrees clockwise.

    2.  **Cyclic Permutation of Adjacent Edges:**

        ```python
        state[2][0], state[4][0], state[3][0], state[5][0]  =  (

        state[5][0], state[2][0], state[4][0], state[3][0]

        )
        ```

        -   **Mathematical Operation**:

            -   **Cycle**:
                -   Left (**L**) top row (`L_0`) receives Back (**B**) top row (`B_0`).
                -   Front (**F**) top row (`F_0`) receives Left (**L**) top row (`L_0`).
                -   Right (**R**) top row (`R_0`) receives Front (**F**) top row (`F_0`).
                -   Back (**B**) top row (`B_0`) receives Right (**R**) top row (`R_0`).

        -   **Result**: The top rows of the adjacent faces are cyclically permuted, reflecting the physical effect of rotating the Up face clockwise.

    **Visualization:**

```python
	# Before Move 'U':
	L_0: [O, O, O]

	F_0: [G, G, G]

	R_0: [R, R, R]

	B_0: [B, B, B]

	# After Move 'u'
	L_0: [B, B, B]

	F_0: [O, O, O]

	R_0: [G, G, G]

	B_0: [R, R, R]
```

This ensures that the cube's state is updated accurately, maintaining consistency with the physical movements of a real Rubik's Cube.

### **Handling Other Moves**

Each move (`'U'`, `'U'`, `'D'`, `'D'`, `'L'`, `'L'`, `'R'`, `'R'`, `'F'`, `'F'`, `'B'`, `'B'`) follows a similar pattern:

1.  **Rotate the Specified Face**: Using rotate_face with the appropriate direction.
2.  **Cyclic Permutation of Adjacent Edges**: Adjusting the affected rows or columns of neighboring faces.

    **Loop-Based Permutations for Certain Moves:**

    For moves like `'L'`, `'R'`, `'F'`, and `'B'`, which involve column manipulations and require element-wise updates, a loop is employed:

    for i in range(3):

    state[0][i][0], state[5][2 - i][2], state[1][i][0], state[4][i][0] = (

    state[4][i][0], state[0][i][0], state[5][2 - i][2], state[1][i][0]

    )

    -   **Logic**:
        -   **Indices Manipulation**:
            -   `2 - i` is used to reverse the order when accessing the Back face's columns to maintain correct orientation.
        -   **Cycle**:
            -   Up face's left column (`U_{i0}`) → Front face's left column (`F_{i0}`) → Down face's left column (`D_{i0}`) → Back face's right column (`B_{2-i,2}`).

## Algorithmic Thinking Implementation

1. **Using a 3x3x6 Array:**
   Using professor Howard A. Peelle's research paper into the best implementation of the cube, I decided to opt for a 3D array which stores the character label for the colour of each square (e.g. 'R' = red)
2. **Scramble Generator:**
   Generating a random move is simple. We just have 2 arrays of the possible moves and randomly decide wether to have a clockwise or anticlockwise move, then randomly pick 1 move. The complexity comes when ensuring the scramble is efficient. If U U' or U' U are generated, they both cancel out and so have no effect on the cube state (we reverse the move we made). Here is how I handled that:

    ````python
        def generate_random_scramble(self, length=10):
        scramble = []

        for _ in range(length):
            move = self.generate_random_move()
            # This code ensures a move is not reversed (e.g. U U' or U' U means the moves cancel out)
            previous_move = scramble[-1] if scramble else None
            if previous_move is not None:
                while previous_move[1:] != move[1:] and previous_move[0] == move[0]:
                    temp = self.generate_random_move()
                    if move != temp:
                        move = temp
                        break

            scramble.append(move)

        return scramble
        ```
    ````

3. **Checking is Solved Fast vs Slow:**
   This is a very straight forward check but my implementation makes the time complexity much faster. We can achieve a simple solution by using 3 for loops and looping through each square to check the colour. This is O(n^3) time complexity - painfully slow. My approach involved using an O(n) approach. I simply had a solved cube stored in a dictionary and did a simple lookup to see if each row matched the row in the solved_cube.

    ```python
        def is_solved_fast(self) -> bool:
          # O(n) time complexity
          correct_faces_count = 0
          solved_cube = {
              'W': [['W'] * 3 for _ in range(3)],
              'Y': [['Y'] * 3 for _ in range(3)],
              'O': [['O'] * 3 for _ in range(3)],
              'R': [['R'] * 3 for _ in range(3)],
              'G': [['G'] * 3 for _ in range(3)],
              'B': [['B'] * 3 for _ in range(3)],
          }

          for face in self.state:
              colour = face[0][0]
              solved_face = solved_cube[colour]
              if face == solved_face:
                  correct_faces_count += 1

          if correct_faces_count == 6:
              return True
          return False
    ```

## References for Concepts

-   https://dl.acm.org/doi/pdf/10.1145/384283.801107
-   [https://web.mit.edu/sp.268/www/rubik.pdf](https://web.mit.edu/sp.268/www/rubik.pdf)
-   https://ruwix.com/the-rubiks-cube/notation/
-   https://drorbn.net/AcademicPensieve/2013-01/NCGE/NCGE.pdf
-   https://en.wikipedia.org/wiki/Rotation_matrix
