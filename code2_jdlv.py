import argparse
import random
import sys
from pathlib import Path

from lib import write_grid


def positive_integer(value):
    number = int(value)

    if number <= 0:
        raise argparse.ArgumentTypeError("Must be positive")

    return number


def non_negative_integer(value):
    number = int(value)

    if number < 0:
        raise argparse.ArgumentTypeError("Must be non-negative")

    return number


def parse_arguments():
    parser = argparse.ArgumentParser(description="Game of Life")

    parser.add_argument("-n", "--nb_cells", type=positive_integer, default=10)
    parser.add_argument("-m", "--max_iterations", type=non_negative_integer, default=10)
    parser.add_argument("-s", "--seed", type=int, default=4200)
    parser.add_argument("-o", "--output_directory", default="outputs")
    parser.add_argument("-t", "--output_type", choices=["image", "text"], default="image")
    parser.add_argument("-p", "--periodic", action="store_true")

    return parser.parse_args()


def create_grid(nb_cells, seed):
    generator = random.Random(seed)

    grid = []

    for row in range(nb_cells):
        line = []

        for column in range(nb_cells):
            line.append(generator.randint(0, 1))

        grid.append(line)

    return grid


def read_grid(data):
    values = data.split()

    if not values:
        raise ValueError("Empty grid")

    size = int(values[0])

    if size <= 0:
        raise ValueError("Grid size must be positive")

    cells = values[1:]

    if len(cells) != size * size:
        raise ValueError("Incorrect number of cells")

    if any(cell not in ("0", "1") for cell in cells):
        raise ValueError("Cells must be 0 or 1")

    grid = []

    for row in range(size):
        start = row * size
        end = start + size

        line = [int(cell) for cell in cells[start:end]]
        grid.append(line)

    return grid


def count_neighbors(grid, row, column, periodic):
    size = len(grid)
    count = 0

    for row_offset in (-1, 0, 1):
        for column_offset in (-1, 0, 1):

            if row_offset == 0 and column_offset == 0:
                continue

            neighbor_row = row + row_offset
            neighbor_column = column + column_offset

            if periodic:
                neighbor_row %= size
                neighbor_column %= size

            elif not (0 <= neighbor_row < size and 0 <= neighbor_column < size):
                continue

            count += grid[neighbor_row][neighbor_column]

    return count


def next_generation(grid, periodic):
    size = len(grid)
    new_grid = []

    for row in range(size):
        line = []

        for column in range(size):
            neighbors = count_neighbors(grid, row, column, periodic)

            if grid[row][column] == 1:
                if neighbors == 2 or neighbors == 3:
                    line.append(1)
                else:
                    line.append(0)

            else:
                if neighbors == 3:
                    line.append(1)
                else:
                    line.append(0)

        new_grid.append(line)

    return new_grid


def write_text(grid, iteration):
    print(f"iteration: {iteration}")

    for row in grid:
        print(" ".join(map(str, row)))


def write_images(grid, max_iterations, output_directory, periodic):
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)

    current_grid = grid

    for iteration in range(max_iterations + 1):
        filename = output_path / f"grid_{iteration:04d}.png"

        write_grid(
            matrix=current_grid,
            filename=filename
        )

        if iteration < max_iterations:
            current_grid = next_generation(current_grid, periodic)

    print(
        f"Generation of {max_iterations + 1} images "
        f"in directory {output_directory}"
    )


def main():
    args = parse_arguments()

    input_data = sys.stdin.read()

    if input_data.strip():
        grid = read_grid(input_data)
    else:
        grid = create_grid(args.nb_cells, args.seed)

    if args.output_type == "text":
        for iteration in range(args.max_iterations):
            grid = next_generation(grid, args.periodic)

        write_text(grid, args.max_iterations)

    else:
        write_images(
            grid,
            args.max_iterations,
            args.output_directory,
            args.periodic
        )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
