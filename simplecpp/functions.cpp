#include "functions.hpp"
#include <iostream>
#include <cstdlib>

using namespace std;

// Function to initialize the game board
void initializeBoard(char board[3][3]) {
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            board[i][j] = ' ';
        }
    }
}

// Function to print the game board
void printBoard(char board[3][3]) {
    cout << "  1 2 3\n";
    for (int i = 0; i < 3; ++i) {
        cout << i + 1 << " ";
        for (int j = 0; j < 3; ++j) {
            cout << board[i][j];
            if (j < 2) cout << "|";
        }
        cout << "\n";
        if (i < 2) cout << "  -----\n";
    }
}

// Function to check if there is a win
bool checkWin(char board[3][3]) {
    // Check rows and columns for a win
    for (int i = 0; i < 3; ++i) {
        // Check rows
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != ' ')
            return true;
        // Check columns
        if (board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[0][i] != ' ')
            return true;
    }
    // Check diagonals
    if ((board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != ' ') ||
        (board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != ' '))
        return true;
    
    return false;
}

// Function to check if the game is a draw
bool checkDraw(char board[3][3]) {
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (board[i][j] == ' ')
                return false; // If there's an empty cell, game is not a draw
        }
    }
    return true; // All cells are filled, game is a draw
}

// Function to allow a player to make a move
void playerMove(char board[3][3]) {
    int row, col;
    while (true) {
        cout << "Enter your move (row and column): ";
        cin >> row >> col;
        
        // Adjust row and col to 0-based indexing
        row--;
        col--;
        
        // Check if the move is valid
        if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == ' ') {
            board[row][col] = 'X';
            break;
        } else {
            cout << "Invalid move. Try again." << endl;
        }
    }
}

// Function to generate a random move for the computer
void computerMove(char board[3][3]) {
    cout << "Computer's move:" << endl;
    while (true) {
        int row = rand() % 3;
        int col = rand() % 3;
        if (board[row][col] == ' ') {
            board[row][col] = 'O';
            break;
        }
    }
}
