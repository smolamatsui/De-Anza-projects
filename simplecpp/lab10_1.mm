#import <XCTest/XCTest.h>
#include "../lab 9-1/functions.cpp"


@interface lab10_1 : XCTestCase

@end

@implementation lab10_1


- (void)testVectorcalculations1 {
    std::vector<int> A1 = {1, 2, 3};
    std::vector<int> B1 = {4, 5, 6};
    std::vector<int> expected1 = {5, 7, 9};
    XCTAssertEqual(expected1, addVectors(A1, B1));
}

- (void)testVectorcalculations2 {
    // Test Case 2: Addition with Zero Vector
    vector<int> A2 = {1, 2, 3};
    vector<int> B2 = {0, 0, 0};
    vector<int> expected2 = {1, 2, 3};
    XCTAssertEqual(expected2, addVectors(A2, B2));
}

- (void)testVectorcalculations3 {
    // Test Case 1: Simple Subtraction
    vector<int> A1 = {4, 5, 6};
    vector<int> B1 = {1, 2, 3};
    vector<int> expected1 = {3, 3, 3};
    XCTAssertEqual(expected1, subtractVectors(A1, B1));
}

- (void)testVectorcalculations4 {
    // Test Case 2: Subtraction Resulting in Negative Values
    vector<int> A2 = {1, 2, 3};
    vector<int> B2 = {4, 5, 6};
    vector<int> expected2 = {-3, -3, -3};    
    XCTAssertEqual(expected2, subtractVectors(A2, B2));
}

- (void)testVectorcalculations5 {
    // Test Case 1: Simple Multiplication
    vector<int> A1 = {1, 2, 3};
    vector<int> B1 = {4, 5, 6};
    vector<int> expected1 = {4, 10, 18};
    XCTAssertEqual(expected1, multiplyVectors(A1, B1));
}

- (void)testVectorcalculations6 {
    // Test Case 2: Multiplication with Zero Vector
    vector<int> A2 = {1, 2, 3};
    vector<int> B2 = {0, 0, 0};
    vector<int> expected2 = {0, 0, 0};
    XCTAssertEqual(expected2, multiplyVectors(A2, B2));
}

- (void)testVectorcalculations7 {
    // Test Case 1: Simple Division
    vector<int> A1 = {10, 20, 30};
    vector<int> B1 = {2, 4, 5};
    vector<int> expected1 = {5, 5, 6};
    XCTAssertEqual(expected1, divideVectors(A1, B1));
}

- (void)testVectorcalculations8 {
    // Test Case 2: Division by One Vector
    vector<int> A2 = {10, 20, 30};
    vector<int> B2 = {1, 1, 1};
    vector<int> expected2 = {10, 20, 30};
    XCTAssertEqual(expected2, divideVectors(A2, B2));
}

@end
