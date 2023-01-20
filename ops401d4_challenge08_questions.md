- Look at the syntax of the code and comments -- not having written it yourself, how easy is it to quickly parse through this code and get an idea of how it works? How could the author have made it easier?
- Look at the comments at the start of each function and within the sections of each function -- is it clear from the comments what each bit of code does and how? How much do you need to read the code to understand what each part does? Is reading the comments faster than reading (someone else's) code?
- Look at the functions which handle encryption/decryption -- how much code is repeated?
- Look at the rest of the functions (besides `main()`) -- how much code is repeated? Do you see anything that could be reduced or combined?
- How many of the functions do you think you could re-use? Would you need to change them? How would you change them?
- How many functions print feedback for the user? How many of them can be called silently to operate in the background?
- Are there any uses of code here that you've never seen before? For example, the use of dictionaries, the function arguments in line 34, `kwargs` on line 76, the booleans in line 108, "try...except" on lines 155 and 161, or `if __name__ == "__main__":` on line 276. What do these do? Why might these be useful or necessary?
- On lines 28 and 29, the two program modes are listed out of order, but when the script is executed the menu displays in numerical order. How does this occur?
- Why use a dictionary to store the program modes? What all benefits might this bring? What are the downsides?
- Assume you have written a new function/feature. Besides the function itself, how many places in the code will you need to make changes in order to itegrate it into the menu system?
- Run the program and explore its features.
  - What do you try, and how do you go about systematically testing it?
  - Can you cause the program to crash?
  - Are you confident that either there are no bugs or that you have found all the bugs?
  - How does the code handle errors so that it avoids crashes?