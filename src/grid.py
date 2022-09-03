from piece import PType, Piece, generateCoords, generatePiece


class Grid:
    basicWallKick = [
        [(-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 0>>1
        [(1, 0), (1, -1), (0, 2), (1, 2)],  # 1>>0
        [(1, 0), (1, -1), (0, 2), (1, 2)],  # 1>>2
        [(-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 2>>1
        [(1, 0), (1, 1), (0, -2), (1, -2)],  # 2>>3
        [(-1, 0), (-1, -1), (0, 2), (-1, 2)],  # 3>>2
        [(-1, 0), (-1, -1), (0, 2), (-1, 2)],  # 3>>0
        [(1, 0), (1, 1), (0, -2), (1, -2)],  # 0>>3
    ]

    iWallKick = [
        [(-2, 0), (1, 0), (-2, -1), (1, 2)],  # 0>>1
        [(2, 0), (-1, 0), (2, 1), (-1, -2)],  # 1>>0
        [(-1, 0), (2, 0), (-1, 2), (2, -1)],  # 1>>2
        [(1, 0), (-2, 0), (1, -2), (-2, 1)],  # 2>>1
        [(2, 0), (-1, 0), (2, 1), (-1, -2)],  # 2>>3
        [(-2, 0), (1, 0), (-2, -1), (1, 2)],  # 3>>2
        [(1, 0), (-2, 0), (1, -2), (-2, 1)],  # 3>>0
        [(-1, 0), (2, 0), (-1, 2), (2, -1)],  # 0>>3
    ]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[False for y in range(width)] for x in range(height)]
        self.blocks = [[None for y in range(width)] for x in range(height)]
        self.toDelete = []

    def getGrid(self) -> list[list[bool]]:
        return self.grid

    def isBlock(self, x: int, y: int) -> bool:
        return self.grid[y][x]

    def tryFit(self, piece: Piece, rotation=None) -> bool:
        fits = True
        coords = generateCoords(
            piece.type, rotation if rotation is not None else piece.rotation
        )
        for x, y in coords:
            if piece.x + x < 0 or piece.x + x >= self.width:
                fits = False
                break
            if piece.y + y < 0 or piece.y + y >= self.height:
                fits = False
                break
            if self.isBlock(piece.x + x, piece.y + y):
                fits = False
                break
        if fits:
            return True
        if rotation is None or rotation == piece.rotation:
            return False

        testIndex = self.getTestIndex(piece.rotation, rotation)
        tests = (
            self.basicWallKick[testIndex]
            if piece.type != PType.I
            else self.iWallKick[testIndex]
        )
        originalPosition = (piece.x, piece.y)
        oldRotation = piece.rotation
        for testX, testY in tests:
            piece.x += testX
            piece.y -= testY
            piece.setRotate(rotation)
            if self.tryFit(piece, rotation):
                return True
            piece.x, piece.y = originalPosition
            piece.setRotate(oldRotation)
        return False

    def getTestIndex(self, oldRot: int, newRot: int) -> int:
        match oldRot:
            case 0:
                return 0 if newRot == 1 else 7
            case 1:
                return 1 if newRot == 0 else 2
            case 2:
                return 3 if newRot == 1 else 4
            case 3:
                return 5 if newRot == 2 else 6

    def addPiece(self, piece: Piece) -> None:
        for x, y in piece.getCoords():
            self.grid[piece.y + y][piece.x + x] = True
            self.blocks[piece.y + y][piece.x + x] = piece.getBlock(
                piece.x + x, piece.y + y
            )

    def clearLines(self) -> None:  # Todo: Add return value
        for y in range(self.height):
            if not all(self.grid[y]):
                continue
            self.grid.pop(y)
            self.grid.insert(0, [False for x in range(self.width)])
            self.toDelete += self.blocks.pop(y)
            self.blocks.insert(0, [None for x in range(self.width)])

            for yy in range(y + 1):
                for block in self.blocks[yy]:
                    if block:
                        block.y += 1
            y -= 1

    def clear(self) -> None:
        self.grid = [[False for y in range(self.width)] for x in range(self.height)]
        self.blocks = [[None for y in range(self.width)] for x in range(self.height)]
