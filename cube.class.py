import random
import copy

def convert_to_3d_array(array):
    return [[list(face[i:i+3]) for i in range(0, 9, 3)] for face in array]

def rotate_face(face, clockwise=True):
    if clockwise:
        return [list(row) for row in zip(*face[::-1])]
    else:
        return [list(row) for row in zip(*face)][::-1]


class Cube:
    def __init__(self, initial_state=None):
        # Initial state of the cube is a 6-by-3-by-3 cubic array (Local Representation)
        if initial_state != None and len(initial_state) == 54:
            self.state = convert_to_3d_array([
                initial_state[:9],
                initial_state[9:18],
                initial_state[18:27],
                initial_state[27:36],
                initial_state[36:45],
                initial_state[45:]
            ])
        else:
            self.state = initial_state or [
                [['W'] * 3 for _ in range(3)],
                [['Y'] * 3 for _ in range(3)],
                [['O'] * 3 for _ in range(3)],
                [['R'] * 3 for _ in range(3)],
                [['B'] * 3 for _ in range(3)],
                [['G'] * 3 for _ in range(3)],
            ]

    def __str__(self):
        # Returns a string representation of the cube - user friendly
        faces = ['Up', 'Down', 'Left', 'Right', 'Front', 'Back']
        result = ""
        for i, face in enumerate(self.state):
            result += f"{faces[i]} Face:\n"
            for row in face:
                result += ' '.join(row) + '\n'
            result += '\n'
        return result

    def generate_random_move(self):
        moves_clockwise = ['U', 'D', 'L', 'R', 'F', 'B']
        moves_anticlockwise = ['U\'', 'D\'', 'L\'', 'R\'', 'F\'', 'B\'']
        which_way = random.choice(['clockwise', 'anticlockwise'])
        if which_way == 'clockwise':
            move = random.choice(moves_clockwise)
        else:
            move = random.choice(moves_anticlockwise)
        return move
    
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
    
    def display_move(self, move):
        """Modify the cube state based on the given move."""
        state = self.state
        def rotate_face(face, clockwise=True):
            """Rotate a 3x3 face 90 degrees clockwise or counterclockwise."""
            if clockwise:
                return [list(row) for row in zip(*face[::-1])]
            else:
                return [list(row) for row in zip(*face)][::-1]

        if move == 'U':
            # Rotate Up face clockwise
            state[0] = rotate_face(state[0], clockwise=True)
            # Rotate edges around the Up face
            state[2][0], state[4][0], state[3][0], state[5][0] = (
                state[5][0], state[2][0], state[4][0], state[3][0]
            )
        elif move == "U'":
            # Rotate Up face counterclockwise
            state[0] = rotate_face(state[0], clockwise=False)
            state[2][0], state[5][0], state[3][0], state[4][0] = (
                state[4][0], state[2][0], state[5][0], state[3][0]
            )
        elif move == 'D':
            # Rotate Down face clockwise
            state[1] = rotate_face(state[1], clockwise=True)
            state[2][2], state[5][2], state[3][2], state[4][2] = (
                state[4][2], state[2][2], state[5][2], state[3][2]
            )
        elif move == "D'":
            # Rotate Down face counterclockwise
            state[1] = rotate_face(state[1], clockwise=False)
            state[2][2], state[4][2], state[3][2], state[5][2] = (
                state[5][2], state[2][2], state[4][2], state[3][2]
            )
        elif move == 'L':
            # Rotate Left face clockwise
            state[2] = rotate_face(state[2], clockwise=True)
            for i in range(3):
                state[0][i][0], state[5][2 - i][2], state[1][i][0], state[4][i][0] = (
                    state[4][i][0], state[0][i][0], state[5][2 - i][2], state[1][i][0]
                )
        elif move == "L'":
            # Rotate Left face counterclockwise
            state[2] = rotate_face(state[2], clockwise=False)
            for i in range(3):
                state[0][i][0], state[4][i][0], state[1][i][0], state[5][2 - i][2] = (
                    state[5][2 - i][2], state[0][i][0], state[4][i][0], state[1][i][0]
                )
        elif move == 'R':
            # Rotate Right face clockwise
            state[3] = rotate_face(state[3], clockwise=True)
            for i in range(3):
                state[0][i][2], state[4][i][2], state[1][i][2], state[5][2 - i][0] = (
                    state[5][2 - i][0], state[0][i][2], state[4][i][2], state[1][i][2]
                )
        elif move == "R'":
            # Rotate Right face counterclockwise
            state[3] = rotate_face(state[3], clockwise=False)
            for i in range(3):
                state[0][i][2], state[5][2 - i][0], state[1][i][2], state[4][i][2] = (
                    state[4][i][2], state[0][i][2], state[5][2 - i][0], state[1][i][2]
                )
        elif move == 'F':
            # Rotate Front face clockwise
            state[4] = rotate_face(state[4], clockwise=True)
            for i in range(3):
                state[0][2][i], state[3][i][0], state[1][0][2 - i], state[2][2 - i][2] = (
                    state[2][2 - i][2], state[0][2][i], state[3][i][0], state[1][0][2 - i]
                )
        elif move == "F'":
            # Rotate Front face counterclockwise
            state[4] = rotate_face(state[4], clockwise=False)
            for i in range(3):
                state[0][2][i], state[2][2 - i][2], state[1][0][2 - i], state[3][i][0] = (
                    state[3][i][0], state[0][2][i], state[2][2 - i][2], state[1][0][2 - i]
                )
        elif move == 'B':
            # Rotate Back face clockwise
            state[5] = rotate_face(state[5], clockwise=True)
            for i in range(3):
                state[0][0][i], state[2][2 - i][0], state[1][2][2 - i], state[3][i][2] = (
                    state[3][i][2], state[0][0][i], state[2][2 - i][0], state[1][2][2 - i]
                )
        elif move == "B'":
            # Rotate Back face counterclockwise
            state[5] = rotate_face(state[5], clockwise=False)
            for i in range(3):
                state[0][0][i], state[3][i][2], state[1][2][2 - i], state[2][2 - i][0] = (
                    state[2][2 - i][0], state[0][0][i], state[3][i][2], state[1][2][2 - i]
                )
    
    def apply_all_moves(self, moves):
        """Apply a sequence of moves to the cube."""
        for move in moves:
            self.display_move(move)

    def is_solved_slow(self) -> bool:
        # O(n^3) time complexity
        for face in self.state:
            if len(set([cell for row in face for cell in row])) > 1:
                return False
            return True
        
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

    def solve_moves_generator(self):
        """Generates a set of moves to solve the cube using Iterative Deepening DFS."""
        moves = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"]
        max_depth = 7  # You can adjust this value based on performance

        # Helper function to convert the cube state to a hashable key
        def state_to_key(state):
            return tuple(tuple(tuple(row) for row in face) for face in state)

        # Depth-limited DFS
        def dfs(cube, depth, path, visited):
            if cube.is_solved_fast():
                return path
            if depth == 0:
                return None
            state_key = state_to_key(cube.state)
            if state_key in visited:
                return None
            visited.add(state_key)
            for move in moves:
                new_cube = Cube(copy.deepcopy(cube.state))
                new_cube.display_move(move)
                result = dfs(new_cube, depth - 1, path + [move], visited)
                if result is not None:
                    return result
            visited.remove(state_key)
            return None

        for depth in range(1, max_depth + 1):
            visited = set()
            result = dfs(self, depth, [], visited)
            if result is not None:
                return result
        return []

# Example usage:
cube = Cube()
scramble = cube.generate_random_scramble(10)
print("Scramble Moves:", scramble)
cube.apply_all_moves(scramble)
print("Scrambled Cube:")
print(cube)

solution = cube.solve_moves_generator()
print("Solution Moves:", solution)
cube.apply_all_moves(solution)
print("Solved Cube:")
print(cube)