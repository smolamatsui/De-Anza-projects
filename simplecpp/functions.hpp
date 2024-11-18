#ifndef FUNCTIONS_HPP_
#define FUNCTIONS_HPP_

#include <iostream>
#include <cstdlib>

// Function to initialize the game board
void initializeBoard(char board[3][3]);

// Function to print the game board
void printBoard(char board[3][3]);

// Function to check if there is a win
bool checkWin(char board[3][3]);

// Function to check if the game is a draw
bool checkDraw(char board[3][3]);

// Function to allow a player to make a move
void playerMove(char board[3][3]);

// Function to generate a random move for the computer
void computerMove(char board[3][3]);

#endif /* FUNCTIONS_HPP_ */

