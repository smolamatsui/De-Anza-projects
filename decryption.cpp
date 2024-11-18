#include "decryption.hpp"
#include <iostream>

void decryptFile(string inputFileName, string outputFileName, int key) {
    ifstream inputFile(inputFileName);
    ofstream outputFile(outputFileName);

    if (inputFile.is_open() && outputFile.is_open()) {
        char ch;
        while (inputFile.get(ch)) {
            // Decrypt each character using the Caesar cipher
            if (isalpha(ch)) {
                if (isupper(ch)) {
                    ch = ((ch - 'A' - key + 26) % 26) + 'A';
                }
                else {
                    ch = ((ch - 'a' - key + 26) % 26) + 'a';
                }
            }
            outputFile.put(ch);
        }

        // Close the files
        inputFile.close();
        outputFile.close();
    }
}
