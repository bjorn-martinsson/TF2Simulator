This is a work in progress. Expect many changes in the near future.

This project aims to as accurately as possible simulate rocket jumping in TF2. This project
is of interest for anyone that wants to understand how the source engine works, or want to
simulate specifc scenarios. This simulation is mainly based on TF2's source code. It should 
therefor correctly simulate many of TF2's movement bugs, such as C-taps, "deadstrafes", 
"C-taps making you shorter", bunnyjumping resulting in higher jump, bounces, and jump bugs.

It is challenging to simulate TF2 accurately. In particular TF2's use of 32 bit signed floats
results in rather large and unpredictable floating point errors. To counteract this issue, 
the project uses 64 bit doubles everywhere except for when the floating point errors are unusually
large and predictable. It is not perfect, but it gets close.

The goal for the future is to build a bounce checker based on this simulation. Hopefully 
much smarter than any of the tools currently in use, such as https://github.com/bakapear/bcheck
