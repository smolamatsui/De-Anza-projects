#import <XCTest/XCTest.h>
#include "../test2/functions.cpp" // Adjust the path as per your project structure

@interface TicTacToeTests : XCTestCase

@end

@implementation TicTacToeTests

- (void)testCheckWinRow {
    char board[3][3] = { {'X', 'X', 'X'},
                         {' ', 'O', ' '},
                         {' ', 'O', ' '} };
    XCTAssertTrue(checkWin(board));
}

- (void)testCheckWinColumn {
    char board[3][3] = { {'X', ' ', 'O'},
                         {'X', 'O', ' '},
                         {'X', ' ', 'O'} };
    XCTAssertTrue(checkWin(board));
}

- (void)testCheckWinDiagonal1 {
    char board[3][3] = { {'X', 'O', ' '},
                         {'O', 'X', ' '},
                         {' ', ' ', 'X'} };
    XCTAssertTrue(checkWin(board));
}

- (void)testCheckWinDiagonal2 {
    char board[3][3] = { {' ', 'O', 'X'},
                         {'O', 'X', ' '},
                         {'X', ' ', 'O'} };
    XCTAssertTrue(checkWin(board));
}

- (void)testCheckWinNoWin1 {
    char board[3][3] = { {'X', 'O', 'X'},
                         {'O', 'X', 'O'},
                         {'O', 'X', 'O'} };
    XCTAssertFalse(checkWin(board));
}

- (void)testCheckWinNoWin2 {
    char board[3][3] = { {'X', 'O', 'X'},
                         {'X', 'O', 'O'},
                         {'O', 'X', 'O'} };
    XCTAssertFalse(checkWin(board));
}

- (void)testCheckDrawDraw {
    char board[3][3] = { {'X', 'O', 'X'},
                         {'X', 'O', 'O'},
                         {'O', 'X', 'O'} };
    XCTAssertTrue(checkDraw(board));
}

- (void)testCheckDrawNotDraw1 {
    char board[3][3] = { {' ', ' ', ' '},
                         {' ', ' ', ' '},
                         {' ', ' ', ' '} };
    XCTAssertFalse(checkDraw(board));
}

- (void)testCheckDrawNotDraw2 {
    char board[3][3] = { {'X', 'O', ' '},
                         {' ', 'X', ' '},
                         {' ', ' ', 'O'} };
    XCTAssertFalse(checkDraw(board));
}

- (void)testComputerMoveEmptyBoard {
    char board[3][3] = { {' ', ' ', ' '},
                         {' ', ' ', ' '},
                         {' ', ' ', ' '} };
    computerMove(board);
    int countO = 0;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == 'O') {
                countO++;
            }
        }
    }
    XCTAssertEqual(countO, 1);
}

- (void)testComputerMovePartialBoard {
    char board[3][3] = { {'X', 'O', 'X'},
                         {' ', 'X', ' '},
                         {'O', ' ', ' '} };
    computerMove(board);
    int countO = 0;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == 'O') {
                countO++;
            }
        }
    }
    XCTAssertEqual(countO, 3);
}

- (void)testComputerMoveOneEmptySpot {
    char board[3][3] = { {'O', 'O', 'X'},
                         {'X', 'O', 'O'},
                         {'X', 'X', ' '} };
    computerMove(board);
    int countO = 0;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == 'O') {
                countO++;
            }
        }
    }
    XCTAssertEqual(countO, 5);
}

@end
