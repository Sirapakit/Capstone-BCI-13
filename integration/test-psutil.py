import cProfile

# Function to profile
def my_function():
    for i in range(1000000):
        a = i * i
        b = a + i
        c = a - b
    print("Done!")

# Profile the function using cProfile
cProfile.run('my_function()')
