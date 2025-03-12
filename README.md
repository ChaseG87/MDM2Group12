# This is the working repository of MDM2's Second Term Group 12.


### It contains 2 versions of the lambda calculus evaluator: lambda_reader.py and lambda_reader2.py.

##### * _lambda_reader.py_ is an outdated version that parses through strings directly and is limited in its computational ability.

##### * _lambda_reader2.py_ is the most updated version that parses through lists of strings and functional objects.

--------------------------------------------------------------------------------------------------------------------------------

#### To see _lambda_reader2.py_ in action simply call the program to run and it will show and example multiplication of 4 times 4.

--------------------------------------------------------------------------------------------------------------------------------

## Other File Descriptions:

* _Definitions.csv_ defines symbols of commonly used functions in lambda calculus.

* _TestCases.csv_ is a list of test cases that can be applied via the **test_case()** function in **lambda_reader2.py**.

* _hello.txt_ is the file called to be read by default when **lambda_reader2.py** is called.

* _input.txt_ is an old test case input for **lambda_reader.py**.

* _manim_animation.py_ produces a simple beta reduction animation of the identity function using the manim library.

* _successor1.py_ produces an animation of the beta reduction steps showing the successor of 0 is 1.

* _NAND\_vid.mp4_ is a video of a NAND gate being represented in pure lambda calculus.

* _identity\_vid.mp4_ is a video of the identity function $\lambda x.x$ being applied to $y$.

* _successor\_vid.mp4_ is a video of the successor function, $\lambda nfx.f(nfx)$, beiong applied to 0.

###### To run _manim_animation.py_ or _successor1.py_, manim, a latex interpreter, and a video processor like ffmpeg must be installed.
###### To run _lambda_reader2.py_ pandas must be installed.

--------------------------------------------------------------------------------------------------------------------------------

### **🔴 Important Note:** `λ` is represented as a forward-slash string `/`.


